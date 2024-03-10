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
from werkzeug.utils import secure_filename
from flask import current_app
from utils import save_image

admin_page = Blueprint("admin", __name__, static_folder="static", 
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@admin_page.route('/admin_dashboard')
@role_required('admin')
def admin_dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('admin_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    pass

@admin_page.route("/")
@role_required('admin')
def admin_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('admin_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@admin_page.route('/profile')
@role_required('admin')
def admin_profile():
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
        return render_template('admin_profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@admin_page.route('/edit_profile', methods=['GET', 'POST'])
@role_required('admin')
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
            return redirect(url_for('admin.admin_profile'))
    
        cursor.execute("""
                        SELECT u.*, s.*
                        FROM user u
                        JOIN staffadmin s ON u.user_id = s.user_id
                        WHERE s.user_id = %s""", (session['user_id'],))
        user_data = cursor.fetchone()
        if user_data:
            return render_template('admin_edit_profile.html', user_data=user_data)
        else:
            flash('User data not found.')
            return redirect(url_for('admin.admin_profile'))

@admin_page.route('/change_password', methods=['GET', 'POST'])
@role_required('admin')
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
            return redirect(url_for('admin.change_password'))

        # Check if the old password matches
        if not hashing.check_value(user_data['password'], old_password, salt='abcd') or new_password != confirm_password:
            flash('Invalid old password or new passwords do not match.', 'danger')
        else:
            # Hash the new password and update it in the database
            hashed_new_password = hashing.hash_value(new_password, salt='abcd')
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_new_password, session['user_id'],))
            flash('Your password has been updated successfully.', 'success')

        return redirect(url_for('admin.admin_profile'))
    return render_template('admin_change_password.html')

@admin_page.route('/manage_user_profile')
@role_required('admin')
def manage_user_profile():
    cursor = getCursor()
    #Fetch  the list of pests/weeds from the database
    cursor.execute("""SELECT * 
                    FROM agronomist a
                    LEFT JOIN user u ON a.user_id = u.user_id;""")
    agronomist_list = cursor.fetchall()
    cursor.execute("""SELECT * 
                    FROM staffadmin s
                    LEFT JOIN user u ON s.user_id = u.user_id
                    WHERE position = 'staff';""")
    staff_list = cursor.fetchall()
    return render_template('admin_manage_user_profile.html', agronomistList = agronomist_list, staffList = staff_list)

@admin_page.route('/add_user', methods=['GET', 'POST'])
@role_required('admin')
def add_user():
    if request.method == 'GET':
        # Display the form to add a new user
        return render_template('admin_add_user.html')
    elif request.method == 'POST':
        try:
            cursor = getCursor()  
            # Extract form data common to both roles
            role = request.form['role']
            username = request.form['username']
            raw_password = request.form['password']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            address = request.form['address']
            phone_number = request.form.get('phone_number') 
            date_joined = request.form.get('date_joined')
            status = request.form.get('status') 
            work_phone_number = request.form.get('work_phone_number')
            hire_date = request.form.get('hire_date')
            position = request.form.get('position')
            department = request.form.get('department')
            
            from app import hashing
            # Hash the password
            hashed_password = hashing.hash_value(raw_password, salt='abcd')
            
            # Check if username or email already exists
            cursor.execute("SELECT * FROM user WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                flash('Username or email already exists.', 'danger')
                return redirect(url_for('admin.add_user'))
            
            # Insert the new user into the database with their role
            cursor.execute("INSERT INTO user (username, password, email, role) VALUES (%s, %s, %s, %s)", (username, hashed_password, email, role))
            user_id = cursor.lastrowid
            
            # Insert role-specific details into their respective tables
            if role == 'agronomist':
                cursor.execute("INSERT INTO agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user_id, first_name, last_name, address, email, phone_number, date_joined, status))
            elif role == 'staff' or role == 'admin':
                cursor.execute("INSERT INTO staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status))
            flash(f'User successfully added.', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('admin.manage_user_profile'))

@admin_page.route('/edit_agronomist/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_agronomist(user_id):
    cursor = getCursor()
    
    if request.method == 'GET':
        cursor.execute("""SELECT * 
                        FROM agronomist a 
                        LEFT JOIN user u ON u.user_id = a.user_id 
                        WHERE u.user_id = %s""", (user_id,))
        agronomist = cursor.fetchone()
        if agronomist is None:
            flash("User not found.", "danger")
            return redirect(url_for('manage_user_profile'))
        return render_template('admin_edit_agronomist.html', agronomist = agronomist)

    elif request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        date_joined = request.form.get('date_joined')
        status = request.form.get('status')

        try:
            # Update user table
            cursor.execute(
                """UPDATE user SET username = %s, email = %s WHERE user_id = %s""",
                (username, email, user_id)
            )
            
            # Update agronomist table
            cursor.execute(
                """UPDATE agronomist SET first_name = %s, last_name = %s, address = %s, phone_number = %s, date_joined = %s, status = %s WHERE user_id = %s""",
                (first_name, last_name, address, phone_number, date_joined, status, user_id)
            )
            
            flash("User profile updated successfully.", "success")
        except Exception as e:
            flash("An error occurred: " + str(e), "danger")
        finally:
            cursor.close()

        return redirect(url_for('admin.manage_user_profile'))
    
@admin_page.route('/edit_staff/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_staff(user_id):
    cursor = getCursor()
    
    if request.method == 'GET':
        cursor.execute("""SELECT * 
                        FROM staffadmin s 
                        LEFT JOIN user u ON u.user_id = s.user_id 
                        WHERE u.user_id = %s""", (user_id,))
        staff = cursor.fetchone()
        if staff is None:
            flash("User not found.", "danger")
            return redirect(url_for('manage_user_profile'))
        return render_template('admin_edit_staff.html', staff = staff)

    elif request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        work_phone_number = request.form.get('work_phone_number')
        hire_date = request.form.get('hire_date')
        position = request.form.get('position')
        department = request.form.get('department')
        status = request.form.get('status')

        try:
            # Update user table
            cursor.execute(
                """UPDATE user SET username = %s, email = %s WHERE user_id = %s""",
                (username, email, user_id)
            )
            
            # Update agronomist table
            cursor.execute(
                """UPDATE staffadmin SET first_name = %s, last_name = %s, work_phone_number = %s, hire_date = %s, position = %s, department = %s, status = %s WHERE user_id = %s""",
                (first_name, last_name, work_phone_number, hire_date, position, department, status, user_id)
            )
            
            flash("User profile updated successfully.", "success")
        except Exception as e:
            flash("An error occurred: " + str(e), "danger")
        finally:
            cursor.close()

        return redirect(url_for('admin.manage_user_profile'))

@admin_page.route('/change_user_password/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def change_user_password(user_id):
    cursor = getCursor()
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Ensure the new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('admin.change_user_password', user_id=user_id))

        # Hash the new password
        hashed_new_password = g.hashing.hash_value(new_password, salt='abcd')

        try:
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_new_password, user_id))
            flash('Password successfully updated.', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')

        return redirect(url_for('admin.manage_user_profile', user_id=user_id))
    else:
        cursor.execute("SELECT * FROM user WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        # For GET request, redirect to user edit page or show a custom password change form
        return render_template('admin_change_user_password.html', user=user)


@admin_page.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def delete_user(user_id):
    try:
        cursor = getCursor()
        # Before deleting the user, you might want to delete or update any records associated with the user.
        # For example, if the user has created posts, comments, etc., decide if you want to delete them or assign them to another user.
        cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        flash('User successfully deleted.', 'success')
    except Exception as e:
        flash('Error deleting user: ' + str(e), 'danger')
    finally:
        cursor.close()
    return redirect(url_for('admin.manage_user_profile'))

@admin_page.route('/view_pest_directory')
@role_required('admin')
def view_pest_directory():
    cursor = getCursor()
    
    # Fetch the list of pests from the database
    cursor.execute("SELECT * FROM pest_directory WHERE item_type = 'pest';")
    pest_list = cursor.fetchall()

    # Fetch the list of weeds from the database
    cursor.execute("SELECT * FROM pest_directory WHERE item_type = 'weed';")
    weed_list = cursor.fetchall()
    
    return render_template('admin_pest_directory.html', pestList=pest_list, weedList=weed_list)

@admin_page.route('/view_pest_weed_details/<int:agriculture_id>')
@role_required('admin')
def view_pest_weed_details(agriculture_id):
    cursor = getCursor()
    # Fetch details of a specific pest/weed from the database using the item_id
    cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
    pest_details = cursor.fetchone()  # Use fetchone() since you're fetching a single item
    return render_template('admin_view_pest_weed_details.html', item=pest_details)

@admin_page.route('/upload_image/<int:agriculture_id>', methods=['POST'])
@role_required('admin')
def upload_image(agriculture_id):
    if 'additional_image' not in request.files:
        flash('No file part', 'warning')
        return redirect(request.referrer)

    file = request.files['additional_image']
    if file.filename == '':
        flash('No selected file', 'warning')
        return redirect(request.referrer)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Update the database entry for the pest/weed to include the new image filename
        try:
            cursor = getCursor()
            cursor.execute("""
                UPDATE pest_directory 
                SET additional_image = %s
                WHERE agriculture_id = %s
            """, (filename, agriculture_id))
            flash('Image uploaded successfully', 'success')
        except Exception as e:
            flash(f"An error occurred while saving the image: {str(e)}", 'danger')

    else:
        flash('Allowed file types are png, jpg, jpeg, gif', 'warning')

    return redirect(url_for('admin.update_pest_weed_details', agriculture_id=agriculture_id))

@admin_page.route('/add_image/<int:agriculture_id>', methods=['GET'])
@role_required('admin')
def add_image(agriculture_id):
    return render_template('admin_add_image.html', agriculture_id=agriculture_id)

@admin_page.route('/update_pest_weed_details/<int:agriculture_id>', methods=['GET', 'POST'])
@role_required('admin')
def update_pest_weed_details(agriculture_id):
    cursor = getCursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
        pest_details = cursor.fetchone()
        return render_template('admin_update_pest_weed_details.html', item=pest_details)
    
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
            flash('An error occurred: ' + str(e))
        return redirect(url_for('admin.view_pest_weed_details', agriculture_id=agriculture_id))
    
@admin_page.route('/add_pest_weed', methods=['GET', 'POST'])
@role_required('admin')
def add_pest_weed():
    cursor = getCursor()
    if request.method == "GET":
        return render_template('admin_add_pest_weed.html')
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

            filename = None
            if primary_image and primary_image.filename != '':
                if allowed_file(primary_image.filename):  # Ensure the file is allowed based on your function's logic
                    filename = secure_filename(primary_image.filename)
                    save_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
                    primary_image.save(save_path)
                else:
                    flash('Invalid file type.', 'warning')
                    return redirect(request.url)

            # Insert data into database
            cursor.execute("""
                INSERT INTO pest_directory (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control, primary_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control, filename))
            flash('Pest/weed details added successfully.', 'success')
            # Redirect to the list of guides
            return redirect(url_for('admin.view_pest_directory'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
            return redirect(url_for('admin.add_pest_weed'))

@admin_page.route('/delete_pest_weed/<int:agriculture_id>', methods=['GET', 'POST'])
@role_required('admin')
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
    return redirect(url_for('admin.view_pest_directory'))

@admin_page.route('/sources')
@role_required('admin')
def sources():
    return render_template('admin_sources.html')

# http://localhost:5000/logout - this will be the logout page
@admin_page.route('/logout')
@role_required('admin')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)
   session.pop('role', None)
   # Redirect to login page
   return redirect(url_for('login'))