from langchain.agents import create_agent
from app.RAG.llm import llm
from app.tools.tools import check_order
from app.RAG.chroma_db import ask_user_rag as ask_tool

agent=create_agent(
    model=llm,
    tools=[check_order, ask_tool]
)

#需要让agent带着用户问题去调用rag链

if __name__ == '__main__':
    res = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": "订单号 12345 的物流信息是什么？一般多久发货？"}
            ]
        },
        config={
            "configurable": {
                "thread_id": "001"
            }
        }
    )
    for message in res['messages']:
        message.pretty_print()