from flask import Flask, request, render_template, session, url_for, redirect, flash
from employee import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()

CIFno = 0


@app.route('/asstmanagerhome')
def asstmanagerhome():
    return render_template("asstmanagerhome.html", empid=session['asmid'], desig=session['desig'])


@app.route('/loanstatus')
def loanstatus():
    return render_template("asstmanagerhome.html", empid=session['asmid'], desig=session['desig'])


@app.route('/accountdetailasm')
def accountdetailsasm():
    return render_template("accountdetailsasm.html", empid=session['asmid'], desig=session['desig'])


@app.route('/showacdetailsasm', methods=['POST', 'GET'])
def showacdetailsasm():
    acno = request.form['acno']
    cursor.execute('SELECT *FROM acdetails WHERE AccountNo= %s', (acno,))
    row = cursor.fetchone()
    if row is None:
        flash("Please enter account number correctly")
        return render_template('accountdetailsasm.html')
    else:
        cursor.execute('select *from customer where SavingsAcno = %s or CurrentAcno = %s', (acno,acno))
        row1 = cursor.fetchone()
        return render_template("accountdetailsasm.html", acno=row[0], cname=row1[5], balance=row[1], dateopened=row[2], actype=row[3])

    '''
    cname = request.form['cname']
    cifno = search(cname)
    if cifno == -1:
        flash("Please enter name correctly")
        return render_template('accountdetailsasm.html')
    else:
        cursor.execute('select *from customer, acdetails where customer.CIFNo=%s and (acdetails.AccountNo = customer.SavingsAcno or acdetails.AccountNo = customer.CurrentAcno)',(cifno,))
        row = cursor.fetchone()
        return render_template("accountdetailsasm.html", cifno=row[0], acno=row[3], cname=row[5], balance=row[11], dateopened=row[12], actype=row[13])
'''

def search(cname):
        cname = cname.replace(" ", "")
        cursor.execute('SELECT *FROM customer')
        rows = cursor.fetchall()
        for row in rows:
            f = row[5].lower()
            f = f.replace(" ", "")
            s = cname.lower()
            s = s.replace(" ", "")
            if s in f:
                return row[0]   # returns CIFno
        return -1


@app.route('/editcustomer1', methods=['POST', 'GET'])
def editcustomer1():
    return render_template("editcustomer1.html",
                           empid=session['asmid'], desig=session['desig'])


@app.route('/editcustomer2', methods=['POST', 'GET'])
def editcustomer2():
    cname = request.form['cname']
    global CIFno
    CIFno = search(cname)
    if CIFno == -1:
        flash("Please enter name correctly")
        return render_template('editcustomer1.html')
    else:
        cursor.execute('SELECT *FROM customer WHERE CIFNo=%s', (CIFno,))
        row = cursor.fetchone()
        return render_template("editcustomer2.html",
                               empid=session['asmid'], desig=session['desig'], cifno=CIFno, cname=row[5],
                               address=row[6], phone=row[7], email=row[8])


@app.route('/updatecustomer', methods=['POST', 'GET'])
def updatecustomer():

        cname = request.form['cname']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        cursor.execute('update customer set cname=%s, address=%s, phone=%s, email=%s where CIFNo=%s', (cname, address, phone, email, CIFno))
        conn.commit()
        flash("Updated Successfully")
        # return render_template("editcustomer2.html", empid=session['asmid'], desig=session['desig'], cifno=row[0], cname=row[5], address=row[6], phone=row[7], email=row[8])
        return render_template("editcustomer2.html", empid=session['asmid'], desig=session['desig'],cifno=CIFno, cname=cname,
                               address=address, phone=phone, email=email)



@app.route('/disableuser', methods=['POST', 'GET'])
def disableuser():

    if request.method == 'POST':
        cifno = request.form['cifno']
        cursor.execute('SELECT *FROM customer WHERE CIFNo= %s', (cifno,))
        row = cursor.fetchone()
        if row is None:
            flash("Please enter CIF number correctly")
            return render_template('disableuser.html')
        elif not row[1]:
            flash("User doesnot exist")
            return render_template('disableuser.html')
        elif row[9] == 0:
            flash("User already disabled")
            return render_template('disableuser.html')

        else:
            cursor.execute('update customer set status=0 where CIFNo=%s', (cifno,))
            conn.commit()
            cursor.execute('select *from customer where CIFNo=%s', (cifno,))
            row = cursor.fetchone()
            flash("User disabled:")
            return render_template('disableuser.html', cname=row[5])  # cname to show name of disabled/enabled
    else:
        return render_template('disableuser.html')


@app.route('/enableuser', methods=['POST', 'GET'])
def enableuser():

    if request.method == 'POST':
        cifno = request.form['cifno']
        cursor.execute('SELECT *FROM customer WHERE CIFNo= %s', (cifno,))
        row = cursor.fetchone()
        if row is None:
            flash("Please enter CIF number correctly")
            return render_template('disableuser.html')
        elif not row[1]:
            flash("User doesnot exist")
            return render_template('disableuser.html')
        elif row[9] == 1:
            flash("User already enabled")
            return render_template('disableuser.html')
        else:
            cursor.execute('update customer set status=1 where CIFNo=%s',(cifno,))
            conn.commit()
            cursor.execute('select *from customer where CIFNo=%s', (cifno,))
            row = cursor.fetchone()
            flash("User enabled:")
            return render_template('disableuser.html', cname=row[5])    # cname to show name of disabled/enabled
    else:
        return render_template('disableuser.html')


@app.route('/allusers')
def allusers():
        cursor.execute('select *from customer')
        row = cursor.fetchall()
        return render_template("listusersasm.html", row=row)

