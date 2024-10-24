from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')
        users[username] = hashed_password
        
        flash('User signup success!')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username exists and password is correct
        if username in users and check_password_hash(users[username], password):
            session['user_id'] = username
            flash('Login successful!')
            return redirect(url_for('vault'))  # Redirect to vault or home page
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

# Vault route
@app.route('/vault')
def vault():
    if 'user_id' not in session:
        flash('Please log in to access your vault.')
        return redirect(url_for('login'))

    return render_template('vault.html')

# Route to add a password
@app.route('/add', methods=['POST'])
def add_password():
    if 'user_id' not in session:
        flash('Please log in to add passwords.')
        return redirect(url_for('login'))

    site = request.form['site']
    username = request.form['username']
    password = request.form['password']

    # Here you would save the password securely
    print(f'Site: {site}, Username: {username}, Password: {password}')
    return redirect(url_for('vault'))

if __name__ == '__main__':
    app.run(debug=True)print ("Login // Sign up Script")



     