from flask import Flask,render_template,request,Response,redirect,url_for,session,flash
import os
from functools import wraps

app = Flask(__name__)
app.secret_key=os.urandom(100)


def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("you need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/kaja')
@login_required
def kajaji():
    return render_template('user_data.html')

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in']=True
            return redirect(url_for('kajaji'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('main_page'))


if __name__ == '__main__':
    app.run(debug=True)
