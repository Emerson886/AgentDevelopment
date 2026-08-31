
"""
Agent <-> GUI 线程桥。

为什么需要它
------------
Agent 运行在 ChatProcessor（QThread 工作线程）里，而 Qt 控件只能在主线程
访问。如果工具函数直接去改 lineEdit_conf / 调用 MainWindow 的方法，会出现
跨线程访问控件的崩溃或界面卡死。

本模块提供一个基于「Qt 信号 + threading.Event」的同步请求/响应桥：

    Agent 工作线程 (ChatProcessor)                主线程 (MainWindow)
    ------------------------------                --------------------
    工具函数调用 bridge.call(op, payload)
        │   emit(operationRequested)  ──(队列连接)──►  GuiOperationHandlers.handle_operation()
        │                                                  │ 按 op 分派
        │                                                  │   * 同步操作：直接 call.finish(结果)
        │                                                  │   * 异步操作：register_pending() 后
        │                                                  │               启动检测线程，稍后 resolve()
        │  call.done.wait(超时) 阻塞 ◄──────────────────────┘
        ▼
    返回结构化结果给 LLM
"""
from __future__ import annotations
# 使用了 from __future__ import annotations 之后，注解表达式不会被立即求值，而是以字符串的形式存储。
# 只有在你显式请求时（例如通过 typing.get_type_hints()）才会被求值。

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from PySide6.QtCore import QObject, Signal


@dataclass
class ToolCall:
    """一次工具调用的完整上下文，跨线程传递（普通 dataclass，可被信号携带）。"""

    op: str                                          # 操作名，如 "set_detection_params"
    payload: dict = field(default_factory=dict)      # 参数
    call_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    # 唯一标识符, uuid.uuid4()生成一个随机的 UUID（通用唯一识别码）版本4（基于随机数）, 包含连字符-
    # .hex将 UUID 对象转换为 不含连字符 - 的纯十六进制字符串
    """
    field() 是数据类提供的字段描述器，它允许我们通过参数精细控制字段行为，并且延迟默认值的生成。
    default_factory 是 field() 中最重要的参数之一。它的规则是：
    它接收一个 无参数的可调用对象（Callable，比如函数或 lambda）。
    这个可调用对象不是在类定义时执行，而是在 __init__ 方法被调用时（即实例化时）执行。
    执行后的返回值会被赋值给该字段。
    如果你用 default=uuid.uuid4().hex[:12]，定义类时就会生成一次。
    如果你用 default_factory=lambda: uuid.uuid4().hex[:12]，每创建一个对象才会生成一次。
    """
    done: threading.Event = field(default_factory=threading.Event, repr=False)
    # repr=False 指示数据类在生成 __repr__ 方法时，彻底忽略该字段。
    # 这样你打印实例时，只看到业务相关的字段，视线不会被这类底层同步原语干扰。

    result: Any = None                               # 主线程写回的返回值
    error: Optional[str] = None                      # 主线程写回的错误信息
    cancelled: bool = False
    created_at: float = field(default_factory=time.time)

    def finish(self, result: Any = None, error: Optional[str] = None) -> None:
        self.result = result
        self.error = error
        self.done.set()


class ToolBridge(QObject):
    """
    用法：
        bridge = ToolBridge(main_window)                 # 必须创建在主线程
        bridge.set_handler(gui_handlers.handle_operation)  # 主线程 QObject 方法
        bridge.activity.connect(main_window.on_agent_activity)

        # 工作线程内（工具函数中）：
        result = bridge.call("set_detection_params", {...}, timeout=30)
    """

    operationRequested = Signal(object)   # 携带 ToolCall
    activity = Signal(str)                # 给 GUI 的进度提示（可选）

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._lock = threading.RLock()
        self._pending: dict[str, ToolCall] = {}
        self._last_result: Any = None
        self._busy = threading.RLock()    # 同一时刻只允许一个工具调用在途

    # ---------------------------------------------------------------- 工作线程侧
    def call(self, op: str, payload: Optional[dict] = None,
             timeout: float = 60.0) -> Any:
        """阻塞式 RPC：发出请求并等待主线程处理完成。

        返回主线程给出的 result；出错 / 超时返回 {"ok": False, "error": ...}。
        """
        with self._busy:
            call = ToolCall(op=op, payload=payload or {})
            try:
                self.operationRequested.emit(call)
            except Exception as e:                     # noqa: BLE001
                return {"ok": False, "error": f"桥接信号发送失败: {e}"}
            if not call.done.wait(timeout):
                call.cancelled = True
                return {"ok": False, "error": f"操作超时或未响应: {op} ({timeout}s)"}
            if call.error:
                return {"ok": False, "error": call.error}
            return call.result

    def notify(self, message: str) -> None:
        """向 GUI 发送一条进度消息（非阻塞，失败静默）。"""
        try:
            self.activity.emit(message)
        except Exception:                                # noqa: BLE001
            pass

    def get_last_result(self) -> Any:
        """读取最近一次检测结果摘要（主线程写入，工作线程读取）。"""
        with self._lock:
            return self._last_result

    # ---------------------------------------------------------------- 主线程侧
    def set_handler(self, handler: Callable[[ToolCall], None]) -> None:
        """把处理回调接到 operationRequested 信号上。

        注意：handler 必须是「主线程 QObject 的方法」（如
        GuiOperationHandlers.handle_operation），Qt 才会对工作线程发来的
        信号使用队列连接，保证 handler 在主线程执行。
        """
        self.operationRequested.connect(handler)

    def register_pending(self, call: ToolCall) -> None:
        """登记一个需要异步完成的调用（如检测任务）。"""
        with self._lock:
            self._pending[call.call_id] = call

    def resolve(self, call_id: str, result: Any = None,
                error: Optional[str] = None) -> bool:
        """异步任务完成后，把结果写回并唤醒等待中的工作线程。"""
        with self._lock:
            call = self._pending.pop(call_id, None)
        if call is None:
            return False
        call.finish(result=result, error=error)
        return True

    def first_pending(self, op: str) -> Optional[ToolCall]:
        """取最早一个尚未完成的指定操作调用（按登记顺序）。"""
        with self._lock:
            for c in self._pending.values():
                if c.op == op:
                    return c
        return None

    def cancel_by_op(self, op: str) -> int:
        """取消所有指定操作类型的挂起调用（例如用户手动开始新的检测）。"""
        with self._lock:
            calls = [c for c in self._pending.values() if c.op == op]
            for c in calls:
                self._pending.pop(c.call_id, None)
            print("当前相同的任务:", calls)
        for c in calls:
            c.cancelled = True
            c.finish(error=f"操作被新的任务取代: {op}")
        return len(calls)

    def cancel_all(self) -> int:
        """取消所有挂起调用（程序退出 / 一轮对话结束时调用）。"""
        with self._lock:
            calls = list(self._pending.values())
            self._pending.clear()
        for c in calls:
            c.cancelled = True
            c.finish(error="操作被取消")
        return len(calls)

    def set_last_result(self, result: Any) -> None:
        with self._lock:
            self._last_result = result
