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
# login Check

def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
            return redirect(url_for("test"))
        else:
            flash("Please Login", "info")
            return render_template('login.html')
    return decorated_function

# login Check Registration page


def login_check_R(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
            return render_template('test.html')
        else:
            return render_template('registration.html')

    return decorated_function


# Admin Check

def admincheck(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'email' in session:
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
        else:
            flash("Please Login", "info")
            return render_template('login.html')
    return decorated_function


def editadmincheck(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        level = 'user'
        print("hello")
        if 'level' in session and session['level'] == "admin":
            level = session['level']
            data = getdata()
            pages = getpage(session["userid"])
            return f(level, data, pages, *args, **kws)
        else:
            print("Second hello")
            flash("Admin Access required", "danger")
            return redirect(url_for("test"))
    return decorated_function

# functions

# Get User Data


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

# Get page Data


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
    json_data = []
    for result in r:
        json_data.append(dict(zip(row_headers, result)))
    r = json.dumps(json_data)
    res = json.loads(r)
    res = res[0]
    return res

# Api

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


# Delete User data and Page records

@main.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    try:
        if 'email' in session and session['level'] == "admin":
            # Delete User Records
            mycursor.execute(
                "DELETE FROM `login` WHERE id='%d'" % id)
            mydb.commit()
            # Delete Page Access Records for User
            mycursor.execute(
                "DELETE FROM `page_access` WHERE u_id='%d'" % id)
            mydb.commit()
            flash("Data Deleted", "danger")
            return redirect(url_for("admin"))
        else:
            flash("Admin Login Required", "danger")
            return redirect(url_for("test"))
    except Exception as error:
        print(error)
        flash("Error Occoured,please try later", "danger")
        return redirect(url_for("test"))


# Edit page Route

@main.route('/edit/<int:id>', methods=['POST', 'GET'])
def edit(id):
    if 'email' in session and session['level'] == "admin":
        # Get User record by ID
        mycursor.execute("select * from login where id='%d'" % id)
        r = mycursor.fetchall()
        val = r[0]
        print(session)

        # Get User Pages record by "u_id"
        mycursor.execute("select * from page_access where u_id='%d'" % id)
        row_headers = [x[0] for x in mycursor.description]
        pages = mycursor.fetchall()
        # Getting data in json format
        json_data = []
        for result in pages:
            json_data.append(dict(zip(row_headers, result)))
        pages = json.dumps(json_data)
        res = json.loads(pages)
        res = res[0]

        print(res)
        return render_template('edit.html', data=r[0], pages=res)
    else:
        flash("Admin Login Required", "danger")
        return redirect(url_for("test"))


# Update User Details and Page Access

@main.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            email = request.form['email']
            user = request.form['user']
            admin = request.form['admin']
            developer = request.form['developer']
            tester = request.form['tester']
            quality = request.form['quality']
            # Update User Records
            mycursor.execute(
                "UPDATE login SET name=%s,email=%s,type=%s WHERE id=%s", (name, email, user, id))
            mydb.commit()
            # Update User Access pages Records
            mycursor.execute(
                "UPDATE page_access SET admin=%s,developer=%s,tester=%s,quality=%s WHERE u_id=%s", (admin, developer, tester, quality, id))
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
