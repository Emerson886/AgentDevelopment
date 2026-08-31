
"""
主线程侧的 GUI 操作处理器。

GuiOperationHandlers 是一个 QObject，归属主线程；把它的 handle_operation
方法连接到 ToolBridge.operationRequested 信号后，Qt 会自动把工作线程发来的
调用以「队列连接」投递到主线程执行，从而保证所有控件读写都在主线程完成。

对外两个入口：
- handle_operation(call)   —— 由桥的信号驱动，负责分派所有工具操作；
- finish_detection(summary)—— 由 MainWindow.on_detect_finished 调用，
                              把检测结果写回并唤醒等待中的 agent。
"""
from __future__ import annotations

import os
from collections import Counter
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QUrl, Slot
from PySide6.QtGui import QDesktopServices

from agent_bridge import ToolBridge, ToolCall

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _detection_running(win) -> bool:
    """判断当前是否有 YOLO 检测线程在跑。

    注意原版 main.py 把 ChatProcessor 和 DetectProcesser 都挂在
    current_processor 上，这里用 input_path 属性区分检测线程。
    """
    proc = getattr(win, "current_processor", None)
    if proc is None or not callable(getattr(proc, "isRunning", None)):
        return False
    try:
        return bool(proc.isRunning()) and hasattr(proc, "input_path")
    except Exception:                              # noqa: BLE001
        return False


def build_detection_summary(results, file_type: str) -> dict:
    """从 YOLO 检测结果汇总出给 LLM 看的统计信息（主线程调用）。

    results 可以是单个 Results（图片）或 Results 列表（文件夹/视频帧）。
    """
    counter = Counter()
    frames = 0
    total_time = 0.0
    items = results if isinstance(results, (list, tuple)) else [results]
    for r in items:
        frames += 1
        boxes = getattr(r, "boxes", None)
        cls = getattr(boxes, "cls", None) if boxes is not None else None
        if cls is not None:
            try:
                cls_ids = cls.int().tolist()
            except Exception:                  # noqa: BLE001
                cls_ids = []
            if cls_ids:
                names = getattr(r, "names", {})
                for c in cls_ids:
                    counter[names.get(c, str(c))] += 1
        speed = getattr(r, "speed", None)
        if speed:
            total_time += sum(speed.values()) / 1000.0
    label = {".mp4": "视频", "dir": "文件夹"}.get(file_type, "图片")
    return {
        "ok": True,
        "file_type": label,
        "frames": frames,
        "total_defects": int(sum(counter.values())),
        "classes": dict(counter.most_common(10)),
        "total_time_s": round(total_time, 3),
    }


class GuiOperationHandlers(QObject):
    """在主线程里真正操作 MainWindow 控件的处理器。"""

    def __init__(self, main_window, bridge: ToolBridge):
        super().__init__(main_window)
        self.win = main_window
        self.bridge = bridge

    # ------------------------------------------------------------------ 入口
    @Slot(object)
    def handle_operation(self, call: ToolCall) -> None:
        handler = getattr(self, f"op_{call.op}", None)
        if handler is None:
            call.finish(error=f"未知操作: {call.op}")
            return
        try:
            handler(call)
        except Exception as e:                     # noqa: BLE001
            call.finish(error=f"操作执行异常({call.op}): {e}")

    # ------------------------------------------------------------------ 同步操作
    def _effective_params(self) -> dict:
        win = self.win
        return {
            "model": win.comboBox_model.currentText(),
            "conf": win.lineEdit_conf.text(),
            "max_det": win.lineEdit_nums.text(),
            "save_json": not win.rb_JSON_n.isChecked(),
            "save_txt": not win.rb_txt_n.isChecked(),
            "show_labels": win.rb_hidel_n.isChecked(),
            "show_conf": win.rb_hidec_n.isChecked(),
            "camera_open": not win.is_camera_free,
            "detection_running": _detection_running(win),
        }

    def op_get_system_status(self, call: ToolCall) -> None:
        print(self._effective_params())
        call.finish(result=self._effective_params())

    def op_set_detection_params(self, call: ToolCall) -> None:
        win = self.win
        p = call.payload
        changed = []

        if "conf" in p:
            conf = float(p["conf"])
            win.lineEdit_conf.setText(f"{conf:.2f}")
            changed.append(f"conf={conf:.2f}")
        if "max_det" in p:
            n = int(p["max_det"])
            win.lineEdit_nums.setText(str(n))
            changed.append(f"max_det={n}")
        if "save_json" in p:
            win.rb_JSON_n.setChecked(not bool(p["save_json"]))
            changed.append(f"save_json={bool(p['save_json'])}")
        if "save_txt" in p:
            win.rb_txt_n.setChecked(not bool(p["save_txt"]))
            changed.append(f"save_txt={bool(p['save_txt'])}")
        if "show_labels" in p:
            win.rb_hidel_n.setChecked(bool(p["show_labels"]))
            changed.append(f"show_labels={bool(p['show_labels'])}")
        if "show_conf" in p:
            win.rb_hidec_n.setChecked(bool(p["show_conf"]))
            changed.append(f"show_conf={bool(p['show_conf'])}")
        if "model" in p:
            idx = self._model_to_index(p["model"])
            if idx is None:
                call.finish(error=f"未知模型: {p['model']}，可用: {self._model_choices()}")
                return
            win.comboBox_model.setCurrentIndex(idx)
            changed.append(f"model={win.comboBox_model.currentText()}")

        try:
            win.lb_hint.setText("提示信息: 已通过AI助手调整参数: " + ", ".join(changed))
        except Exception:                          # noqa: BLE001
            pass
        call.finish(result={"ok": True, "changed": changed,
                            "params": self._effective_params()})

    def _model_to_index(self, model) -> Optional[int]:
        win = self.win
        text = str(model).strip().lower()
        mapping = {"1": 0, "2": 1, "3": 2, "n": 0, "s": 1, "m": 2}
        if text in mapping:
            return mapping[text]
        for i in range(win.comboBox_model.count()):
            if win.comboBox_model.itemText(i).lower() == text:
                return i
        return None

    def _model_choices(self) -> list:
        win = self.win
        return [win.comboBox_model.itemText(i)
                for i in range(win.comboBox_model.count())]

    def op_open_camera(self, call: ToolCall) -> None:
        win = self.win
        want = bool(call.payload.get("open", True))
        if _detection_running(win):
            call.finish(error="检测任务运行中，不能操作摄像头")
            return
        currently_open = not win.is_camera_free
        if want == currently_open:
            call.finish(result={"ok": True, "camera_open": currently_open,
                                "note": "摄像头状态未变化"})
            return
        win.camera_click()   # camr_click() 内部完成开关切换
        call.finish(result={"ok": True, "camera_open": not win.is_camera_free})

    def op_open_output_location(self, call: ToolCall) -> None:
        path = call.payload.get("path") or str(PROJECT_ROOT / "temp_file")
        if not os.path.exists(path):
            call.finish(error=f"路径不存在: {path}")
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.abspath(path)))
        call.finish(result={"ok": True, "path": os.path.abspath(path)})

    # ------------------------------------------------------------------ 异步操作
    def op_run_detection(self, call: ToolCall) -> None:
        win = self.win
        if _detection_running(win):
            call.finish(error="已有检测任务正在运行，请稍后再试")
            return
        if not win.is_camera_free:
            win.detect_click()
            self.bridge.register_pending(call)
            summary = {
                "ok": True,
                "file_type": "camera",
                "frames": None,
                "total_defects": None,
                "classes": None,
                "total_time_s": None,
            }
            self.finish_detection(summary)
            return
        path_in = call.payload.get("path_in") or ""
        if not path_in or not os.path.exists(path_in):
            call.finish(error=f"输入路径不存在: {path_in}")
            return
        # if not win.is_camera_free:
        #     call.finish(error="摄像头处于打开状态，请先关闭摄像头再检测")
        #     return


        # 把 GUI 控件设置成与调用参数一致，然后走与「手动点击检测」完全相同的流程，
        # 保证行为一致（历史记录、界面展示等都会正常发生）。
        win.lineEdit_path_in.setText(path_in)
        path_out = call.payload.get("path_out") or ""
        if path_out:
            win.lineEdit_path_out.setText(path_out)

        # 取代任何旧的挂起检测调用，登记本次调用（检测完成后由 finish_detection 结算）
        self.bridge.cancel_by_op("run_detection")
        win.detect_click()
        self.bridge.register_pending(call)

        # 若检测没能启动（例如文件类型不合法、模型路径错误），立即给出错误
        if not _detection_running(win):
            self.bridge.resolve(call.call_id, error="检测未能启动，请查看界面提示")

    def finish_detection(self, summary: dict) -> None:
        """由 MainWindow.on_detect_finished 调用，完成挂起的检测工具调用。"""
        self.bridge.set_last_result(summary)
        call = self.bridge.first_pending("run_detection")
        if call is None:
            return
        if call.payload.get("save") and call.payload.get("path_out"):
            try:
                self.win.save_click()   # 复用界面的保存流程（复制文件 + 标记历史）
                summary = dict(summary)
                summary["saved_to"] = call.payload.get("path_out")
            except Exception as e:      # noqa: BLE001
                summary = dict(summary)
                summary["save_error"] = str(e)
        self.bridge.resolve(call.call_id, result=summary)
