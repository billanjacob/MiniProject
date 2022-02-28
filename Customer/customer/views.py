from flask import Flask, request, render_template, session, url_for, redirect, flash
from customer import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route("/login")
def customerlogin():
    return render_template("customerlogin.html")


@app.route("/signin")
def customersignin():
    return render_template("customersignin.html")


@app.route('/form_login', methods=['POST', 'GET'])
def form_login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute('SELECT *FROM customer WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchone()
        print(username)
        print(password)
        print(record)
        if record and (record[9] == 1):
            session['loggedin'] = True
            session['username'] = record[1]
            #return render_template('customerhome.html')
            return redirect(url_for('customerhome'))

        else:
            flash("Enter correct credentials!!")
            return render_template('customerlogin.html')
    else:
        return render_template('customerlogin.html')


@app.route('/form_singin', methods=['POST', 'GET'])
def form_signin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        phone = request.form['phone']

        cursor.execute('SELECT *from customer WHERE phone = %s', (phone, ))
        row = cursor.fetchone()  # row will be empty if wrong phone number

        # for checking if username exists
        cursor.execute('SELECT *from customer WHERE username = %s', (username,))
        duplicate = cursor.fetchone()

        if row == None:
            # wrong phone number
            flash("Please enter correct phone number")
            return render_template('customersignin.html')

        elif row[1]:
            flash("User already exists for this phone number")
            return render_template('customersignin.html')

        elif not len(password) >= 8:
            flash("Password length must be at least 8 characters")
            return render_template('customersignin.html')

        elif len(password) >= 8:
            l = p = d = u = 0
            for i in password:
                # counting lowercase alphabets
                if (i.islower()):
                    l += 1

                # counting uppercase alphabets
                if (i.isupper()):
                    u += 1

                # counting digits
                if (i.isdigit()):
                    d += 1

                # counting the mentioned special characters
                if (i == '@' or i == '$' or i == '_'):
                    p += 1
            if not(l >= 1 and u >= 1 and p >= 1 and d >= 1 and l + p + u + d == len(password)):
                flash("Password should contain an upppercase, lowercase, number and special character")
                return render_template('customersignin.html')
            else:
                print("password valid")

        if duplicate == None:
            cursor.execute('update customer set username = %s, password = %s, status=1 where phone=%s',
                           (username, password, phone))
            conn.commit()
            flash("Registration Successful")
            return redirect(url_for('customerlogin'))

        else:
            flash("Username already exists")
            return redirect(url_for('customersignin'))
    else:
        return redirect(url_for('customersignin'))
