from flask import Flask, render_template, url_for, session, request, flash, redirect
import mysql.connector
from functools import wraps
from main import *
import main as m


app = Flask(__name__)
app.register_blueprint(main, url_prefix="")
# secret key
app.secret_key = "super secret key"


@app.route('/')
@m.login_check
def login():
    return render_template('login.html')


@app.route('/register')
@m.login_check_R
def register():
    return render_template('registration.html')


@app.route('/test')
@m.admincheck
def test(level, data, pages):
    return render_template('test.html', level=level, data=data, pages=pages)


@app.route('/admin')
@m.admincheck
def admin(level, data, pages):
    return render_template('admin.html', level=level, data=data, pages=pages)


@app.route('/developer')
@m.admincheck
def developer(level, data, pages):
    return render_template('developer.html', level=level, data=data, pages=pages)


@app.route('/tester')
@m.admincheck
def tester(level, data, pages):
    return render_template('tester.html', level=level, data=data, pages=pages)


@app.route('/quality')
@m.admincheck
def quality(level, data, pages):
    return render_template('quality.html', level=level, data=data, pages=pages)


@app.route('/contactus')
@m.admincheck
def contactus(level, data, pages):
    return render_template('contactus.html', level=level, data=data, pages=pages)


@app.route('/help')
@m.admincheck
def help(level, data, pages):
    return render_template('help.html', level=level, data=data, pages=pages)


@app.route('/support')
@m.admincheck
def support(level, data, pages):
    return render_template('support.html', level=level, data=data, pages=pages)


if __name__ == '__main__':
    app.debug = True
    app.run()
