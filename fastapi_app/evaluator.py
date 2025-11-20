from .models.models import InterviewAnswer, InterviewResult
from .utils.db import SessionLocal

def evaluate_answer(answer_text: str):
    # Dummy scoring logic
    score = len(answer_text.split()) % 10
    feedback = "Auto-evaluated response"

    return {
        "score": score,
        "feedback": feedback
    }


def evaluate_interview(interview_id: int):
    db = SessionLocal()

    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.interview_id == interview_id
    ).all()

    # No answers submitted
    if not answers:
        result = InterviewResult(
            interview_id=interview_id,
            score=0,
            feedback="No answers submitted"
        )
        db.add(result)
        db.commit()
        return {"message": "Interview evaluated", "score": 0}

    # FIXED: use text_answer (correct DB column)
    total_score = sum(len(a.text_answer.split()) % 10 for a in answers)

    # Remove old result if exists
    existing = db.query(InterviewResult).filter(
        InterviewResult.interview_id == interview_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    # Save fresh evaluation
    result = InterviewResult(
        interview_id=interview_id,
        score=total_score,
        feedback="Overall performance evaluated successfully."
    )

    db.add(result)
    db.commit()

    return {"message": "Interview evaluated", "score": total_score}
