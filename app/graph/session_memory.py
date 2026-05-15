"""
定义一个根据会话ID获取当前对话状态state的函数
"""
sessions={}
def get_session_state(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {
            "session_id":"session_id",
            "intent":"",
            "question": "",
            "answer": ""
        }
    return sessions[session_id]