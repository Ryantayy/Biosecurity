# Import necessary modules from Flask
from flask import Blueprint, Flask, render_template, request, redirect, url_for, session, flash, g, current_app

# Import other required modules
import re
from datetime import datetime
import mysql.connector
import connect
from functools import wraps
import os
from werkzeug.utils import secure_filename
from decorators import role_required
from utils import save_image

# Create a Blueprint for staff-related routes
staff_page = Blueprint("staff", __name__, static_folder="static", template_folder="templates")

# Global variables for database connection
dbconn = None
connection = None

# Function to get a cursor for database operations
def getCursor():
    global dbconn
    global connection
    # Establish a database connection and return a cursor
    connection = mysql.connector.connect(user=connect.dbuser, password=connect.dbpass, host=connect.dbhost,
                                         auth_plugin='mysql_native_password', database=connect.dbname, autocommit=True)
    dbconn = connection.cursor(dictionary=True)
    return dbconn

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# Route to staff dashboard
@staff_page.route('/staff_dashboard')
@role_required('staff')
def staff_dashboard():
    # Check if user is logged in
    if 'loggedin' in session:
        # Render staff home page if logged in
        return render_template('staff_home.html', username=session['username'])
    # Redirect to login if not logged in
    return redirect(url_for('login'))

# Route to staff home page
@staff_page.route("/")
@role_required('staff')
def staff_home():
    # Check if user is logged in
    if 'loggedin' in session:
        # Render staff home page if logged in
        return render_template('staff_home.html', username=session['username'])
    # Redirect to login if not logged in
    return redirect(url_for('login'))

# Route to staff profile
@staff_page.route('/profile')
@role_required('staff')
def staff_profile():
    # Check if user is logged in
    if 'loggedin' in session:
        # Fetch user's account info from the database
        cursor = getCursor()
        cursor.execute("""SELECT u.*, s.*
                        FROM user u
                        JOIN staffadmin s ON u.user_id = s.user_id
                        WHERE s.user_id = %s""", (session['user_id'],))
        account = cursor.fetchone()
        # Render staff profile page with account info
        return render_template('staff_profile.html', account=account)
    # Redirect to login if not logged in
    return redirect(url_for('login'))

# Route to edit staff profile
@staff_page.route('/edit_profile', methods=['GET', 'POST'])
@role_required('staff')
def edit_profile():
    # Check if user is logged in
    if 'loggedin' in session:
        cursor = getCursor()
        if request.method == 'POST':
            # Update staff profile details in the database
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
        
        # Fetch staff profile details from the database
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

# Route to change staff password
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
            flash('User not found.', 'danger')
            return redirect(url_for('staff.change_password'))

        # Check if the old password matches
        if not hashing.check_value(user_data['password'], old_password, salt='abcd') or new_password != confirm_password:
            flash('Invalid old password or new passwords do not match.', 'danger')
        else:
            # Hash the new password and update it in the database
            hashed_new_password = hashing.hash_value(new_password, salt='abcd')
            cursor.execute("UPDATE user SET password = %s WHERE user_id = %s", (hashed_new_password, session['user_id'],))
            flash('Your password has been updated successfully.', 'success')

        return redirect(url_for('staff.staff_profile'))
    return render_template('staff_change_password.html')

# Route to view agronomist profile
@staff_page.route('/view_agronomist_profile')
@role_required('staff')
def view_agronomist_profile():
    cursor = getCursor()
    # Fetch the list of agronomists from the database
    cursor.execute("SELECT * FROM agronomist;")
    agronomist_list = cursor.fetchall()
    return render_template('staff_view_agronomist_profile.html', agronomistList=agronomist_list)

# Routes for managing pests and weeds, including viewing, adding, editing, and deleting entries
@staff_page.route('/view_pest_directory')
@role_required('staff')
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

    return render_template('staff_pest_directory.html', pestList=pest_list, weedList=weed_list, imageMap = image_map)

@staff_page.route('/view_pest_weed_details/<int:agriculture_id>')
@role_required('staff')
def view_pest_weed_details(agriculture_id):
    cursor = getCursor()
    
    # Fetch details of the specific pest/weed from the database using the agriculture_id
    cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
    pest_detail = cursor.fetchone()  # Use fetchone() to get a single item

    # Fetch all associated images for this agriculture_id
    cursor.execute("SELECT * FROM images WHERE agriculture_id = %s", (agriculture_id,))
    images = cursor.fetchall()  

    return render_template('staff_view_pest_weed_details.html', item=pest_detail, images=images)

# Route to update details of a specific pest or weed
@staff_page.route('/update_pest_weed_details/<int:agriculture_id>', methods=['GET', 'POST'])
@role_required('staff')
def update_pest_weed_details(agriculture_id):
    cursor = getCursor()
    if request.method == 'GET':
        # Fetch pest/weed details from the database
        cursor.execute("SELECT * FROM pest_directory WHERE agriculture_id = %s", (agriculture_id,))
        pest_details = cursor.fetchone()
        return render_template('staff_update_pest_weed_details.html', item=pest_details)
    
    elif request.method == 'POST':
        try:
            # Retrieve updated pest/weed details from the form
            common_name = request.form.get('common_name')
            scientific_name = request.form.get('scientific_name')
            key_characteristics = request.form.get('key_characteristics')
            biology_description = request.form.get('biology_description')
            impacts = request.form.get('impacts')
            control = request.form.get('control')

            # Update pest/weed details in the database
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

# Route for adding a new pest or weed entry
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
            return redirect(url_for('staff.view_pest_directory'))
        except Exception as e:
            flash('An error occurred: ' + str(e), 'danger')
            return redirect(url_for('staff.add_pest_weed'))
        
@staff_page.route('/manage_images/<int:agriculture_id>', methods=['GET'])
@role_required('staff')
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
    return render_template('staff_manage_images.html', agriculture_id=agriculture_id, images=image_list, common_name=common_name)

@staff_page.route('/upload_image/<int:agriculture_id>', methods=['POST'])
@role_required('staff')
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

    return redirect(url_for('staff.view_pest_weed_details', agriculture_id=agriculture_id))

@staff_page.route('/delete_image/<int:image_id>')
@role_required('staff')
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

@staff_page.route('/set_primary_image/<int:image_id>/<int:agriculture_id>')
@role_required('staff')
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
    
    return redirect(url_for('staff.manage_images', agriculture_id=agriculture_id))

# Route to delete a pest or weed
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

# Route to render sources page
@staff_page.route('/sources')
@role_required('staff')
def sources():
    return render_template('staff_sources.html')

# Route to logout
@staff_page.route('/logout')
@role_required('staff')
def logout():
    # Clear session data and redirect to login page
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))
