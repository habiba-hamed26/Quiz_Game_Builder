from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'my_quizGame_app'

def get_db_connection():
    conn = sqlite3.connect('database.db')   
    conn.execute('PRAGMA foreign_keys = ON')        # Enable foreign key constraints
    conn.row_factory = sqlite3.Row                  # Set row factory to return rows as dictionaries
    return conn

#user registration routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash)) # Insert new user into the database
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username or email already exists.')
            return redirect(url_for('register'))
        finally:
            conn.close()
        return redirect(url_for('login')) # Redirect to login page after successful registration

    # If GET request, show registration form
    return render_template('register.html')   

# user login routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password_hash'], password):
            # Store user information in session
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        flash('Invalid username or password.')

    # If GET request, show login form
    return render_template('login.html')

# user logout route
@app.route('/logout')
def logout():
    session.clear() # Clear the session to log out the user
    return redirect(url_for('index'))   # Redirect to the homepage after logout



def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper

# home page that displays all quizzes
@app.route('/')
def index():
    conn = get_db_connection()
    quizzes = conn.execute('SELECT * FROM quizzes ORDER BY created_at DESC').fetchall()     # Fetch all quizzes ordered by newest first
    conn.close()
    return render_template('index.html', quizzes=quizzes)

# Quiz creation route, accessible only to logged-in users
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')

        
        questions = request.form.getlist('question_text')   # Get the list of questions from the form data
        if len(questions) == 0:
            flash('A quiz needs at least one question.')
            return redirect(url_for('create_quiz'))


        conn = get_db_connection()
        # Insert the new quiz into the quizzes table and get its ID
        cur = conn.execute( 'INSERT INTO quizzes (title, description, created_by) VALUES (?, ?, ?)', (title, description, session['user_id']))
        quiz_id = cur.lastrowid

        
        options_a = request.form.getlist('option_a')
        options_b = request.form.getlist('option_b')
        options_c = request.form.getlist('option_c')
        options_d = request.form.getlist('option_d')
        correct = request.form.getlist('correct_option')

        # Insert each question along with its options into the database
        for i in range(len(questions)):
            conn.execute('''INSERT INTO questions
                (quiz_id, question_text, option_a, option_b, option_c, option_d, correct_option)
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (quiz_id, questions[i], options_a[i], options_b[i], options_c[i], options_d[i], correct[i]))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))


    return render_template('create_quiz.html')  # if GET request, show the quiz creation form


# Route to play a quiz, accessible to both logged-in users and guests
@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def play_quiz(quiz_id):
    conn = get_db_connection()
    # Fetch the quiz details along with the creator's username
    quiz = conn.execute('''
        SELECT quizzes.*, users.username AS creator_name
        FROM quizzes
        JOIN users ON quizzes.created_by = users.id
        WHERE quizzes.id = ?
    ''', (quiz_id,)).fetchone()
    questions = conn.execute('SELECT * FROM questions WHERE quiz_id = ?', (quiz_id,)).fetchall()

    if request.method == 'POST':
        #calculate quiz score
        score = 0
        for q in questions:
            selected = request.form.get(f'question_{q["id"]}')
            if selected == q['correct_option']:
                score += 1

        # determine player identity: logged-in user or guest
        if 'user_id' in session:
            user_id = session['user_id']
            player_name = session['username']
        else:
            user_id = None
            player_name = request.form.get('guest_name', 'Guest')

        # Insert the score into the scores table
        conn.execute('''INSERT INTO scores (quiz_id, user_id, player_name, score, total_questions)
                         VALUES (?, ?, ?, ?, ?)''',
                      (quiz_id, user_id, player_name, score, len(questions)))
        conn.commit()
        conn.close()
        return redirect(url_for('result', quiz_id=quiz_id, score=score, total=len(questions)))

    conn.close()
    return render_template('play_quiz.html', quiz=quiz, questions=questions,
                            logged_in='user_id' in session)


# Quiz result route that displays the score after completing a quiz
@app.route('/result/<int:quiz_id>')
def result(quiz_id):
    score = request.args.get('score')
    total = request.args.get('total')
    return render_template('result.html', score=score, total=total, quiz_id=quiz_id)

# Quiz Leaderboard route this displays top scores for a specific quiz
@app.route('/leaderboard/<int:quiz_id>')
def leaderboard(quiz_id):
    conn = get_db_connection()
    #Fetch top 10 unique players by their highest score
    scores = conn.execute('''
        SELECT player_name, MAX(score) as score
        FROM scores
        WHERE quiz_id = ?
        GROUP BY COALESCE(user_id, player_name)
        ORDER BY score DESC
        LIMIT 10
    ''', (quiz_id,)).fetchall()
    conn.close()

    # Prepare data for the leaderboard chart
    labels = [s['player_name'] for s in scores]
    values = [s['score'] for s in scores]
    top3 = scores[:3]
    return render_template('leaderboard.html', labels=labels, values=values, quiz_id=quiz_id, top3=top3)


if __name__ == '__main__':
    app.run(debug=True)