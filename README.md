# Quiz_Game_Builder


### Quizzly 

Quizzly is a dynamic web application built with Flask and SQLite that allows users to create, share, and play multiple-choice quizzes. Guests can dive right into taking quizzes, while registered users can design custom quizzes and track top scores on an interactive leaderboard.

---

##  Features

* **User Authentication**: Secure registration and login using hashed passwords.
* **Quiz Builder**: Dynamic form allowing logged-in users to add or remove multiple-choice questions.
* **Guest & User Play**: Anyone can take quizzes; guests enter a custom name while logged-in users automatically track scores under their username.
* **Leaderboards & Visualizations**: Top 10 high scores display with a podium and a bar chart powered by **Chart.js**.
* **Database Relational Integrity**: Full foreign-key support via SQLite for cascading deletions of quizzes, questions, and score logs.

---

## 📁 Project Structure

```text
quizzly/
 app.py              # Main Flask application with route handlers
 init_db.py          # Script to initialize the SQLite database
 schema.sql          # Database schema (tables & indexes)
 database.db         # SQLite database file (generated)
 static/
    style.css       # Main stylesheet
 templates/
     base.html       # Shared navigation and layout base
     create_quiz.html# Dynamic quiz creation form
     index.html      # Homepage listing all available quizzes
     leaderboard.html# Top scores display with Chart.js
     login.html      # User login form
     play_quiz.html  # Quiz taking interface
     register.html   # User registration form
     result.html     # Score summary screen
```

---

## setup

### Prerequisites

* **Python 3.x**
* **Flask** & 

### Installation


1. **Install required dependencies:**
   ```bash
   pip install Flask 
   ```

2. **Initialize the database:**
   Run the database initialization script to execute `schema.sql` and set up `database.db`:
   ```bash
   python init_db.py
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Database Schema

* **`users`**: Manages accounts (`username`, `email`, `password_hash`).
* **`quizzes`**: Stores quiz metadata (`title`, `description`, `created_by`).
* **`questions`**: Holds individual question texts, four choices (`option_a` through `option_d`), and the correct answer tag.
* **`scores`**: Records completed games, player identity, scores, and timestamps.