from flask import Flask, request, render_template, session, url_for, redirect, flash
from employee import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template("employeelogin.html")


@app.route('/form_login', methods=['POST', 'GET'])
def form_login():

    if request.method == 'POST':
        empid = request.form['empid']
        password = request.form['password']
        cursor.execute('SELECT *FROM employee WHERE empid=%s AND password=%s', (empid, password))
        record = cursor.fetchone()

        if record:
            session['loggedin'] = True
            session['desig'] = record[4]

            if session['desig'] == 'Clerk':
                # clerk id is saved in variable clerkid
                session['clerkid'] = record[1]
                print(session['clerkid'])
                # return render_template('clerkhome.html', empid=session['empid'], desig=session['desig'])
                return redirect(url_for('clerkhome'))

            elif session['desig'] == 'Asst.Manager':
                # asst.manager id is saved in variable asmid
                session['asmid'] = record[1]
                # return render_template('asstmanagerhome.html', empid=session['asmid'], desig=session['desig'])
                return redirect(url_for('asstmanagerhome'))

        else:
            flash("Enter correct credentials!!")
            return render_template('employeelogin.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('empid', None)
    session.pop('clerkid', None)
    session.pop('asmid', None)
    session.pop('desig', None)
    session['loggedin'] = False

    return redirect(url_for('index'))
    # return render_template('employeelogin.html')


