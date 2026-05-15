from app.graph.tool_router_node import TOOLS
from app.tools.tools import order_list
import re


def tool_executor_node(state: dict) -> dict:
    tool_name = state.get("tool_name")
    question = state["question"]

    tool = TOOLS.get(tool_name)
    if not tool:
        return {"tool_result": "未找到可用工具"}

    # 简单从问题提取订单号
    ids = re.findall(r"\d+", question)
    order_id = ids[0] if ids else ""

    if tool_name == "check_order":
        result = tool.invoke({"order_id": order_id})
    elif tool_name == "refund_tool":
        result = tool.invoke({"order_id": order_id})
    elif tool_name == "product_search":
        result = tool.invoke({"query": question})
    elif tool_name == "ask_user_rag":
        # ask_user_rag 是普通函数，直接调用
        result = tool(question, session_id=state.get("session_id", "default"))
    elif tool_name == "order_list":
        # order_list 是 StructuredTool，需要调用 invoke
        result = order_list.invoke({})
    else:
        result = "未知工具"

    return {"tool_result": result}
