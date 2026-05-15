def response_node(state: dict) -> dict:
    return {"answer": state.get("tool_result", "暂无回答")}