from flask import Flask, request, render_template, session,url_for, redirect
from customer import app
import mysql.connector as sqldb

conn = sqldb.connect(host='localhost', port='3306', database='db1', user='billan', password='04828')
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/contact_guest")
def contact_guest():
    return render_template("contact_guest.html")


@app.route("/about")
def about():
    return render_template("about.html")

