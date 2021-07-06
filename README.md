# python_login
Flask is used to create a web application for Login and restration. Authentication is partially done by bootstrap and remaining by python conditional queries.

## Resources Used
    "flask": "^0.2.10",
    "pip": "^0.0.1",
    "python3": "^0.0.1"
    "Bootstrap":"@5.0.2"
    "Xammp":"v3.2.4"
    
   
## Installation 
If using npm, Can pull repository and use following command to install from json file after going to repo directory :
```sh
$ npm i
```
### Python 
```sh
$ npm i python
```
### Flask 
```sh
$ npm i flask
```
### Mysql-Connector 
```sh
$ pip install mysql-connector-python
```
### Bootsrap
Used Bootstrap free open source CDN :
##### CSS
```sh
<link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
      crossorigin="anonymous"
    />
```
##### JS
```sh
<script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
      crossorigin="anonymous"
    ></script>
```

# Run 
Go to repository and run for starting enviornment :

```sh
$ env\Scripts\activate
```
To run web application
```sh
$ flask run
```
## Database Connection, Routes and API calls in app.js
```sh
from flask import Flask, render_template, url_for, session, request, flash, redirect
import mysql.connector

app = Flask(__name__)

# secret key

app.secret_key = "super secret key"

# connect to test database with table login
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
mycursor = mydb.cursor()

# login route


@app.route('/')
def login():
    if 'email' not in session:
        return render_template('login.html')
    else:
        return render_template('test.html')

# login API


@app.route('/loginuser', methods=['POST', 'GET'])
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

# registration Route


@app.route('/register')
def register():
    if 'email' not in session:
        return render_template('registration.html')
    else:
        return render_template('test.html')

# registration API


@app.route('/user_register', methods=['POST', 'GET'])
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

# Logout API


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.run()

```

# Database 
Use sql Database file named ***"test.sql"*** can be found in sql folder. "test.sql" file is needed to be imported in phpmyadmin or mysql application in order to connect and be live while running application.
