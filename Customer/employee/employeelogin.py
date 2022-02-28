from flask import Flask, request, render_template, session, url_for, redirect, flash
from customer import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template("employeelogin.html")


@app.route('/form_login', methods=['POST', 'GET'])
def form_login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT *FROM employee WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['username'] = record[1]
            #return render_template('customerhome.html')
            return redirect(url_for('employeehome'))

        else:
            flash("Enter correct credentials!!")
            return render_template('employeelogin.html')


