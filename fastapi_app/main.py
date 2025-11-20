from fastapi import FastAPI
from .evaluator import evaluate_answer, evaluate_interview
from .utils.db import SessionLocal
from .models.models import InterviewResult

app = FastAPI()

@app.post("/evaluate/answer")
def evaluate_single_answer(payload: dict):
    answer_text = payload.get("answer_text")
    return evaluate_answer(answer_text)

@app.post("/evaluate/interview/{id}")
def evaluate_full_interview(id: int):
    return evaluate_interview(id)

@app.get("/results/{interview_id}")
def get_result(interview_id: int):
    db = SessionLocal()

    result = db.query(InterviewResult).filter(
        InterviewResult.interview_id == interview_id
    ).first()

    if not result:
        return {"message": "Result not found for interview", "interview_id": interview_id}

    return {
        "interview_id": interview_id,
        "score": result.score,
        "feedback": result.feedback
    }
