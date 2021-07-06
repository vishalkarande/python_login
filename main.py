from flask import Blueprint, render_template
from flask import Flask, render_template, url_for, session, request, flash, redirect
import mysql.connector
main = Blueprint("main", __name__)

# connect to test database with table login
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
mycursor = mydb.cursor()

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
            print(r)
            p = r[0]
            count = mycursor.rowcount
            print(count)
            if count == 1:
                session["name"] = p[1]
                session["email"] = p[2]
                print(session)
                return render_template('test.html')
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
            # mycursor.close()
            flash("Registration success", "success")
            return render_template('login.html')
        except Exception as error:
            flash("Error Occoured,please try later", "danger")
            return render_template('registration.html')


# logout

@main.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')
