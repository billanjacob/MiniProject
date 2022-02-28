from datetime import date

from flask import Flask, request, render_template, session, url_for, redirect, flash
from customer import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route("/home")
def customerhome():
    return render_template("customerhome.html", username=session['username'])
    # return render_template("customerhome.html")


@app.route("/viewcustomerdetails")
def viewcustomerdetails():
    username = session['username']
    cursor.execute('SELECT *from customer WHERE username= %s', (username,))

    row = cursor.fetchone()
    return render_template("customerdetails.html", username=session['username'], cifno=row[0], cname=row[5], sacno=row[3], cacno=row[4], address=row[6], phone=row[7], email=row[8])


@app.route("/accountdetails")
def accountdetails():
    username = session['username']
    cursor.execute('SELECT SavingsAcno,CurrentAcno FROM customer WHERE username= %s', (username,))
    row = cursor.fetchone()
    if row[0] is None:
        cursor.execute('SELECT *FROM acdetails WHERE AccountNo= %s', (row[1],))
        row2 = cursor.fetchone()
        return render_template("accountdetails.html", username=session['username'], acno=row2[0], balance=row2[1], dateopened=row2[2],actype=row2[3], flag=1)
    elif row[1] is None:
        cursor.execute('SELECT *FROM acdetails WHERE AccountNo= %s', (row[0],))
        row2 = cursor.fetchone()
        return render_template("accountdetails.html", username=session['username'], acno=row2[0], balance=row2[1], dateopened=row2[2], actype=row2[3], flag=1)
    else:
        cursor.execute('SELECT *FROM acdetails WHERE AccountNo= %s or AccountNo=%s', (row[0],row[1]))
        row2 = cursor.fetchone()
        row3 = cursor.fetchone()
        return render_template("accountdetails.html", username=session['username'],
        acno1=row2[0], balance1=row2[1], dateopened1=row2[2], actype1=row2[3], acno2=row3[0], balance2=row3[1], dateopened2=row3[2], actype2=row3[3], flag=2)

        #return render_template("accountdetails.html", username=session['username'],
        #acno1=row2[0], balance1=row2[1], dateopened1=row2[2], actype1=row2[3], acno2=row3[0], balance2=row3[1], dateopened2=row3[2], actype2=row3[3], flag=2)


@app.route("/contact")
def contact():
    return render_template("contact.html", username=session['username'])


@app.route("/loanapplication")
def loanapplication():
    return render_template("loanapplication.html", username=session['username'])


@app.route("/loansubmit", methods=['GET', 'POST'])
def loansubmit():
    username = session['username']
    loanamount = request.form['loanamount']
    today = date.today()
    cursor.execute('insert into loan (uname, loanamount, loanstatus, application_date) values (%s,%s,%s,%s)', (username, loanamount, 0, today))
    conn.commit()
    flash("Loan Application Submitted")
    return render_template("loanapplication.html", username=session['username'])


@app.route("/loanstatus")
def loanstatus():
    username = session['username']
    cursor.execute('select *from loan where uname = %s', (username,))
    row = cursor.fetchone()
    if row:
        if row[3] == 0:
            status = 'Pending'
        else:
            status = 'Approved'
        return render_template("loanstatus.html", username=session['username'], appno=row[0], loanamount=row[2], status=status, date=row[4])
    else:
        flash("You have not applied any loan")
        return render_template("loanstatus.html", username=session['username'])


@app.route('/logout')
def customerlogout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.clear()
    # return redirect(url_for('login'))
    return render_template('index.html')
