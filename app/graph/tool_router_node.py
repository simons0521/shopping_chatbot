import re
from app.tools.tools import order_list,check_order,refund_tool,product_search
from app.RAG.chroma_db import ask_user_rag
from app.RAG.llm import llm

TOOLS = {
    "check_order": check_order,
    "refund_tool": refund_tool,
    "product_search": product_search,
    "ask_user_rag": ask_user_rag,
    "order_list": order_list
}

TOOL_ROUTER_PROMPT = """
你是电商客服工具路由器。

用户问题：
{question}

可用工具：
1.check_order - 查询某一个订单，需要订单号
2.refund_tool - 退款，需要订单号
3.product_search - 用户需要你推荐一些商品
4.ask_user_rag - 用户向你询问关于发货、退货、运费、发票、联系客服、退款，售后，账户注销等问题时使用
5.order_list -订单列表，用户想要查看自己所有订单信息时使用

请根据用户问题和意图返回一个工具名，仅返回工具名。
"""

def tool_router_node(state: dict) -> dict:
    question = state["question"]
    intent = state["intent"]
    prompt = TOOL_ROUTER_PROMPT.format(question=question)
    response = llm.invoke(prompt)
    tool_name = response.content.strip()
    return {"tool_name": tool_name}
