from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d


app = Flask(__name__)
app.secret_key = 'passwordManagerKey'  #random key

# Database connection
def get_db_connection():
    conn = sqlite3.connect('server_db.db')
    conn.row_factory = sqlite3.Row
    return conn

def obscure(data: bytes) -> bytes:
    return b64e(zlib.compress(data, 9))

def unobscure(obscured: bytes) -> bytes:
    return zlib.decompress(b64d(obscured))


# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # Check if the form is submitted
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Login WHERE username = ?', (username,)).fetchone()
        
        # Check if the username already exists
        if user:
            flash('Username is already taken.', 'error')  # Flash error message
            conn.close()
            return redirect(url_for('signup'))  # Redirect back to signup page to try again

        # If username is unique, hash the password and add the user to the database
        hashed_password = generate_password_hash(password, method='sha256')
        conn.execute('INSERT INTO Login (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Signup successful! Please log in.', 'success')  # Flash success message
        return redirect(url_for('login'))  # Redirect to the login page after signup

    return render_template('signup.html')  # Render signup form

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Check if the form is submitted
        username = request.form['username']
        password = request.form['password']

        # Fetch user and verify password
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Login WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user:  # User exists
            if check_password_hash(user['password'], password):  # Password is correct
                session['userID'] = user['id']
                flash('Login successful!', 'success')
                return redirect(url_for('vault'))  # Redirect to the vault page
            else:  # Password is incorrect
                flash('Invalid username or password.', 'error')  # Flash error message for wrong password
        else:  # Username not found
            flash('Username not found. Please try again.', 'error')  # Flash error message for non-existent username

    return render_template('login.html')

# Vault route
@app.route('/vault')
def vault():
    if 'userID' not in session:
        flash('Please log in to access your vault.')
        return redirect(url_for('login'))
    
    # Retrieve stored passwords for the logged-in user
    conn = get_db_connection()
    passwords = conn.execute('SELECT * FROM Vault WHERE userID = ?', (session['userID'],)).fetchall()
    conn.close()
    return render_template('vault.html', passwords=passwords)

# Add password route
@app.route('/add', methods=['POST'])
def add_password():
    if 'userID' not in session:
        flash('Please log in to add passwords.')
        return redirect(url_for('login'))

    website = request.form['website']
    username = request.form['username']
    password = obscure(bytes(request.form['password'], 'ASCII'))

    # Insert new password record
    conn = get_db_connection()
    conn.execute('INSERT INTO Vault (userID, website, username, password) VALUES (?, ?, ?, ?)',
                 (session['userID'], website, username, password))
    conn.commit()
    conn.close()
    flash('Password added successfully!')
    return redirect(url_for('vault'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('userID', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/show', methods=['GET'])
def show_website(website):
    if 'userID' not in session:
        flash('Please log in to add passwords.')
        return redirect(url_for('login'))

    conn = get_db_connection()
    conn.execute('SELECT * FROM Vault WHERE userID = ? and website = ?', (session['userID'], website ))



if __name__ == '__main__':
    app.run(debug=True)

