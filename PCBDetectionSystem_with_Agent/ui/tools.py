
"""
Agent 工具定义。

设计原则
--------
1. 每个工具都真正做事：要么通过 bridge 把操作交给主线程执行
   （改参数、开摄像头、跑检测、打开文件夹），要么直接读取文件
   （历史、模型列表、知识库）。
2. 所有工具返回可被 LLM 直接阅读的 JSON 字符串，字段稳定、简洁。
3. 只读工具不经过 GUI，避免不必要的跨线程往返。

"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[1]
HISTORY_FILE = PROJECT_ROOT / "history" / "history.json"
MODEL_WEIGHTS_DIR = PROJECT_ROOT / "model" / "weights"
CUSTOM_MODELS_DIR = PROJECT_ROOT / "model" / "custom_models"
KNOWLEDGE_FILE = Path(__file__).resolve().parent / "knowledge_base.md"

MODEL_CHOICES = {
    "n": "PCB_YOLO_n_1024_CAwithCBAM.pt",   # 快速
    "s": "PCB_YOLO_s_1024_CAwithCBAM.pt",   # 兼顾速度与精度
    "m": "PCB_YOLO_m_1024_CAwithCBAM.pt",   # 精确
}


def build_tools(bridge) -> list:
    """根据桥接器构造可用的工具列表（在 init_agent 时调用）。

    bridge 为 None 时，所有需要 GUI 的工具都会返回「未连接界面」的错误，
    便于在没有界面的环境里调试只读工具。
    """

    def _gui(op: str, payload: Optional[dict] = None, timeout: float = 30.0):
        if bridge is None:
            return {"ok": False, "error": "当前未连接图形界面，无法执行该操作"}
        return bridge.call(op, payload or {}, timeout=timeout)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def get_system_status() -> str:
        """获取检测系统的当前状态（模型、参数、摄像头、是否正在检测等）。

        Returns:
            返回 JSON 字符串，包含 model、conf、max_det、save_json、
            save_txt、show_labels、show_conf、camera_open、detection_running
        """
        return json.dumps(_gui("get_system_status", timeout=10), ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def set_detection_params(
        conf: Optional[float] = None,
        max_det: Optional[int] = None,
        save_json: Optional[bool] = None,
        save_txt: Optional[bool] = None,
        show_labels: Optional[bool] = None,
        show_conf: Optional[bool] = None,
        model: Optional[str] = None,
    ) -> str:
        """调整检测参数，只修改显式提供的字段，其余保持不变。

        Args:
            conf: 置信度阈值，取值 0.0-1.0，默认 0.25，越小检测越宽松
            max_det: 单张图最多检测的缺陷数量，1-100，默认 5
            save_json: 是否保存检测结果的 JSON 标注文件
            save_txt: 是否保存检测结果的 txt 标注文件
            show_labels: 是否在结果图上显示类别标签
            show_conf: 是否在结果图上显示置信度
            model: 模型选择。传字符串 "1"/"2"/"3"（1=快速, 2=兼顾, 3=精确），
                或 "n"/"s"/"m"，或自定义模型文件名

        Returns:
            返回 JSON 字符串：生效后的完整参数表；参数非法时返回错误信息
        """
        # 本地快速校验，减少无谓的跨线程往返
        if conf is not None and not (0.0 <= float(conf) <= 1.0):
            return json.dumps({"ok": False, "error": "conf 必须在 0.0-1.0 之间"},
                              ensure_ascii=False)
        if max_det is not None and not (1 <= int(max_det) <= 100):
            return json.dumps({"ok": False, "error": "max_det 必须在 1-100 之间"},
                              ensure_ascii=False)
        for name, val in (("save_json", save_json), ("save_txt", save_txt),
                          ("show_labels", show_labels), ("show_conf", show_conf)):
            if val is not None and not isinstance(val, bool):
                return json.dumps({"ok": False, "error": f"{name} 必须是布尔值"},
                                  ensure_ascii=False)
        payload = {k: v for k, v in {
            "conf": conf, "max_det": max_det, "save_json": save_json,
            "save_txt": save_txt, "show_labels": show_labels,
            "show_conf": show_conf, "model": model,
        }.items() if v is not None}
        return json.dumps(_gui("set_detection_params", payload), ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def open_camera(open: bool = True) -> str:
        """打开或关闭摄像头实时检测。

        Args:
            open: True 打开摄像头，False 关闭摄像头

        Returns:
            返回 JSON 字符串：camera_open 表示操作后的摄像头状态
        """
        return json.dumps(_gui("open_camera", {"open": bool(open)}), ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def run_detection(camera_on: bool, path_in: str = "", path_out: str = "", save: bool = False) -> str:
        """对指定的图片、文件夹或视频执行缺陷检测。

        Args:
            camera_on: 摄像头状态，是否打开(True/False)，camera_on为 True 时，忽略其他参数
            path_in: 输入路径，可以是图片文件、视频文件或只含图片的文件夹
            path_out: 保存结果的文件夹路径；save 为 False 时可省略
            save: 是否把检测结果保存到 path_out，默认为 False

        Returns:
            返回 JSON 字符串：file_type、frames、total_defects、classes
            （各缺陷类别数量）、total_time_s、saved_to 等
        """
        if camera_on:
            result = _gui("run_detection", timeout=600)
            return json.dumps(result, ensure_ascii=False)
        if not path_in or not os.path.exists(path_in):
            return json.dumps({"ok": False, "error": f"输入路径不存在: {path_in}"},
                              ensure_ascii=False)
        if save and not path_out:
            return json.dumps({"ok": False, "error": "save 为 True 时必须提供 path_out"},
                              ensure_ascii=False)
        if save and not os.path.exists(path_out):
            return json.dumps({"ok": False, "error": f"保存路径不存在: {path_out}"},
                              ensure_ascii=False)
        result = _gui("run_detection",
                      {"path_in": path_in, "path_out": path_out, "save": bool(save)},
                      timeout=600)   # 检测是异步长任务，给足超时
        return json.dumps(result, ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def get_latest_result() -> str:
        """获取最近一次检测的统计结果（不重新检测）。

        Returns:
            返回 JSON 字符串；没有检测记录时 ok=False
        """
        if bridge is None:
            return json.dumps({"ok": False, "message": "未连接界面"}, ensure_ascii=False)
        result = bridge.get_last_result()
        if result is None:
            return json.dumps({"ok": False, "message": "暂无检测结果"}, ensure_ascii=False)
        return json.dumps(result, ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def get_history(limit: int = 5, keyword: str = "") -> str:
        """查询历史检测记录。

        Args:
            limit: 最多返回的记录条数，1-50，默认 5
            keyword: 按记录内容关键词过滤（如路径、缺陷），为空表示不过滤

        Returns:
            返回 JSON 字符串：记录列表，每条含 文件类型/检测时间/来源路径/
            是否保存/保存路径
        """
        limit = max(1, min(int(limit), 50))
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:                     # noqa: BLE001
            return json.dumps({"ok": False, "error": f"读取历史失败: {e}"},
                              ensure_ascii=False)
        headers = data.get("headers", [])
        records = data.get("records", [])
        items = []
        for row in records:
            rec = dict(zip(headers, row + [""] * (len(headers) - len(row))))
            if keyword and keyword.lower() not in json.dumps(rec, ensure_ascii=False).lower():
                continue
            items.append(rec)
        return json.dumps({"ok": True, "total": len(items), "records": items[-limit:]},
                          ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def list_models() -> str:
        """列出系统可用的检测模型。

        Returns:
            返回 JSON 字符串：内置模型（n 快速 / s 兼顾 / m 精确）与
            自定义模型列表
        """
        builtin = []
        for key, fn in MODEL_CHOICES.items():
            if (MODEL_WEIGHTS_DIR / fn).exists():
                builtin.append({"id": key, "file": fn, "type": "内置"})
        custom = []
        if CUSTOM_MODELS_DIR.exists():
            custom = [{"id": f, "file": f, "type": "自定义"}
                      for f in sorted(os.listdir(CUSTOM_MODELS_DIR)) if f.endswith(".pt")]
        return json.dumps({"ok": True, "builtin": builtin, "custom": custom},
                          ensure_ascii=False)

    # ------------------------------------------------------------------
    # @tool(parse_docstring=True)
    # def query_knowledge_base(keyword: str = "") -> str:
    #     """从系统知识库中查询资料（缺陷类型、参数含义、使用说明等）。
    #
    #     Args:
    #         keyword: 查询关键词（如缺陷类型、术语），为空返回全部内容
    #
    #     Returns:
    #         返回 JSON 字符串：匹配的知识库内容片段
    #     """
    #     if not KNOWLEDGE_FILE.exists():
    #         return json.dumps({"ok": False, "error": f"知识库文件不存在: {KNOWLEDGE_FILE}"},
    #                           ensure_ascii=False)
    #     text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    #     if not keyword:
    #         return json.dumps({"ok": True, "content": text[:4000]}, ensure_ascii=False)
    #     lines = text.splitlines() # 按照换行符等进行文本划分
    #     hits = [ln for ln in lines if keyword.lower() in ln.lower()]
    #     section = [ln for ln in lines
    #                if ln.strip().startswith("#") or keyword.lower() in ln.lower()]
    #     return json.dumps({"ok": True, "keyword": keyword,
    #                        "matched_lines": hits[:20], "section": section[:60]},
    #                       ensure_ascii=False)

    # ------------------------------------------------------------------
    @tool(parse_docstring=True)
    def open_output_location(path: str = "") -> str:
        """在文件管理器中打开一个文件夹。

        Args:
            path: 要打开的文件夹路径，为空则打开临时检测结果目录

        Returns:
            返回 JSON 字符串：ok 表示是否成功打开
        """
        return json.dumps(_gui("open_output_location", {"path": path}), ensure_ascii=False)

    return [get_system_status, set_detection_params, open_camera, run_detection,
            get_latest_result, get_history, list_models, open_output_location]
