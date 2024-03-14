# Import necessary modules from Flask
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash, g, current_app

# Import other required modules
import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from functools import wraps
from decorators import role_required
import os
from werkzeug.utils import secure_filename
from utils import save_image

admin_page = Blueprint("admin", __name__, static_folder="static", 
                       template_folder="templates")

dbconn = None
connection = None

# Function to establish a database connection and return a cursor
def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor(dictionary=True)
    return dbconn

# Function to check if a file's extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Route for the admin dashboard, protected by role
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

# Route for the admin home page, identical to admin_dashboard
@admin_page.route("/")
@role_required('admin')
def admin_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('admin_home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# Route for the admin profile page, displays user account info
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

# Route for editing the admin's profile
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
        # Fetch current user data to pre-fill the form for GET requests
        # If user data not found, redirect back with an error message
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

# Route for changing the admin's password
@admin_page.route('/change_password', methods=['GET', 'POST'])
@role_required('admin')
def change_password():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
     # Handles password change logic, including validation and updating the database
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

# Route for managing user profiles, lists all users with options to edit or delete
@admin_page.route('/manage_user_profile')
@role_required('admin')
def manage_user_profile():
    cursor = getCursor()
    # Fetches lists of users from the database and displays them on the page
    cursor.execute("""SELECT * 
                    FROM agronomist a
                    LEFT JOIN user u ON a.user_id = u.user_id;""")
    agronomist_list = cursor.fetchall()
    cursor.execute("""SELECT * 
                    FROM staffadmin s
                    LEFT JOIN user u ON s.user_id = u.user_id
                    WHERE role = 'staff';""")
    staff_list = cursor.fetchall()
    return render_template('admin_manage_user_profile.html', agronomistList = agronomist_list, staffList = staff_list)

# Route for adding a new user, with form handling for both GET and POST requests
@admin_page.route('/add_user', methods=['GET', 'POST'])
@role_required('admin')
def add_user():
    if request.method == 'GET':
        # Display the form to add a new user
        return render_template('admin_add_user.html')
    elif request.method == 'POST':
        try:
            cursor = getCursor()  
            # Handles adding a new user, including form data processing and database insertion
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
                cursor.execute("UPDATE agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (user_id, first_name, last_name, address, email, phone_number, date_joined, status))
            elif role == 'staff' or role == 'admin':
                cursor.execute("UPDATE staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status))
            flash(f'User successfully added.', 'success')
        except Exception as e:
            flash(f"An error occurred: {e}", 'danger')
        finally:
            cursor.close()
            connection.close()
        return redirect(url_for('admin.manage_user_profile'))

# Routes for editing specific users, handling both displaying the edit form and processing updates
@admin_page.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_user(user_id):
    cursor = getCursor()
    # Handle GET request
    if request.method == 'GET':
        # Fetch the user data from the user table and their role-specific table
        cursor.execute("""SELECT
                        u.user_id AS user_id,
                        u.username AS username,
                        u.password AS password,
                        u.email AS email,
                        u.role AS role,
                        s.staff_id AS staff_id,
                        s.work_phone_number AS work_phone_number,
                        s.hire_date AS hire_date,
                        s.position AS position,
                        s.department AS department,
                        s.status AS status,
                        a.agronomist_id AS agronomist_id,
                        a.address AS address,
                        a.phone_number AS phone_number,
                        a.date_joined AS date_joined,
                        COALESCE(s.first_name, a.first_name) AS first_name,
                        COALESCE(s.last_name, a.last_name) AS last_name
                        FROM user u
                        LEFT JOIN staffadmin s ON u.user_id = s.user_id
                        LEFT JOIN agronomist a ON u.user_id = a.user_id
                        WHERE u.user_id = %s;""", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('admin.manage_user_profile'))
        
        return render_template('admin_edit_user.html', user=user)

    elif request.method == 'POST':
        # Extract the form data
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        status = request.form['status']
        new_role = request.form['role']
        # Determine the current role of the user
        cursor.execute("SELECT role FROM user WHERE user_id=%s", (user_id,))
        current_role = cursor.fetchone()['role']

        # Update common user information
        cursor.execute("UPDATE user SET username=%s, email=%s, role=%s WHERE user_id=%s", (username, email, new_role, user_id))

        if new_role != current_role:
            if current_role == 'staff':
                cursor.execute("DELETE FROM staffadmin WHERE user_id=%s", (user_id,))
            elif current_role == 'agronomist':
                cursor.execute("DELETE FROM agronomist WHERE user_id=%s", (user_id,))

        try:
            # Insert or update new role information
            if new_role == 'staff':
                work_phone_number = request.form.get('work_phone_number')
                hire_date = request.form.get('hire_date')
                department = request.form.get('department')
                position = request.form.get('position')
                cursor.execute("""
                    INSERT INTO staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    first_name=%s, last_name=%s, email=%s, work_phone_number=%s, hire_date=%s, position=%s, department=%s, status=%s
                    """, (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status, 
                            first_name, last_name, email, work_phone_number, hire_date, position, department, status))
            elif new_role == 'admin':
                work_phone_number = request.form.get('work_phone_number')
                hire_date = request.form.get('hire_date')
                department = request.form.get('department')
                position = request.form.get('position')
                cursor.execute("""
                    INSERT INTO staffadmin (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    first_name=%s, last_name=%s, email=%s, work_phone_number=%s, hire_date=%s, position=%s, department=%s, status=%s
                    """, (user_id, first_name, last_name, email, work_phone_number, hire_date, position, department, status, 
                            first_name, last_name, email, work_phone_number, hire_date, position, department, status))
            elif new_role == 'agronomist':
                address = request.form.get('address')
                phone_number = request.form.get('phone_number')
                date_joined = request.form.get('date_joined')
                cursor.execute("""
                    INSERT INTO agronomist (user_id, first_name, last_name, address, email, phone_number, date_joined, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE 
                    first_name=%s, last_name=%s, address=%s, email=%s, phone_number=%s, date_joined=%s, status=%s
                    """, (user_id, first_name, last_name, address, email, phone_number, date_joined, status, 
                            first_name, last_name, address, email, phone_number, date_joined, status))
            flash("User profile updated successfully.", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('admin.manage_user_profile'))

# Route for changing a user's password, with validation and database update logic
@admin_page.route('/change_user_password/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def change_user_password(user_id):
    cursor = getCursor()
    # Change another user's password
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

# Route for deleting a user, with database deletion logic
@admin_page.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])
@role_required('admin')
def delete_user(user_id):
    # Delete a user from the database
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

# Routes for managing pests and weeds, including viewing, adding, editing, and deleting entries
@admin_page.route('/view_pest_directory')
@role_required('admin')
def view_pest_directory():
    cursor = getCursor()
    
    # Fetch the list of pests from the database
    cursor.execute("""SELECT * FROM pest_directory
                   WHERE item_type = 'pest';""")
    pest_list = cursor.fetchall()

    # Fetch the list of weeds from the database
    cursor.execute("""SELECT * FROM pest_directory
                   WHERE item_type = 'weed';""")
    weed_list = cursor.fetchall()

    # Fetch the list of images from the database
    cursor.execute("""SELECT * FROM images
                   WHERE status = 'primary';""")
    image_list = cursor.fetchall()

    image_map = {image['agriculture_id']: image for image in image_list}

    return render_template('admin_pest_directory.html', pestList=pest_list, weedList=weed_list, imageMap = image_map)

@admin_page.route('/view_pest_weed_details/<int:agriculture_id>')
@role_required('admin')
def view_pest_weed_details(agriculture_id):
    cursor = getCursor()
    
    # Fetch details of the specific pest/weed from the database using the agriculture_id
    cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
    pest_detail = cursor.fetchone()  # Use fetchone() to get a single item

    # Fetch all associated images for this agriculture_id
    cursor.execute("SELECT * FROM images WHERE agriculture_id = %s", (agriculture_id,))
    images = cursor.fetchall()  

    return render_template('admin_view_pest_weed_details.html', item=pest_detail, images=images)

# Route for updating pest or weed details
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

# Route for adding a new pest or weed entry
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
            uploaded_file = request.files.get('filename')

            file_name = None
            if uploaded_file and uploaded_file.filename != '':
                if allowed_file(uploaded_file.filename):  # Ensure the file is allowed based on your function's logic
                    file_name = secure_filename(uploaded_file.filename)
                    save_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], file_name)
                    uploaded_file.save(save_path)
                else:
                    flash('Invalid file type.', 'warning')
                    return redirect(request.url)

             # Insert data into the pest_directory table
            cursor.execute("""
                INSERT INTO pest_directory (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (item_type, common_name, scientific_name, key_characteristics, biology_description, impacts, control))
            
            # Get the last insert id to link the image
            agriculture_id = cursor.lastrowid

            if file_name:
                cursor.execute("""
                    INSERT INTO images (agriculture_id, filename, status)
                    VALUES (%s, %s, %s)
                """, (agriculture_id, file_name, 'primary'))

            flash('Pest/weed details added successfully.', 'success')
            return redirect(url_for('admin.view_pest_directory'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
            return redirect(url_for('admin.add_pest_weed'))

@admin_page.route('/manage_images/<int:agriculture_id>', methods=['GET'])
@role_required('admin')
def manage_images(agriculture_id):
    cursor = getCursor()
    # Fetch list of images for the pest/weed
    cursor.execute("""SELECT * FROM images
                   WHERE agriculture_id = %s;""", (agriculture_id,))
    image_list = cursor.fetchall()
    # Fetch common name for display purposes
    cursor.execute("""SELECT common_name FROM pest_directory
                   WHERE agriculture_id = %s;""", (agriculture_id,))
    common_name_result = cursor.fetchone()
    common_name = common_name_result['common_name'] if common_name_result else 'Unknown'
    return render_template('admin_manage_images.html', agriculture_id=agriculture_id, images=image_list, common_name=common_name)

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
                INSERT INTO images (agriculture_id, filename, status)
                VALUES (%s, %s, 'active')
            """, (agriculture_id, filename))
            flash('Image uploaded successfully', 'success')
        except Exception as e:
            flash(f"An error occurred while saving the image: {str(e)}", 'danger')

    else:
        flash('Allowed file types are png, jpg, jpeg, gif', 'warning')

    return redirect(url_for('admin.view_pest_weed_details', agriculture_id=agriculture_id))

@admin_page.route('/delete_image/<int:image_id>')
@role_required('admin')
def delete_image(image_id):
    try:
        cursor = getCursor()
        # Retrieve the filename before deleting the record
        cursor.execute("SELECT filename FROM images WHERE image_id = %s", (image_id,))
        image_record = cursor.fetchone()

        if image_record:
            # Delete the file from the server
            filepath = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], image_record['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)

            # Delete the image record from the database
            cursor.execute("DELETE FROM images WHERE image_id = %s", (image_id,))
            flash('Image deleted successfully', 'success')
        else:
            flash('Image not found', 'warning')
    except Exception as e:
        flash('An error occurred: ' + str(e), 'danger')
    finally:
        return redirect(request.referrer)

@admin_page.route('/set_primary_image/<int:image_id>/<int:agriculture_id>')
@role_required('admin')
def set_primary_image(image_id, agriculture_id):
    try:
        cursor = getCursor()
        # Retrieve agriculture_id for the image
        cursor.execute("SELECT agriculture_id FROM images WHERE image_id = %s", (image_id,))
        result = cursor.fetchone()
        agriculture_id = result['agriculture_id']

        # Reset the status of all images for the item
        cursor.execute("""
            UPDATE images SET status='active'
            WHERE agriculture_id = %s AND status = 'primary'
        """, (agriculture_id,))

        # Set the selected image as primary
        cursor.execute("""
            UPDATE images SET status='primary'
            WHERE image_id = %s
        """, (image_id,))
        flash('Image set as primary successfully.', 'success')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
    
    return redirect(url_for('admin.manage_images', agriculture_id=agriculture_id))

# Route for deleting a pest or weed entry
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


# Route for displaying sources or references page
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