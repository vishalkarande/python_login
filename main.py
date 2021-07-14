from flask import Blueprint, render_template
from flask import Flask, render_template, url_for, session, request, flash, redirect
import flask
import mysql.connector
from functools import wraps
import json

main = Blueprint("main", __name__)

# connect to test database with table login
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
mycursor = mydb.cursor()


# decorators

def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
            return redirect(url_for("test"))
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


def admincheck(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        level = 'user'
        if session['level'] == "admin":
            level = session['level']
            data = getdata()
            pages = getpage(session["userid"])
            return f(level, data, pages, *args, **kws)

        else:
            level = session['level']
            data = getdata()
            pages = getpage(session["userid"])
            return f(level, data, pages, *args, **kws)
    return decorated_function


# function


def getdata():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from login")
    # row_headers = [x[0] for x in mycursor.description]
    r = mycursor.fetchall()
    # json_data = []
    # for result in r:
    #     json_data.append(dict(zip(row_headers, result)))
    # print(f"json: {json.dumps(json_data)}")
    return r


def getpage(id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select * from page_access where u_id='%d'" % id)
    row_headers = [x[0] for x in mycursor.description]
    r = mycursor.fetchall()
    print(r)
    json_data = []
    for result in r:
        json_data.append(dict(zip(row_headers, result)))
    r = json.dumps(json_data)
    res = json.loads(r)
    res = res[0]
    return res

# login API


@main.route('/loginuser', methods=['POST', 'GET'])
def result():
    try:
        if request.method == 'POST':
            count = 0
            signup = request.form
            username = signup['name']
            password = signup['password']
            if not len(password) >= 8:
                flash("Password must be atleast 8 Characters", "danger")
                return render_template('login.html')
            mycursor.execute("select * from login where email= '" +
                             username+"' and password='"+password+"'")
            r = mycursor.fetchall()
            p = r[0]
            count = mycursor.rowcount

            if count == 1:
                session["name"] = p[1]
                session["email"] = p[2]
                session["level"] = p[4]
                session["userid"] = p[0]
                session["check"] = p

                return redirect(url_for("test"))
            elif count > 1:
                flash("Multiple Users", "danger")
                return render_template('login.html')
            else:
                flash("Not able to Login", "danger")
                return render_template('login.html')
        mydb.commit()
        mycursor.close()
    except Exception as error:
        print(error)
        flash("Error Occoured, Check Id and Password", "danger")
        return render_template('login.html')

# registration API


@main.route('/user_register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            if not len(password) >= 8:
                flash("Password must be atleast 8 Characters", "danger")
                return render_template('registration.html')
            mycursor.execute(
                "INSERT INTO login (name, email, password) VALUES (%s,%s,%s)", (name, email, password))
            mydb.commit()
            l_id = mycursor.lastrowid
            print(l_id)
            dev = 0
            mycursor.execute(
                "INSERT INTO `page_access`( `u_id`, `developer`) VALUES (%s,%s)", (l_id, dev))
            mydb.commit()

            flash("Registration success", "success")
            return render_template('login.html')
        except Exception as error:
            flash("Error Occoured,please try later", "danger")
            return render_template('registration.html')


@main.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        print(type(id))
        mycursor.execute(
            "DELETE FROM `login` WHERE id='%d'" % id)
        mydb.commit()
        flash("Data Deleted", "danger")
        return redirect(url_for("test"))
    except Exception as error:
        print(error)
        flash("Error Occoured,please try later", "danger")
        return redirect(url_for("test"))


@main.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    mycursor.execute("select * from login where id='%d'" % id)
    r = mycursor.fetchall()
    print(r[0])
    return render_template('edit.html', data=r[0])


@main.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            user = request.form['user']
            mycursor.execute(
                "UPDATE login SET name=%s,email=%s,type=%s WHERE id=%s", (name, email, user, id))
            mydb.commit()
            flash("Updated Successfully", "success")
            return redirect(url_for("test"))
        except Exception as error:
            print(error)
            flash("Error Occoured,please try later", "danger")
            return redirect(url_for("test"))

# logout API
@main.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')
