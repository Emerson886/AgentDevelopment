
from datetime import datetime
from typing import Any

from langchain.agents.middleware import (
    SummarizationMiddleware, ModelCallLimitMiddleware,
    LLMToolSelectorMiddleware, before_model)
from langchain.agents.middleware.types import StateT
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.runtime import Runtime
from langgraph.typing import ContextT


def summarizer(model, messages_limit=10):
    """总结历史，model传入模型，messages_limit限制保留最近消息数"""
    mid = SummarizationMiddleware(
        model=model,
        trigger=[{"tokens" : 5000, "messages" : 5},
                 {"tokens": 1000, "messages" : 10}
                 ],
        keep=("messages", messages_limit),
        summary_prompt="请总结以下对话，保留关键信息: \n\n{messages}\n\n摘要:"
    )
    return mid

# def call_limit(limit : int = 5):
#     mid = ModelCallLimitMiddleware(
#         thread_limit=limit,
#         exit_behavior="end"
#     )
#
#     return mid

def tool_selector(model):
    mid = LLMToolSelectorMiddleware(
        model=model,
        max_tools=5,
    )
    return mid


@before_model(can_jump_to=["tools"])
def check_system_status(state: StateT, runtime: Runtime[ContextT]) -> dict[str, Any] | None:
    text = state["messages"][-1].content
    if isinstance(text, str) and ("系统参数" in text or "系统状态" in text):
        for message in state["messages"]:
            if isinstance(message, ToolMessage) and 'Name: get_system_status' in  str(message.content):
                return {
                    "messages": message
                }

        fake_tool_call = AIMessage(
            content="fake_tool_call: 查询系统参数状态",
            tool_calls=[{
                "name" : "get_system_status",
                "args" : {},
                "id" : "call_status_" + str(datetime.now()),
            }]
        )

        return {
            "messages": [fake_tool_call],
            "jump_to": "tools"
        }

    return None

