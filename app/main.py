"""
程序的启动入口，实现前后端连接
"""
from fastapi import FastAPI,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from RAG.chroma_db import vector_store
import datetime
import json
import os
from agent.agent import agent
from graph.session_memory import get_session_state
from graph.graph import app_graph

# 创建 FastAPI 实例
app = FastAPI(title="网购客服检索系统")

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "app", "Web", "templates")
LOG_DIR = os.path.join(BASE_DIR, "app", "logs")

print(f"模板目录: {TEMPLATES_DIR}")  # 调试信息
print(f"日志目录: {LOG_DIR}")  # 调试信息

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# 定义请求体模型
class QuestionRequest(BaseModel):
    question: str
    session_id: str
    k: int = 1  # 默认返回1条答案
    merge_answers: bool = True

# 日志文件
LOG_FILE = os.path.join(LOG_DIR, "user_questions.log")
os.makedirs(LOG_DIR, exist_ok=True)

# 日志函数
def log_question(question, answers):
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "question": question,
        "answers": answers
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# 检索函数
def ask_user(query, k=3,merge_answers= True):
    results = vector_store.similarity_search(query, k=k)
    answers = [res.metadata["answer"] for res in results]
    if merge_answers:
        merged = "；".join(answers)  # 用中文分号连接多条答案
        return [merged]
    else:
        return answers

# API 路由
@app.post("/ask")
def langgraph_ask(req: QuestionRequest):
    state=get_session_state(req.session_id) # 获取当前会话状态
    state['question']=req.question
    state['session_id']=req.session_id
    res=app_graph.invoke(state)
    answer=res.get("answer","抱歉，我无法回答这个问题👀")
    state["answer"]= answer
    log_question(req.question, [answer])
    return {"question": req.question, "answers": [answer]}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', host="0.0.0.0", port=8000, reload=True)