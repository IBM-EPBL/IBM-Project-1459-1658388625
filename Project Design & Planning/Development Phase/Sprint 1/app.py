
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)

app.secret_key = 'password'
conn = ibm_db.connect(
    "DATABASE=bludb; HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756; SECURITY=SSL; SSLServerCerrificate=DigiCertGlobalRootCA.crt; UID=jhk48064; PWD=pcsPf5G40FoUexOI",
    '', '')


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        sql = f"select * from user where name='{username}'"
        sql = ibm_db.prepare(conn, sql)
        dt = ibm_db.execute(sql)

        account = ibm_db.fetch_assoc(sql)
        print(account)

        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['NAME']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        sql = f"select * from user where name='{username}'"
        sql = ibm_db.prepare(conn, sql)
        dt = ibm_db.execute(sql)

        account = ibm_db.fetch_assoc(sql)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            sql = f"INSERT INTO  USER VALUES('{username}', '{email}', '{password}', 'user');"
            print(sql)
            sql = ibm_db.prepare(conn, sql)
            dt = ibm_db.execute(sql)

            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)
