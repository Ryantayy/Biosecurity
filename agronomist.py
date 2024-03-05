from flask import Blueprint
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
from functools import wraps
from flask import flash
from decorators import role_required
from flask import g

agronomist_page = Blueprint("agronomist", __name__, static_folder="static", 
                       template_folder="templates")

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

@agronomist_page.route('/agronomist_dashboard')
@role_required('agronomist')
def agronomist_dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('agronomist_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    pass

@agronomist_page.route("/")
def agronomist_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('agronomist_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@agronomist_page.route('/profile')
def agronomist_profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute("""SELECT s.*, a.*
                        FROM user s
                        JOIN agronomist a ON s.user_id = a.user_id
                        WHERE a.user_id = %s""", (session['user_id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('agronomist_profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@agronomist_page.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'loggedin' in session:
        cursor = getCursor()
        if request.method == 'POST':
            #Retrieve form data
            agronomist_id = request.form['agronomist_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            address = request.form['address']
            phone_number = request.form['phone_number']
            
            cursor.execute("""
                            UPDATE agronomist SET first_name = %s, last_name = %s, email = %s, address = %s, phone_number = %s
                            WHERE agronomist_id = %s AND user_id = %s""", 
                            (first_name, last_name, email, address, phone_number, agronomist_id, session['user_id']))
            flash('Profile successfully updated.')
            return redirect(url_for('agronomist.agronomist_profile'))
    
        cursor.execute("""
                        SELECT s.*, a.*
                        FROM user s
                        JOIN agronomist a ON s.user_id = a.user_id
                        WHERE a.user_id = %s""", (session['user_id'],))
        user_data = cursor.fetchone()
        if user_data:
            return render_template('edit_profile.html', user_data=user_data)
        else:
            flash('User data not found.')
            return redirect(url_for('agronomist.agronomist_profile'))

@agronomist_page.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    hashing = g.hashing
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        cursor = getCursor()
        cursor.execute("SELECT password FROM user WHERE user_id = %s", (session['user_id'],))
        user_data = cursor.fetchone()

        if not user_data:
            flash('User not found.', 'error')
            return redirect(url_for('agronomist.change_password'))

        # Check if the old password matches
        if not hashing.check_value(user_data['password'], old_password, salt='abcd') or new_password != confirm_password:
            flash('Invalid old password or new passwords do not match.', 'error')
        else:
            # Hash the new password and update it in the database
            hashed_new_password = hashing.hash_value(new_password, salt='abcd')
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_new_password, session['user_id'],))
            flash('Your password has been updated successfully.', 'success')

        return redirect(url_for('agronomist.agronomist_profile'))
    return render_template('change_password.html')

@agronomist_page.route('/view_pest_directory')
def view_pest_directory():
    cursor = getCursor()
    #Fetch  the list of pests/weeds from the database
    cursor.execute("SELECT * FROM pest_directory;")
    pest_directory_list = cursor.fetchall()
    return render_template('pest_directory.html', pestDirectoryList = pest_directory_list)

@agronomist_page.route('/view_pest_weed_details/<int:agriculture_id>')
def view_pest_weed_details(agriculture_id):
    cursor = getCursor()
    # Fetch details of a specific pest/weed from the database using the item_id
    cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
    pest_details = cursor.fetchone()  # Use fetchone() since you're fetching a single item
    return render_template('view_pest_weed_details.html', item=pest_details)

# http://localhost:5000/logout - this will be the logout page
@agronomist_page.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   session.pop('role', None)
   # Redirect to login page
   return redirect(url_for('login'))