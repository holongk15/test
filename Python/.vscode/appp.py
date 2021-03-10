from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions
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
            return render_template("index.html")
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


app.run(debug=True)