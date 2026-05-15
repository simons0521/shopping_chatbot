"""
定义一个意识探测函数，通过获取state里面的当前的question，
如果question里面涉及订单则更新意图为查询订单，否则更新意图为简单问答
"""
from app.RAG.llm import llm

INTENT_PROMPT="""
你是一个电商客服意图识别器。

用户问题：

{question}

请识别用户意图。

只能返回以下之一：

order
faq
refund
order_list
product_search

不要解释。
"""
def intent_node(state):

    question = state["question"]

    prompt = INTENT_PROMPT.format(

        question=question
    )

    response = llm.invoke(prompt)

    intent = response.content.strip()

    return {

        "intent":intent
    }