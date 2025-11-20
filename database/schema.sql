CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    candidate_name VARCHAR(200),
    skill VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ongoing',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE interview_questions (
    id SERIAL PRIMARY KEY,
    skill VARCHAR(100),
    question_text TEXT
);

CREATE TABLE interview_answers (
    id SERIAL PRIMARY KEY,
    interview_id INT REFERENCES interviews(id),
    question_id INT REFERENCES interview_questions(id),
    answer_text TEXT,
    file_path TEXT
);

CREATE TABLE interview_results (
    id SERIAL PRIMARY KEY,
    interview_id INT REFERENCES interviews(id),
    score INT,
    feedback TEXT
);
