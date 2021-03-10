"""
    Created by nguyenvanhieu.vn at 9/16/2018
"""
from flask import Flask, render_template, redirect, url_for, request
 
app = Flask(__name__,template_folder='./template')


@app.route('/', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = s'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('signup.html', error=error)

@app.route('/home')
def home():
    return 'Login success!' 

@app.route('/')    
def index():
    return render_template('index.html')    
# @app.route('/showSignUp')
# def showSignUp():
#     return render_template('signup.html')
# @app.route('/signUp', methods=['GET', 'POST'])
# def signUp():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('home.html', error=error)


# Route for handling the login page logic
# @app.route('/signUp',methods=['POST'])
# def signUp():
 
#     # read the posted values from the UI
#     _name = request.form['inputName']
#     _email = request.form['inputEmail']
#     _password = request.form['inputPassword']

    

if __name__ == '__main__':
    app.run( debug=True)
