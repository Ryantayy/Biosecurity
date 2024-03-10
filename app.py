from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from functools import wraps
from flask import flash
from decorators import role_required
from flask import g
from agronomist import agronomist_page
from staff import staff_page
from admin import admin_page
import os
from flask import current_app

app = Flask(__name__)
hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'lemontea'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


app.register_blueprint(agronomist_page, url_prefix="/agronomist")
app.register_blueprint(staff_page, url_prefix="/staff")
app.register_blueprint(admin_page, url_prefix="/admin")

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor(dictionary=True)
    return dbconn

@app.before_request
def before_request():
    # Make hashing available in g
    g.hashing = hashing

@app.route('/')
def index():
    #Render the home.thml template upon accessing the root URL
    return redirect(url_for('login'))

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account['password']
            if hashing.check_value(password, user_password, salt='abcd'):
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['user_id'] = account['user_id']
                session['username'] = account['username']
                session['role'] = account['role']
                # Redirect user based on role
                if session['role'] == 'agronomist':
                    return redirect(url_for('agronomist.agronomist_dashboard'))
                elif session['role'] == 'staff':
                    return redirect(url_for('staff.staff_dashboard'))
                elif session['role'] == 'admin':
                    return redirect(url_for('admin.admin_dashboard'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)
    pass

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone_number = request.form['phone_number']
        date_joined = datetime.now()
        status = 'active'
        
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}', password):
            msg = 'Password must be at least 8 characters long and mix of character types!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)', (username, hashed, email, 'agronomist'))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (user_id, first_name, last_name, address, email, phone_number, date_joined, status))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
   pass

if __name__ == '__main__':
    app.run(debug=True)

