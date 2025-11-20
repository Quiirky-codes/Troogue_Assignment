from flask import Blueprint, request, jsonify
from utils.db import SessionLocal
from models.models import (
    Candidate,
    Interview,
    InterviewQuestion,
    InterviewAnswer,
    InterviewResult
)
import os
import requests


bp = Blueprint("interviews", __name__)


# ----------------------------------------------------
# CREATE INTERVIEW (Candidate → Interview)
# ----------------------------------------------------
@bp.route("/interviews/create", methods=["POST"])
def create_interview():
    data = request.json

    name = data.get("candidate_name")
    email = data.get("email")
    phone = data.get("phone")
    skill = data.get("skill")

    db = SessionLocal()

    # 1. Create candidate
    candidate = Candidate(name=name, email=email, phone=phone)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    # 2. Create interview linked to candidate
    interview = Interview(
        candidate_id=candidate.id,
        skill=skill,
        status="ongoing"
    )
    db.add(interview)
    db.commit()
    db.refresh(interview)

    return jsonify({
        "message": "Interview created",
        "interview_id": interview.id,
        "candidate_id": candidate.id
    })


# ----------------------------------------------------
# GET QUESTIONS FOR AN INTERVIEW
# ----------------------------------------------------
@bp.route("/interviews/<int:id>/questions", methods=["GET"])
def get_questions(id):
    db = SessionLocal()

    interview = db.query(Interview).filter(Interview.id == id).first()
    if not interview:
        return jsonify({"error": "Interview not found"}), 404

    qs = db.query(InterviewQuestion).filter(
        InterviewQuestion.skill == interview.skill
    ).all()

    return jsonify([
        {"question_id": q.id, "question": q.question_text}
        for q in qs
    ])


# ----------------------------------------------------
# COMPLETE INTERVIEW → Trigger FastAPI Evaluation
# ----------------------------------------------------
@bp.route("/interviews/<int:id>/complete", methods=["PUT"])
def complete_interview(id):
    db = SessionLocal()

    interview = db.query(Interview).filter(Interview.id == id).first()
    if not interview:
        return jsonify({"error": "Interview not found"}), 404

    interview.status = "completed"
    db.commit()

    fastapi_url = os.getenv("FASTAPI_URL") + f"/evaluate/interview/{id}"
    requests.post(fastapi_url)

    return jsonify({"message": "Interview sent for evaluation"})


# ----------------------------------------------------
# DASHBOARD – Return Full Interview + Candidate + Answers + Result
# ----------------------------------------------------
@bp.route("/interviews/<int:id>", methods=["GET"])
def get_dashboard(id):
    db = SessionLocal()

    interview = db.query(Interview).filter(Interview.id == id).first()
    if not interview:
        return jsonify({"error": "Interview not found"}), 404

    # Fetch candidate (proper FK usage)
    candidate = db.query(Candidate).filter(Candidate.id == interview.candidate_id).first()

    answers = db.query(InterviewAnswer).filter(
        InterviewAnswer.interview_id == id
    ).all()

    result = db.query(InterviewResult).filter(
        InterviewResult.interview_id == id
    ).first()

    return jsonify({
        "interview": {
            "id": interview.id,
            "skill": interview.skill,
            "status": interview.status,
            "candidate": candidate.name if candidate else None,
            "email": candidate.email if candidate else None,
            "phone": candidate.phone if candidate else None,
        },
        "answers": [
            {
                "question_id": a.question_id,
                "answer": a.answer_text,
                "file": a.file_path
            }
            for a in answers
        ],
        "result": {
            "score": result.score,
            "feedback": result.feedback
        } if result else None
    })
