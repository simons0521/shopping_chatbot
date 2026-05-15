from langgraph.graph import StateGraph
from langgraph.graph import END
from app.graph.state import AgentState
from app.graph.intent_node import intent_node
from app.graph.tool_router_node import tool_router_node
from app.graph.tool_executor_node import tool_executor_node
from app.graph.response_node import response_node


workflow = StateGraph(AgentState)#创建一个状态图，图中结点都使用AgentState


workflow.add_node("intent_node",intent_node)
workflow.add_node("tool_router_node",tool_router_node)
workflow.add_node("tool_executor_node",tool_executor_node)
workflow.add_node("response_node",response_node)

workflow.set_entry_point("intent_node")
workflow.add_edge("intent_node", "tool_router_node")
workflow.add_edge("tool_router_node", "tool_executor_node")
workflow.add_edge("tool_executor_node", "response_node")
workflow.add_edge("response_node", END)


app_graph=workflow.compile()

