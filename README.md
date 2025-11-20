# Interview Evaluation System - Troogue Assignment

A two-service modular backend application designed to manage candidate interviews, store answers (including file uploads), automatically evaluate completed interviews, and provide an integrated dashboard for results.

This system demonstrates concepts including:

* Microservice-style separation of concerns

* Inter-service communication (Flask → FastAPI)

* Relational data modeling

* ORM-based DB access (SQLAlchemy)

* Request handling, file uploads, and evaluation logic

## System Overview

This system consists of three main components:

### 1. Flask Service (Port 5001)

Responsible for all interview workflow operations, including:

* Creating candidates

* Creating interviews

* Fetching dynamically loaded questions

* Accepting and storing text answers

* Accepting and storing file uploads

* Marking the interview as completed

* Displaying a full dashboard (candidate → answers → result)

It handles every user-facing function.

### 2. FastAPI Service (Port 8000)

Responsible for the evaluation of:

* Individual answers

* Complete interview results

* When an interview is marked “completed”, Flask automatically calls FastAPI to:

* Fetch all answers for the interview

* Run evaluation logic (dummy scoring rules or LLM-based scoring)

* Store the score + feedback inside interview_results table

FastAPI is designed to be stateless and purely functional: it receives data, evaluates, and updates the database.

### 3. PostgreSQL Database

* Stores all system data:

* Candidates

* Interviews

* Questions

* Answers (text/file)

* Evaluation results

Both Flask and FastAPI connect to the same database via SQLAlchemy ORM.

## Architectural Flow (End-to-End)

Below is exactly what happens at runtime:

### Step 1 — Interview Creation (Flask)

The user creates a new interview with:

```

candidate_name  
email  
phone  
skill

```
Flask:

* Inserts candidate → candidates

* Inserts interview → interviews (FK → candidates.id)

* Returns interview_id

### Step 2 — Fetch Questions (Flask)

Flask loads questions from interview_questions filtered by skill.
These are static database entries.

### Step 3 — Submit Answers (Flask)

Supports:

* Plain text answers

* File uploads

* Flask stores answers in:

* interview_answers.text_answer

* interview_answers.file_path

Files are stored in:

```

flask_app/uploads/

```

### Step 4 — Complete Interview → Trigger FastAPI

When interview is marked completed:

```

PUT /interviews/<id>/complete

```

Flask:

* Updates interview status → “completed”

* Automatically sends request to FastAPI:

```

POST FASTAPI_URL/evaluate/interview/<id>

```
### Step 5 — FastAPI Performs Evaluation

FastAPI:

* Loads all answers for the interview

* Generates score (heuristic or LLM-driven)

* Generates feedback

* Stores result in interview_results

FastAPI returns:

```

{"message": "Interview evaluated", "score": <value>}

```

### Step 6 — Full Interview Dashboard (Flask)

Flask returns a consolidated JSON:

* Candidate info

* All answers

* File paths

* Final score

* Evaluation feedback

This provides a complete overview.

## Project Structure Explained

```

troogue_assignment/

```
#### flask_app/

Handles interview lifecycle.

```

app.py                  → entry point
routes/interviews.py    → interview creation, questions, dashboard
routes/answers.py       → text input + file uploads
models/models.py        → ORM models
utils/db.py             → SQLAlchemy engine + SessionLocal
uploads/                → uploaded files

```
#### fastapi_app/

Handles scoring.

```

main.py                 → API endpoints
evaluator.py            → scoring logic
models/models.py        → ORM models
utils/db.py             → database session

```

#### database/schema.sql

* Creates PostgreSQL tables.

#### requirements.txt

* All dependencies.

#### .env

* Environment variables for DB and FastAPI.

## Prerequisites

Install:

```

Python 3.11+

PostgreSQL 14+

pip / virtualenv

```

## Environment Setup

```

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Database Setup

Start PostgreSQL:

```

psql postgres
CREATE DATABASE interviewdb;
\c interviewdb
\i database/schema.sql;

```

#### Verify:

```

\dt

```

**Tables should appear.**

## Environment Variables

Create `.env`:

```

DATABASE_URL=postgresql://<user>:<pass>@localhost:5432/interviewdb
FASTAPI_URL=http://127.0.0.1:8000

```

## Running Services

#### Start FastAPI:

```

cd fastapi_app

```
```

uvicorn main:app --reload --port 8000

```

#### Start Flask:

```

cd flask_app

```

```

python app.py

```

## End-to-End Testing (cURL Commands)

### 1. Create interview

```

curl -X POST http://localhost:5001/interviews/create \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "email": "john@example.com",
    "phone": "99999",
    "skill": "python"
  }'

```

### 2. Get questions

```

curl http://localhost:5001/interviews/6/questions

```

### 3. Submit text answer

```

curl -X POST http://localhost:5001/answers/create \
  -F "interview_id=6" \
  -F "question_id=1" \
  -F "answer_text=List comprehensions allow concise list creation."

```

### 4. Submit the answer with the file

```

curl -X POST http://localhost:5001/answers/create \
  -F "interview_id=6" \
  -F "question_id=2" \
  -F "answer_text=Here is my file answer" \
  -F "file=@sample.txt"

```
### 5. Mark interview as complete → triggers FastAPI

```

curl -X PUT http://localhost:5001/interviews/6/complete

```

### 6. Interview dashboard
```

curl http://localhost:5001/interviews/6

```

## What This Project Demonstrates

### This project clearly showcases:

* Backend Engineering Skills

* Clean REST API design

* Microservices communication

* Python-based backend frameworks (Flask + FastAPI)

* End-to-end request lifecycle handling

* Database Engineering

* Proper relational schema

* Foreign key management

* ORM usage (SQLAlchemy)

* SQL querying and debugging

* System Design

* Decoupled architecture

* Extensible scoring engine

* Modular deployment-ready structure
