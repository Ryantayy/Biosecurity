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
from agronomist import agronomist_page
from functools import wraps
from flask import flash
from decorators import role_required
from flask import g

app = Flask(__name__)
hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'lemontea'

@app.before_request
def before_request():
    g.hashing = hashing

app.register_blueprint(agronomist_page, url_prefix="/agronomist")

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

def hash_and_update_passwords():
    try:
        cursor = getCursor()
        
        # Fetch all users
        cursor.execute("SELECT user_id, password FROM user")
        users = cursor.fetchall()
        
        for user in users:
            user_id = user['user_id']  # Assuming your cursor returns a dictionary
            plaintext_password = user['password']
            
            # Hash each password
            hashed_password = hashing.hash_value(plaintext_password, salt='abcd')
            
            # Update the database with the hashed password
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_password, user_id))
        
        connection.commit()  # Ensure changes are committed to the database
        print("Passwords have been hashed and updated.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

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
            print(f"Hashed (DB): {password}")
            print(f"Plaintext (Input): {user_password}")
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
                    return redirect(url_for('staff_dashboard'))
                elif session['role'] == 'administrator':
                    return redirect(url_for('admin_dashboard'))
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
        email = request.form['email']
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
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            msg = 'Password must be at least 8 characters long and include letters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)', (username, hashed, email, 'agronomist'))
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

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'update-passwords':
        with app.app_context():
            hash_and_update_passwords()
            print("Passwords updated successfully.")
    else:
        app.run(debug=True)

