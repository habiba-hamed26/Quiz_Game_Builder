CREATE TABLE users
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE quizzes
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE

);

CREATE TABLE questions
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL CHECK (correct_option IN ('a', 'b', 'c', 'd')),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
);

CREATE TABLE scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    user_id INTEGER ,
    player_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX idx_scores_quiz ON scores(quiz_id);
CREATE INDEX idx_questions_quiz ON questions(quiz_id);



INSERT INTO users (username, email, password_hash)
VALUES
('admin', 'admin@example.com', 'hashed_password');


INSERT INTO quizzes (title, description, created_by)
VALUES
(
    'Python Basics Quiz',
    'Test your knowledge of Python programming fundamentals.',
    1
),
(
    'General Knowledge Quiz',
    'A fun quiz covering history, science, and geography.',
    1
);


INSERT INTO questions
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(
    1,
    'Which keyword is used to define a function in Python?',
    'function',
    'def',
    'func',
    'define',
    'b'
),
(
    1,
    'Which data type is immutable?',
    'List',
    'Dictionary',
    'Tuple',
    'Set',
    'c'
);

INSERT INTO questions
(quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
VALUES
(
    2,
    'What is the capital of France?',
    'Rome',
    'Madrid',
    'Paris',
    'Berlin',
    'c'
),
(
    2,
    'Which planet is known as the Red Planet?',
    'Earth',
    'Mars',
    'Venus',
    'Jupiter',
    'b'
);