from flask import Flask, request, render_template, session, url_for, redirect, flash
from employee import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route('/clerkhome')
def clerkhome():
    if session['desig'] == 'Clerk':
        return render_template("clerkhome.html")
    # return render_template("clerkhome.html", empid=session['clerkid'], desig=session['desig'])



@app.route('/accountdetailsclerk')
def accountdetailsclerk():
    return render_template("accountdetailsclerk.html", empid=session['clerkid'], desig=session['desig'])


@app.route('/showacdetailsclerk', methods=['POST', 'GET'])
def showacdetailsclerk():
    acno = request.form['acno']
    cursor.execute('SELECT *FROM acdetails WHERE AccountNo= %s', (acno,))
    row = cursor.fetchone()
    if row is None:
        flash("Please enter account number correctly")
        return render_template('accountdetailsclerk.html')
    else:
        cursor.execute('select *from customer where SavingsAcno = %s or CurrentAcno = %s', (acno,acno))
        row1 = cursor.fetchone()
        return render_template("accountdetailsclerk.html", acno=row[0], cname=row1[5], balance=row[1], dateopened=row[2], actype=row[3])


@app.route('/editacbalance', methods=['POST', 'GET'])
def editacbalance():
    return render_template("editacbalance.html", empid=session['clerkid'], desig=session['desig'])


@app.route('/addamount', methods=['POST', 'GET'])
def addamount():

    if request.method == 'POST':
        acno = request.form['acno']
        amount = request.form['amount']
        cursor.execute('SELECT *FROM acdetails WHERE AccountNo=%s', (acno,))
        row = cursor.fetchone()
        if row == None:
            flash("Please enter account number correctly")
            return render_template('editacbalance.html')
        elif int(amount) > 50000:
            flash("Cannot deposit more than Rs.50,000")
            return render_template('editacbalance.html')
        elif int(amount) < 0:
            flash("Enter a valid number")
            return render_template('editacbalance.html')
        else:
            prevbalance = row[1]
            cursor.execute('update acdetails set Balance = Balance+%s where AccountNo= %s', (amount, acno))
            conn.commit()
            cursor.execute('SELECT *FROM acdetails WHERE AccountNo=%s', (acno,))
            row = cursor.fetchone()
            return render_template('editacbalance.html', acno=row[0], prevbalance=prevbalance, newbalance=row[1], amount=amount)


@app.route('/reduceramount', methods=['POST', 'GET'])
def reduceamount():
    if request.method == 'POST':
        acno = request.form['acno']
        amount = request.form['amount']
        cursor.execute('SELECT *FROM acdetails WHERE AccountNo=%s', (acno,))
        row = cursor.fetchone()
        if row == None:
            flash("Please enter account number correctly")
            return render_template('editacbalance.html')
        elif (row[1]-1000) <= int(amount):
            flash("Cannot withdraw whole amount, minimum balance Rs.1000 required")
            return render_template('editacbalance.html')
        elif int(amount) > 50000:
            flash("Cannot withdraw more than Rs.50,000")
            return render_template('editacbalance.html')
        elif int(amount) < 0:
            flash("Enter a valid number")
            return render_template('editacbalance.html')
        else:
            prevbalance = row[1]
            cursor.execute('update acdetails set Balance = Balance-%s where AccountNo= %s', (amount, acno))
            conn.commit()
            cursor.execute('SELECT *FROM acdetails WHERE AccountNo=%s', (acno,))
            row = cursor.fetchone()
            return render_template('editacbalance.html', acno=row[0], prevbalance=prevbalance, newbalance=row[1], amount=amount)

@app.route('/allusersclerk')
def allusersclerk():
        # cursor.execute('select *from customer,acdetails where customer.SavingsAcno=acdetails.AccountNo or customer.CurrentAcno=acdetails.AccountNo')
        cursor.execute('select *from customer,acdetails where customer.SavingsAcno=acdetails.AccountNo or customer.CurrentAcno=acdetails.AccountNo group by acdetails.AccountNo')
        row = cursor.fetchall()
        return render_template("listusersclerk.html", row=row)

