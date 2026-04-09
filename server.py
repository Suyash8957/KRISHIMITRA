from fastapi import FastAPI
from pydantic import BaseModel
from core.brain import smart_answer
from agents.planner import plan_task
from agents.executor import execute_task

app = FastAPI()

class Query(BaseModel):
    text: str

@app.post("/ask")
def ask(query: Query):
    user_input = query.text

    decision = smart_answer(user_input)

    if decision["type"] in ["data", "web"]:
        response = decision["response"]
    else:
        plan = plan_task(user_input)
        response = execute_task(plan, user_input)

    return {
        "response": response
    }