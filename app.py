from flask import Flask, render_template, url_for, session, request, flash, redirect
import mysql.connector
from functools import wraps
from main import main

app = Flask(__name__)
app.register_blueprint(main, url_prefix="")
# secret key
app.secret_key = "super secret key"


def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
            return render_template('test.html')
        else:
            flash("Please Login", "info")
            return render_template('login.html')
    return decorated_function


def login_check_R(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
            return render_template('test.html')
        else:
            return render_template('registration.html')

    return decorated_function


def getdata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from login")
    r = mycursor.fetchall()
    return r


def admincheck(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        print(session['level'])
        level = 'user'
        if session['level'] == "admin":
            level = session['level']
            data = getdata()
            return f(level, data, *args, **kws)

        else:
            level = session['level']
            data = getdata()
            return f(level, data, *args, **kws)
    return decorated_function


@app.route('/')
@login_check
def login():
    return render_template('login.html')


@app.route('/register')
@login_check_R
def register():
    return render_template('registration.html')


@app.route('/test')
@admincheck
def test(level, data):
    return render_template('test.html', level=level, data=data)


if __name__ == '__main__':
    app.debug = True
    app.run()
