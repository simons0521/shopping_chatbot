"""
定义一个状态池，用来记录当前任务的发展进程
"""
from typing import TypedDict
class AgentState(TypedDict):

    question:str

    intent:str

    answer:str

    session_id:str

    tool_name:str

    tool_result:str