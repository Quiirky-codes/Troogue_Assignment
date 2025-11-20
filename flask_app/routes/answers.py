from flask import Blueprint, request, jsonify
from utils.db import SessionLocal
from models.models import InterviewAnswer
import os

bp2 = Blueprint("answers", __name__)

# Absolute upload path
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)

@bp2.route("/answers/submit", methods=["POST"])
def submit_answer():
    interview_id = request.form.get("interview_id")
    question_id = request.form.get("question_id")
    answer_text = request.form.get("answer_text")

    file_path = None

    if "file" in request.files:
        f = request.files["file"]

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(file_path)

    db = SessionLocal()
    ans = InterviewAnswer(
        interview_id=interview_id,
        question_id=question_id,
        answer_text=answer_text,
        file_path=file_path
    )
    db.add(ans)
    db.commit()

    return jsonify({"message": "Answer saved"})
