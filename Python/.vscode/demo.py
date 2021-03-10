from flask import Flask, render_template, request, redirect, url_for, flash, session, sessions
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder='./template')
app.secret_key = "Secret Key"
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import mysql.connector
import pymysql
import re
from pymysql import cursors
from werkzeug.utils import format_string


app = Flask(__name__, template_folder='./template')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Company'
mysql = MySQL(app) 

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
# #   passwd="yourpassword",
#   database="Company"
# )
# mycursor = mydb.cursor()
# mycursor.execute("SELECT * FROM customers")
# myresult = mycursor.fetchall()
# for x in myresult:
#   print(x)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("login.html")
@app.route('/login1',methods=['GET','POST'])
def login():
    loi = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM Account WHERE USER = %s AND PASSWORD = %s', (username, password,))
        account = cursor.fetchone()
        cursor.execute('SELECT TENNV FROM Account WHERE USER = %s AND PASSWORD = %s',(username, password,))
        nv = cursor.fetchone()
        if account:
            session['loggedin'] = True
            flash("Welcome {}".format(nv))
            return redirect(url_for('Index'))
            # Redirect to home page
        else:
            loi = 'Incorrect username/password!'
    return render_template("login.html",loi=loi)


@app.route('/signup',methods=['GET','POST'])
def signup():
    loi =""
    if request.method == 'POST':
        fullname = request.form['username']
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM Account WHERE USER = %s', (username,))
        account = cursor.fetchone()
        if account:
            loi = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            loi = 'Username must contain only characters and numbers!'
        elif not username or not password or not fullname:
            loi = 'Please fill out the form!'
        else:
            cursor.execute('insert INTO  Account(USER, PASSWORD, TENNV) VALUES (%s, %s, %s)',(username,password,fullname,))
            mysql.connection.commit()
            loi = 'Sign up succesfully'
    return render_template("signup.html",loi=loi)
@app.route('/layout')
def layout():
 return render_template("layout.html")
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone
#This is the index route where we are going to
#query on all our employee data
@app.route('/Index')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return render_template("index.html")
 
 
#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
 
        db.session.commit()
        flash("Employee Updated Successfully")
 
        return redirect(url_for('Index'))

#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))
if __name__ == "__main__":
    app.run(debug=True)