"""
根据用户的提问，检索向量库，将检索的结果组装成新的提示词交给大模型返回给用户
"""
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from app.RAG.faq_db import load_faq
from langchain_core.prompts import ChatPromptTemplate
from app.RAG.llm import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

class FixedDashScopeEmbeddings(DashScopeEmbeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """确保传入的是列表格式"""
        if not isinstance(texts, list):
            texts = [texts]
        return super().embed_documents(texts)

    def embed_query(self, text: str) -> list[float]:
        """在 embedding 调用前将字符串包装成列表"""
        if not isinstance(text, str):
            text = str(text)
        result = self.embed_documents([text])
        return result[0] if result else []



# 初始化向量数据库 + embedding
vector_store = Chroma(
    collection_name="faq_collection",
    embedding_function=FixedDashScopeEmbeddings (),
    persist_directory="app.chroma_db"
)

# 加载 FAQ
faq = load_faq()

# 转成 Document
docs = [
    Document(
        page_content=item["question"],
        metadata={"answer": item["answer"]}
    )
    for item in faq
]

# 存入向量库（自动 embedding）
vector_store.add_documents(
    documents=docs,
    ids=["id" + str(i) for i in range(len(docs))]
)

#创建一个字典用来存放用户的对话历史
chat_history = {}

#创建一个获取历史对话的函数
def get_history(session_id: str):#每个session_id对应一个对话
    if session_id not in chat_history:
        chat_history[session_id] = InMemoryChatMessageHistory()
    return chat_history[session_id]



#创建一个带有会话历史的prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        你是一个网购平台智能客服。
        请根据以下系统库回答用户问题：{context}
        如果系统库中没有答案，请礼貌回复。
        """
    ),
    ("placeholder","{history}"),
    ("human","{question}")
])

retriever=vector_store.as_retriever(search_kwargs={'k':5})

def format_func(docs):
    if not docs:
        return "无参考资料"
    formatted_parts = []
    for i, doc in enumerate(docs, 1):
        question = doc.page_content
        answer = doc.metadata.get("answer", "未知")
        formatted_parts.append(f"{i}. 问题：{question}\n   答案：{answer}")
    return "\n\n".join(formatted_parts)


base_chain=(
    {"question":RunnablePassthrough(),"context":retriever|format_func}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain=RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="question",
    history_messages_key="history"
)



def ask_user_rag(user_question:str,session_id: str):
    """
    工具函数：根据用户问题，检索向量库，将检索的结果组装成新的提示词交给大模型返回给用户
    """
    session_config={"configurable":{"session_id":session_id}}
    response=rag_chain.invoke({'question':user_question},config=session_config)
    print(response)
    return response







