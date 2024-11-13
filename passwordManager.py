from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)


# Database connection
def get_db_connection():
    conn = sqlite3.connect('server_db.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            flash('Username already exists. Please choose a different one.')
            conn.close()
            return redirect(url_for('signup'))
        
        # Hash password and add new user
        hashed_password = generate_password_hash(password, method='sha256')
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()
        flash('Signup successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user and verify password
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            flash('Login successful!')
            return redirect(url_for('vault'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

# Vault route
@app.route('/vault')
def vault():
    if 'user_id' not in session:
        flash('Please log in to access your vault.')
        return redirect(url_for('login'))
    
    # Retrieve stored passwords for the logged-in user
    conn = get_db_connection()
    passwords = conn.execute('SELECT * FROM passwords WHERE user_id = ?', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('vault.html', passwords=passwords)

# Add password route
@app.route('/add', methods=['POST'])
def add_password():
    if 'user_id' not in session:
        flash('Please log in to add passwords.')
        return redirect(url_for('login'))

    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    # Insert new password record
    conn = get_db_connection()
    conn.execute('INSERT INTO passwords (user_id, site, username, password) VALUES (?, ?, ?, ?)',
                 (session['user_id'], site, username, password))
    conn.commit()
    conn.close()
    flash('Password added successfully!')
    return redirect(url_for('vault'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)