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
import os
from flask import current_app

staff_page = Blueprint("staff", __name__, static_folder="static", 
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

@staff_page.route('/staff_dashboard')
@role_required('staff')
def staff_dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('staff_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    pass

@staff_page.route("/")
@role_required('staff')
def staff_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('staff_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@staff_page.route('/profile')
@role_required('staff')
def staff_profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute("""SELECT u.*, s.*
                        FROM user u
                        JOIN staffadmin s ON u.user_id = s.user_id
                        WHERE s.user_id = %s""", (session['user_id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('staff_profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@staff_page.route('/edit_profile', methods=['GET', 'POST'])
@role_required('staff')
def edit_profile():
    if 'loggedin' in session:
        cursor = getCursor()
        if request.method == 'POST':
            #Retrieve form data
            staff_id = request.form['staff_id']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            work_phone_number = request.form['phone_number']
            
            cursor.execute("""
                            UPDATE staffadmin SET first_name = %s, last_name = %s, email = %s, work_phone_number = %s
                            WHERE staff_id = %s AND user_id = %s""", 
                            (first_name, last_name, email, work_phone_number, staff_id, session['user_id']))
            flash('Profile successfully updated.', 'success')
            return redirect(url_for('staff.staff_profile'))
    
        cursor.execute("""
                        SELECT u.*, s.*
                        FROM user u
                        JOIN staffadmin s ON u.user_id = s.user_id
                        WHERE s.user_id = %s""", (session['user_id'],))
        user_data = cursor.fetchone()
        if user_data:
            return render_template('staff_edit_profile.html', user_data=user_data)
        else:
            flash('User data not found.')
            return redirect(url_for('staff.staff_profile'))

@staff_page.route('/change_password', methods=['GET', 'POST'])
@role_required('staff')
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
            return redirect(url_for('staff.change_password'))

        # Check if the old password matches
        if not hashing.check_value(user_data['password'], old_password, salt='abcd') or new_password != confirm_password:
            flash('Invalid old password or new passwords do not match.', 'error')
        else:
            # Hash the new password and update it in the database
            hashed_new_password = hashing.hash_value(new_password, salt='abcd')
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_new_password, session['user_id'],))
            flash('Your password has been updated successfully.', 'success')

        return redirect(url_for('staff.staff_profile'))
    return render_template('staff_change_password.html')

@staff_page.route('/view_agronomist_profile')
@role_required('staff')
def view_agronomist_profile():
    cursor = getCursor()
    #Fetch  the list of pests/weeds from the database
    cursor.execute("SELECT * FROM agronomist;")
    agronomist_list = cursor.fetchall()
    return render_template('staff_view_agronomist_profile.html', agronomistList = agronomist_list)

@staff_page.route('/view_pest_directory')
@role_required('staff')
def view_pest_directory():
    cursor = getCursor()
    
    # Fetch the list of pests from the database
    cursor.execute("SELECT * FROM pest_directory WHERE item_type = 'pest';")
    pest_list = cursor.fetchall()

    # Fetch the list of weeds from the database
    cursor.execute("SELECT * FROM pest_directory WHERE item_type = 'weed';")
    weed_list = cursor.fetchall()
    
    return render_template('staff_pest_directory.html', pestList=pest_list, weedList=weed_list)

@staff_page.route('/view_pest_weed_details/<int:agriculture_id>')
@role_required('staff')
def view_pest_weed_details(agriculture_id):
    cursor = getCursor()
    # Fetch details of a specific pest/weed from the database using the item_id
    cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
    pest_details = cursor.fetchone()  # Use fetchone() since you're fetching a single item
    return render_template('staff_view_pest_weed_details.html', item=pest_details)

@staff_page.route('/update_pest_weed_details/<int:agriculture_id>', methods=['GET', 'POST'])
@role_required('staff')
def update_pest_weed_details(agriculture_id):
    cursor = getCursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
        pest_details = cursor.fetchone()
        return render_template('staff_update_pest_weed_details.html', item=pest_details)
    
    elif request.method == 'POST':
        try:
            common_name = request.form.get('common_name')
            scientific_name = request.form.get('scientific_name')
            key_characteristics = request.form.get('key_characteristics')
            biology_description = request.form.get('biology_description')
            impacts = request.form.get('impacts')
            control = request.form.get('control')

            cursor.execute("""
                    UPDATE pest_directory SET 
                    common_name = %s, 
                    scientific_name = %s, 
                    key_characteristics = %s, 
                    biology_description = %s, 
                    impacts = %s, 
                    control = %s
                    WHERE agriculture_id = %s
                """, (common_name, scientific_name, key_characteristics, biology_description, impacts, control, agriculture_id))
            flash('Pest/weed details updated successfully.', 'success')
        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
        return redirect(url_for('staff.view_pest_weed_details', agriculture_id=agriculture_id))
    
@staff_page.route('/add_pest_weed', methods=['GET', 'POST'])
@role_required('staff')
def add_pest_weed():
    cursor = getCursor()
    if request.method == "GET":
        return render_template('staff_add_pest_weed.html')
    elif request.method == "POST":
        try:
            # Retrieve form data
            item_type = request.form.get('item_type')
            common_name = request.form.get('common_name')
            scientific_name = request.form.get('scientific_name')
            key_characteristics = request.form.get('key_characteristics')
            biology_description = request.form.get('biology_description')
            impacts = request.form.get('impacts')
            control = request.form.get('control')
            
            primary_image = request.files.get('primary_image')

            if primary_image and allowed_file(primary_image.filename):
                filename = secure_filename(primary_image.filename)
                save_path = os.path.join(current_app.root_path, current_app.config['/static'], filename)
                primary_image.save(save_path)

            # Insert data into database
            cursor = getCursor()
            cursor.execute("""
                INSERT INTO pest_directory (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control, primary_image)
                VALUES (%s, %s,  %s,  %s,  %s,  %s,  %s, %s)
            """, (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control, filename))
            flash('Pest/weed details added successfully.', 'success')
            # Redirect to the list of guides
            return redirect(url_for('staff.view_pest_directory'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
            return redirect(url_for('staff.add_pest_weed'))

@staff_page.route('/delete_pest_weed/<int:agriculture_id>', methods=['GET', 'POST'])
@role_required('staff')
def delete_pest_weed(agriculture_id):
    cursor = getCursor()
    try:
        # Delete the pest or weed entry from the database
        cursor.execute("DELETE FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
        flash('Pest/weed successfully deleted.', 'success')
    except Exception as e:
        # If there's an error, rollback any changes
        connection.rollback()
        flash('Error deleting pest/weed: ' + str(e), 'error')
    
    # Redirect back to the pest directory page
    return redirect(url_for('staff.view_pest_directory'))

# Example allowed_file function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# http://localhost:5000/logout - this will be the logout page
@staff_page.route('/logout')
@role_required('staff')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   session.pop('role', None)
   # Redirect to login page
   return redirect(url_for('login'))