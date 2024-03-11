# COMP639 Studio Project – Semester 1 2024
# Individual Assignment
**Name**: Ryan Tay Peng Yeow <br>
**Student ID**: 1157892

## Biosecurity Guide - Web Application Structure:
### Structure Overview:

**Blueprints and Their Roles:** <br>
- **Agronomist Blueprint:** Primarily caters to agronomists by providing access to view and possibly contribute to the pest/weed directory, alongside managing their professional profiles.<br>
- **Staff Blueprint:** Designed for staff users, focusing on the pest/weed directory (view, add, update, delete), uploading images for pest/weed entries, and managing their profiles. It enables staff to contribute to and maintain the pest/weed database. <br>
Agronomist Blueprint: Although not detailed in your submission, it's implied that this blueprint would cater to agronomists' specific functionalities, likely around viewing and possibly contributing to the pest/weed directory, along with managing their professional profiles. <br>
- **Admin Blueprint:** Handles routes and functionalities specific to the administrative role, including user management (add, edit, delete users), pest/weed directory management, and profile management. It serves as a central hub for system oversight and content management.<br>

**Functionality and Data Flow:**<br>
- **User Management:** Admins have the capability to manage user profiles across different roles, including creating new user accounts, editing existing ones, and removing users from the system. This involves interactions with the database to fetch, update, or delete user-related data.<br>
- **Pest/Weed Directory Management:** Both staff and admin roles can manage the pest/weed directory. This includes adding new entries, updating existing ones, uploading images, and deleting entries as needed. The process involves submitting forms, handling file uploads, and performing database transactions to maintain up-to-date and accurate directory information.<br>
- **Profile Management:** Users across all roles have the ability to view and edit their profiles, change their passwords, and log out. This personalization aspect ensures that users can maintain their account details and security settings as per their preferences.<br>

**Technical Considerations:**<br>
- **Session Management:** User sessions are utilized to manage login states and role-based access control. The session data dictate what resources and routes a user can access, ensuring a secure and personalized user experience.<br>

**Security and Access Control**<br>
- **Role-Based Access Control:** Decorators like @role_required enforce access control, ensuring that users can only access routes and functionalities pertinent to their assigned roles.<br>
- **Password Handling:** The hashing module is used for secure password management, involving hashing passwords before storing them in the database and verifying user login attempts.<br>
<p>This structure facilitates a modular and organized approach to developing and expanding the web application, with clear separation of role-based functionalities for admins, staff, and agronomists. <p/>

### Routes & Functions:

App.py
Index/Home ( / ): <br/>
Description: Redirects to the login page. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: The root index redirects users to the login page, acting as a default entry point to the application. <br/><p/>

Login ( /login/ ): <br/>
Description: Handles user authentication and session creation. <br/>
Template: index.html <br/>
Data Passed: User credentials from form. <br/>
Data Relationship: On POST, validates user credentials against the database, creates a session, and redirects to the appropriate dashboard based on role. On GET, displays the login form. <br/><p/>

Register ( /register ): <br/>
Description: Handles new user registration. <br/>
Template: register.html <br/>
Data Passed: New user data from form. <br/>
Data Relationship: On POST, processes the registration form, validates the data, hashes the password, inserts a new user into the database, and commits the transaction. On GET, displays the registration form. <br/><p/>

Logout ( /logout ): <br/>
Description: Ends the user session and redirects to the login page. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: Clears the user's session data to log them out and redirects them to the login page. <br/><p/>

Before Request ( @app.before_request ): <br/>
Description: Prepares certain variables before processing a request. <br/>
Template: N/A <br/>
Data Passed: N/A <br/>
Data Relationship: Attaches the hashing instance to the global object g before handling any requests. <br/><p/>

Staff Blueprint

Staff Dashboard ( /staff_dashboard ): <br/>
Description: Displays the main dashboard for staff users. <br/>
Template: staff_home.html <br/>
Data Passed: Username from session. <br/>
Data Relationship: Directly presents the staff dashboard if the user is logged in and assigned a 'staff' role. Redirects to login otherwise. <br/><p/>

Staff Home ( /staff/ ): <br/>
Description: Duplicate of the staff dashboard, potentially for different staff-related home content. <br/>
Template: staff_home.html <br/>
Data Passed: Username from session. <br/>
Data Relationship: Similar to the staff_dashboard, checks for 'loggedin' session status and renders the staff homepage or redirects to login. <br/><p/>

Staff Profile ( /staff/profile ): <br/>
Description: Displays the profile details of the logged-in staff member. <br/>
Template: staff_profile.html <br/>
Data Passed: Account details from database query. <br/>
Data Relationship: Retrieves the staff user's details from the database and presents them on the profile page if logged in. Redirects to login if not logged in. <br/><p/>

Edit Staff Profile ( /staff/edit_profile ): <br/>
Description: Allows staff to edit their profile information. <br/>
Template: staff_edit_profile.html for GET, redirects on POST. <br/>
Data Passed: Profile data for form pre-filling on GET, updated data on POST. <br/>
Data Relationship: For GET requests, it pre-fills the form with existing user data. For POST requests, it updates the user's profile details in the database. <br/><p/>

Change Staff Password ( /staff/change_password ): <br/>
Description: Allows staff to change their password. <br/>
Template: staff_change_password.html for GET, redirects on POST. <br/>
Data Passed: Old and new passwords from form. <br/>
Data Relationship: Provides a form to change password on GET requests. Validates and updates the password in the database on POST requests. <br/><p/>

View Agronomist Profile ( /staff/view_agronomist_profile ): <br/>
Description: Lists profiles of agronomists for staff to view. <br/>
Template: staff_view_agronomist_profile.html <br/>
Data Passed: List of agronomists from the database. <br/>
Data Relationship: Retrieves and displays agronomist profiles from the database for staff to view. <br/><p/>

View Pest Directory ( /staff/view_pest_directory ): <br/>
Description: Lists pests and weeds for staff to manage. <br/>
Template: staff_pest_directory.html <br/>
Data Passed: Lists of pests and weeds from the database. <br/>
Data Relationship: Fetches and displays pests and weeds entries, allowing staff to perform management tasks like editing and deletion. <br/><p/>

View Pest/Weed Details ( /staff/view_pest_weed_details/int:agriculture_id ): <br/>
Description: Shows detailed information for a specific pest or weed. <br/>
Template: staff_view_pest_weed_details.html <br/>
Data Passed: Details of a single pest or weed from the database. <br/>
Data Relationship: Retrieves and displays detailed information about a particular pest/weed entry based on the provided agriculture_id. <br/><p/>

Upload Additional Image ( /staff/upload_image/int:agriculture_id ): <br/>
Description: Handles the upload of additional images for pests or weeds. <br/>
Template: Redirects after POST <br/>
Data Passed: Uploaded image file. <br/>
Data Relationship: Accepts image uploads and updates the corresponding database entry with the image's filename after saving it to the server. <br/><p/>

Add Image ( /staff/add_image/int:agriculture_id ): <br/>
Description: Renders a form to upload an additional image for a specific pest or weed. <br/>
Template: staff_add_image.html <br/>
Data Passed: agriculture_id for identifying which pest or weed to add an image to. <br/>
Data Relationship: Renders a form that allows staff to upload an additional image for a pest/weed. <br/><p/>

Update Pest/Weed Details ( /staff/update_pest_weed_details/int:agriculture_id ): <br/>
Description: Allows staff to update details of a specific pest or weed. <br/>
Template: staff_update_pest_weed_details.html for GET, redirects on POST. <br/>
Data Passed: Updated pest/weed details from form. <br/>
Data Relationship: For GET requests, pre-fills a form with existing pest/weed details. On POST, updates the database with the new details. <br/><p/>

Add Pest/Weed ( /staff/add_pest_weed ): <br/>
Description: Allows staff to add a new pest or weed to the database. <br/>
Template: staff_add_pest_weed.html for GET, redirects on POST. <br/>
Data Passed: New pest/weed details from form. <br/>
Data Relationship: Provides a form to add a new pest/weed on GET requests. Inserts the new pest/weed into the database on POST requests. <br/><p/>

Delete Pest/Weed ( /staff/delete_pest_weed/int:agriculture_id ): <br/>
Description: Handles the deletion of a specific pest or weed from the database. <br/>
Template: Redirects after POST <br/>
Data Passed: agriculture_id to identify the pest/weed to delete. <br/>
Data Relationship: Deletes the specified pest/weed from the database and redirects to the pest directory. <br/><p/>

Sources ( /staff/sources ): <br/>
Description: Displays the sources or references page for staff. <br/>
Template: staff_sources.html <br/>
Data Passed: None. <br/>
Data Relationship: Renders a static page with sources or references relevant to the staff content. <br/><p/>

Logout ( /staff/logout ): <br/>
Description: Logs out the current staff user and ends their session. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: Clears the staff user's session data and redirects to the login page. <br/><p/>

Admin Blueprint

Admin Dashboard (/admin/admin_dashboard): <br>
Description: Serves the dashboard for administrators after login. <br>
Template: admin_home.html <br>
Data Passed: username from session <br>
Data Relationship: The admin_dashboard route renders the admin_home.html template displaying the admin dashboard. It requires the user to be logged in and have the 'admin' role. <br><p/>

Admin Home (/admin/): <br>
Description: Identical to admin_dashboard, serves as an entry point to admin functions. <br>
Template: admin_home.html <br>
Data Passed: username from session <br>
Data Relationship: The admin_home route is an alternative URL that serves the same admin_home.html template as the admin_dashboard. <br><p/>

Admin Profile (/admin/profile): <br>
Description: Displays the admin's profile information. <br>
Template: admin_profile.html <br>
Data Passed: Account information fetched from database <br>
Data Relationship: Fetches the admin's account details from the database and passes it to the admin_profile.html template. <br><p/>

Edit Profile (/admin/edit_profile): <br>
Description: Allows the admin to update their profile details. <br>
Template: admin_edit_profile.html for GET, redirects to admin_profile on POST <br>
Data Passed: For GET, current user data to pre-fill the form; for POST, updated user data <br>
Data Relationship: Displays the current admin's information on the admin_edit_profile.html template and updates the database with any changes on POST submission. <br><p/>

Change Password (/admin/change_password): <br>
Description: Allows the admin to change their password. <br>
Template: admin_change_password.html <br>
Data Passed: None for GET, form data for POST <br>
Data Relationship: Renders a form to change password on GET request. On POST, validates and updates the new password in the database. <br><p/>

Manage User Profile (/admin/manage_user_profile): <br>
Description: Lists all users with options to edit or delete profiles. <br>
Template: admin_manage_user_profile.html <br>
Data Passed: Lists of agronomists and staff users <br>
Data Relationship: Fetches lists of users from the database and displays them on the page with options to edit or delete. <br><p/>

Add User (/admin/add_user): <br>
Description: Adds a new user to the system. <br>
Template: admin_add_user.html for GET, redirects to manage_user_profile on POST <br>
Data Passed: User data from form on POST <br>
Data Relationship: Renders a form to add a new user and inserts the user into the database on POST submission. <br><p/>

Edit User (/admin/edit_agronomist and /admin/edit_staff): <br>
Description: Routes for editing specific agronomist and staff users, handling both displaying the edit form and processing updates. <br>
Templates: admin_edit_agronomist.html and admin_edit_staff.html for GET, redirects to manage_user_profile on POST <br>
Data Passed: User data to be edited <br>
Data Relationship: Fetches the user's current data, displays it for editing, and updates the database on POST submission. <br><p/>

Change User Password (/admin/change_user_password/int:user_id): <br>
Description: Allows changing another user's password. <br>
Template: admin_change_user_password.html <br>
Data Passed: User ID for whom the password is to be changed <br>
Data Relationship: Renders a form for admin to change a specific user's password and updates the database on POST submission. <br><p/>

Delete User (/admin/delete_user/int:user_id): <br>
Description: Deletes a user from the system. <br>
Template: None, redirects to manage_user_profile <br>
Data Passed: User ID of the user to be deleted <br>
Data Relationship: Removes the user from the database and redirects back to the user management page. <br><p/>

View Pest Directory (/admin/view_pest_directory): <br>
Description: Displays the list of pests and weeds. <br>
Template: admin_pest_directory.html <br>
Data Passed: Lists of pests and weeds <br>
Data Relationship: Fetches the lists of pests and weeds from the database and passes them to the admin_pest_directory.html template. <br><p/>

View Pest/Weed Details (/admin/view_pest_weed_details/int:agriculture_id): <br>
Description: Displays details for a specific pest or weed. <br>
Template: admin_view_pest_weed_details.html <br>
Data Passed: Details of the specific pest or weed <br>
Data Relationship: Fetches the details of a specific pest or weed from the database and displays them on the admin_view_pest_weed_details.html template. <br><p/>

Upload Image (/admin/upload_image/int:agriculture_id): <br>
Description: Handles the uploading of additional images for a pest or weed. <br>
Template: Redirects to update_pest_weed_details on POST <br>
Data Passed: The image file and agriculture_id <br>
Data Relationship: Receives the image upload through POST, saves the file, and updates the database entry for the pest/weed. <br><p/>

Add Image (/admin/add_image/int:agriculture_id): <br>
Description: Renders a form to upload additional images for a pest or weed. <br>
Template: admin_add_image.html <br>
Data Passed: agriculture_id <br>
Data Relationship: Renders the admin_add_image.html template to provide a form for uploading additional images. <br><p/>

Update Pest/Weed Details (/admin/update_pest_weed_details/int:agriculture_id): <br>
Description: Updates the details for a specific pest or weed. <br>
Template: admin_update_pest_weed_details.html for GET, redirects to view_pest_weed_details on POST <br>
Data Passed: Updated details of the pest or weed <br>
Data Relationship: Displays current details in the admin_update_pest_weed_details.html template for editing and updates the database on POST submission. <br><p/>

Add Pest/Weed (/admin/add_pest_weed): <br>
Description: Adds a new pest or weed entry to the database. <br>
Template: admin_add_pest_weed.html for GET, redirects to view_pest_directory on POST <br>
Data Passed: New pest or weed data from the form <br>
Data Relationship: Provides a form for adding new pest/weed entries and inserts them into the database on POST submission. <br><p/>

Delete Pest/Weed (/admin/delete_pest_weed/int:agriculture_id): <br>
Description: Deletes a pest or weed entry from the database. <br>
Template: None, redirects to view_pest_directory <br>
Data Passed: agriculture_id of the pest or weed to be deleted <br>
Data Relationship: Removes the pest or weed entry from the database and redirects to the pest directory page. <br><p/>

Sources (/admin/sources): <br>
Description: Displays a page with references or sources of content. <br>
Template: admin_sources.html <br>
Data Passed: None <br>
Data Relationship: Renders the admin_sources.html template, which lists references or sources for the content. <br><p/>

Logout (/admin/logout): <br>
Description: Logs the admin out by clearing the session. <br>
Template: None, redirects to login <br>
Data Passed: None <br>
Data Relationship: Clears session data and redirects to the login page. <br><p/>

### Assumptions and design decisions: <br>
Assumptions: 
- Administrators and staff cannot delete their own profiles.
- Administrators cannot change the role of staff and agronomists, they can only add new users with associated roles.
- Website can be further customised to include more role-specific features.
- Any new users would only be registered through the webpage.

### Design decision: 
The website was crafted with an emphasis on both functionality and aesthetics. Here's a breakdown of the design decisions and their rationale:<br>
<p>1. Homepage Design: The primary landing page incorporates images for both the driver and admin interfaces, elevating the visual appeal. These images not only make the site more engaging but also offer flexibility. They serve as placeholders, allowing for seamless integration of event information or other pertinent content in the future.<p/>
<p>2. Navigation System: Recognizing the importance of user-friendly navigation, a comprehensive navigation bar was integrated. It ensures users can intuitively find their way around the platform, enhancing overall user experience.<p/>
<p>3. Driver's Run Details: This route is backed by dual templates. The first presents a dropdown list for selections, while the second displays detailed driver run stats. The differentiation ensures that when users transition from the 'list driver' app route to access specific driver run details, they aren’t confronted with the dropdown again, effectively reducing information clutter.
<p>4. Admin Interface: A specialized route was carved out exclusively for the admin interface. It’s an encapsulated space where administrators can tap into functionalities concealed from the general audience, ensuring secure administrative operations.<p/>
<p>5. Edit Runs Route: The 'edit runs' route uses one template for run selection and another for run detail modifications. The design ensures only the most pertinent fields are editable, thereby limiting potential human errors. To further bolster data integrity, input fields like time, cones, and wd are confined to numeric data types.<p/>
<p>6. Adding a Driver: The route to add a new driver streamlines information collection through a singular template. This consolidated approach reduces user navigation steps and ensures a smoother data entry experience. Alongside, robust input validation mechanisms are in place on both client and server sides to maintain data quality. <br><p/>
<p>7. Overall Results: I opted to include a caption below the table, providing explanations for the abbreviations. This was done to ensure that drivers who are newcomers to the event can easily comprehend the terms used. <p/>
In essence, each design decision was a balance between user-centric aesthetics and functional robustness, all while ensuring data integrity and usability remained paramount. <br>
<p>8. User feedback: Messages are displayed prominently to confirm that actions like updating data or adding a new driver have been completed successfully or unsuccessfully, providing users with immediate feedback on the success of their actions. </p>


### Image Sources: <br>
HD wallpaper: green coupe wallpaper, BMW, car, minimalism, black, simple background | Wallpaper Flare. (n.d.). https://www.wallpaperflare.com/green-coupe-wallpaper-bmw-car-minimalism-black-simple-background-wallpaper-pbimn








