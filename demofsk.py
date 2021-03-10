from flask.templating import render_template
from flask import Flask, render_template, redirect,url_for,request,flash,session,sessions

from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import pymysql
from pymysql import cursors
from werkzeug.utils import format_string


app = Flask(__name__,template_folder='templates')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Company'
mysql = MySQL(app) 





@app.route('/',methods=['GET','POST'])
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
    sql = 'SELECT TT,USER FROM  Account where USER=%s'
    pa = ("1",)
    cursor.execute(sql,pa)
    ac = cursor.fetchall()

    cursor.close()
    return render_template("home.html",ac=ac)


user1 = {
        'name' : 'Thanh Nhat',
        'email':'banxavi@gmail.com',
        'password':'123'
        }


@app.route('/login1',methods=['GET','POST'])
def login():
    loi = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('SELECT * FROM Account WHERE USER = %s AND PASSWORD = %s', (email, password,))
        account = cursor.fetchone()
       
        if account:
            session['loggedin'] = True
            flash("Welcome {}".format(email))
            return render_template("home.html")
            # Redirect to home page
        else:
            loi = 'Incorrect username/password!'
    return render_template("login.html",loi=loi)
@app.route('/signup')
def signup():
    return render_template("signup.html")
@app.route('/layout')
def layout():
    return render_template("layout.html")

app.run(debug=True)