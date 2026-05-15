"""
创建智能体能调用的工具
"""
# tools.py
from langchain_core.tools import tool
from typing import Dict

# 模拟数据库
ORDERS_DB = {
    "12345": {"status": "已发货", "物流公司": "顺丰", "预计送达": "2026-05-12"},
    "67890": {"status": "处理中", "物流公司": None, "预计送达": None},
    "90123": {"status": "已取消", "物流公司": None, "预计送达": None}
}

@tool
def check_order(order_id: str) -> str:
    """
    工具函数：根据订单号返回订单信息
    """
    order = ORDERS_DB.get(order_id)
    if not order:
        return f"抱歉，未找到订单号 {order_id} 的信息。"

    return (
        f"订单号 {order_id} 状态：{order['status']}。\n"
        f"物流公司：{order['物流公司'] or '未发货'}。\n"
        f"预计送达时间：{order['预计送达'] or '未知'}。"
    )
@ tool
def order_list():
    """
    工具函数：返回所有订单信息
    """
    orders = [
        f"订单号 {order_id} 状态：{order['status']}。\n"
        f"物流公司：{order['物流公司'] or '未发货'}。\n"
        f"预计送达时间：{order['预计送达'] or '未知'}。\n"
        for order_id, order in ORDERS_DB.items()
    ]
    return "\n".join(orders)

@tool
def refund_tool(order_id: str) -> str:
    """
    工具函数：提交退款申请
    """
    return f"订单 {order_id} 的退款申请已提交"

@tool
def product_search(query: str) -> str:
    """
    工具函数：根据查询条件返回商品推荐
    """
    url=f"https://www.example.com/search?q={query}"
    return url