
from __future__ import annotations

import threading
from typing import Optional

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from agent_bridge import ToolBridge
from tools import build_tools

import middlewares as mids

from RAG import RAG

config = {"configurable": {"thread_id" : "main"}}
checkpointer = InMemorySaver()

# ---------------------------------------------------------------------------
# RAG 惰性单例 + 失败降级：
#   - 进程内只初始化一次（避免每轮对话重复创建 Milvus 客户端与嵌入模型）；
#   - 初始化或检索失败时静默降级为普通对话，不让知识库拖垮整个聊天。
# ---------------------------------------------------------------------------
_rag_instance: Optional[RAG] = None
_rag_lock = threading.Lock()


def _get_rag() -> Optional[RAG]:
    """惰性初始化 RAG 单例；失败返回 None（下次调用会重试，自动恢复）。"""
    global _rag_instance
    if _rag_instance is not None:
        return _rag_instance
    with _rag_lock:
        if _rag_instance is None:
            try:
                rag = RAG()
                rag.init_embedding_model()
                _rag_instance = rag
                print("[RAG] 知识库检索已就绪")
            except Exception as e:  # noqa: BLE001
                print(f"[RAG] 初始化失败，本次对话降级为普通问答: {e}")
                return None
    return _rag_instance


PROMPT = """
你是一个帮助用户解答关于PCB缺陷检测系统问题的助手。

你可以调用工具，工具是真实生效的，用法如下：
- 需要了解系统当前状态（模型、参数、摄像头、是否在检测）时，调用 get_system_status；
- 用户要求调整检测参数（置信度、最大缺陷数、是否保存、标签/置信度显示、模型）时，
  调用 set_detection_params，只传用户要求修改的字段；
- 用户要求打开/关闭摄像头时，调用 open_camera；
- 用户要求检测图片/文件夹/视频时，调用 run_detection，并尽量在检测完成后用
  get_latest_result 向用户汇报结果细节；
- 用户询问历史记录、可用模型时，分别调用 get_history、list_models、
- 用户要求打开某个文件夹时，调用 open_output_location。

调用规则：
1. 先判断用户意图对应哪个工具；参数不确定时先用 get_system_status / get_history
   等只读工具确认；
2. 工具返回 JSON 字符串，请按其中字段如实回答；工具返回 ok=False 时，把 error
   里的信息转述给用户；
3. 如果工具无法完成用户想要的操作，停止尝试，不要编造结果；
4. 严格遵循提供的知识库回答用户的知识性问题，如果知识库没有，回答不知道；
5. 在保证问题回答充分的情况下，回答尽量简洁干练。
"""


class AnswerAgent:
    def __init__(self, api_key: str = "", model_name: str = "",
                 bridge: Optional[ToolBridge] = None):
        self.API_KEY = api_key
        self.BASE_URL = ""
        self.MODEL_NAME = model_name.lower()
        self.bridge = bridge
        self.model = None
        self.agent = None

    def url_chooser(self):
        if "deepseek" in self.MODEL_NAME:
            self.BASE_URL = "https://api.deepseek.com/v1"
            return
        if "gpt" in self.MODEL_NAME:
            self.BASE_URL = "https://api.gpt-data.com/v1/"
            return

    def init_agent(self):
        self.url_chooser()
        self.model = init_chat_model(
            model=self.MODEL_NAME,
            api_key=self.API_KEY,
            model_provider="deepseek",
            extra_body={"thinking": {"type": "disabled"}}   # v4 默认开思考，必须显式关闭，否则工具调用轮报 400
        ) if "deepseek" in self.MODEL_NAME else init_chat_model(
            model=self.MODEL_NAME,
            model_provider="OpenAI",
            api_key=self.API_KEY,
            base_url=self.BASE_URL,
        )

        self.agent = create_agent(
            model=self.model,
            system_prompt=PROMPT,
            tools=build_tools(self.bridge),
            checkpointer=checkpointer,
            middleware=[
                mids.summarizer(self.model, 10),
                mids.tool_selector(self.model),
                mids.check_system_status
            ]
        )

    def reply(self, question: str = ""):
        question_o = question

        # RAG 检索（惰性单例 + 降级：检索失败不影响正常对话）
        context = ""
        rag = _get_rag()
        if rag is not None:
            try:
                context = rag.generate_context(question)
            except Exception as e:  # noqa: BLE001
                print(f"[RAG] 检索失败，跳过知识库: {e}")
        if context:
            question = "问题:\n" + question + "\n\n知识库：\n" + context

        try:
            response = self.agent.invoke({
                "messages": [
                    {"role": "user", "content": question}
                ]
            },
            config = config)

            print(f"\n\n模型的对于'{question_o}'的回复结果具体如下：\n")
            from rich import print as rprint
            rprint(response)
            print("\n\n")

            return response["messages"][-1].content
        finally:
            # 防御：释放本轮可能残留的挂起任务（如超时未返回的检测调用）
            if self.bridge is not None:
                self.bridge.cancel_all()


# if __name__ == "__main__":
#     import json
#     from pathlib import Path
#
#     info = json.loads((Path(__file__).resolve().parents[1] / "history" / "model_info.json")
#                       .read_text(encoding="utf-8"))
#     agent = AnswerAgent(api_key=info["api_key"], model_name=info["model_name"])
#     agent.init_agent()
#     print(agent.reply("你好, 一句话介绍你自己"))
