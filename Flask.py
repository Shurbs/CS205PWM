from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('vault'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/vault')
def vault_page():
   return render_template('vault.html')

if __name__ == '__main__':
    app.run(debug=True)