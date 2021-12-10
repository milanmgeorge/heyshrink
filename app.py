from re import X
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
import MySQLdb.cursors
import os
import re
import mysql.connector
from wtforms.fields.html5 import DateField, EmailField

app = Flask(__name__)
app.secret_key = 'your secret key'


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'millenium1998'
app.config['MYSQL_DB'] = 'heyshrink'

mysql = MySQL(app)


@app.route("/")
def startup():
    return render_template('index.html')


@app.route("/index")
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('diary.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'repassword' in request.form and 'first' in request.form and 'last' in request.form and 'DOB' in request.form and 'gender' in request.form and 'password' in request.form and 'email' in request.form:
        first = request.form['first']
        last = request.form['password']
        dob = request.form['DOB']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM users WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not email or not password or not first or not last or not dob or not gender:
            msg = 'Please fill out the form !'
        elif password != repassword:
            msg = 'Enter both the passwords correctly'
        else:
            cursor.execute(
                'INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, % s)', (first, last, dob, gender, email, password, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')


@app.route("/depression")
def depression():
    return render_template('depression.html')


@app.route("/diary")
def diary():
    return render_template('diary.html')


@app.route("/anxiety")
def anxiety():
    return render_template('anxiety.html')


@app.route("/sexualabuse")
def sexualabuse():
    return render_template('sexualabuse.html')


@app.route("/substanceabuse")
def substanceabuse():
    return render_template('substanceabuse.html')


@app.route("/suicideprevention")
def suicideprevention():
    return render_template('suicideprevention.html')


@app.route("/selfharm")
def selfharm():
    return render_template('selfharm.html')


@app.route("/ocd")
def ocd():
    return render_template('ocd.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=80)
