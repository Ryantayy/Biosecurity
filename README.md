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

**Main app (app.py)**
1. **Index/Home ( / ):** <br/>
Description: Redirects to the login page. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: The root index redirects users to the login page, acting as a default entry point to the application. <br/><p/>

2. **Login ( /login/ ):** <br/>
Description: Handles user authentication and session creation. <br/>
Template: index.html <br/>
Data Passed: User credentials from form. <br/>
Data Relationship: On POST, validates user credentials against the database, creates a session, and redirects to the appropriate dashboard based on role. On GET, displays the login form. <br/><p/>

3. **Register ( /register ):** <br/>
Description: Handles new user registration. <br/>
Template: register.html <br/>
Data Passed: New user data from form. <br/>
Data Relationship: On POST, processes the registration form, validates the data, hashes the password, inserts a new user into the database, and commits the transaction. On GET, displays the registration form. <br/><p/>

4. **Logout ( /logout ):** <br/>
Description: Ends the user session and redirects to the login page. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: Clears the user's session data to log them out and redirects them to the login page. <br/><p/>

5. **Before Request ( @app.before_request ):** <br/>
Description: Prepares certain variables before processing a request. <br/>
Template: N/A <br/>
Data Passed: N/A <br/>
Data Relationship: Attaches the hashing instance to the global object g before handling any requests. <br/><p/>

**Agronomist_Page Blueprint (agronomist.py)**
1. **Agronomist Dashboard**<br>
Description: Displays the main dashboard for agronomist users.<br>
Template: agronomist_home.html<br>
Data Passed: Username from session.<br>
Data Relationship: Directly presents the agronomist dashboard if the user is logged in and assigned an 'agronomist' role. Redirects to login otherwise.<br>

2. **Agronomist Profile**<br>
Description: Displays the profile page for agronomist users.<br>
Template: agronomist_profile.htmlbr>
Data Passed: User information from the database.<br>
Data Relationship: Presents the profile of the logged-in agronomist. Requires user data from `agronomist` and `user` tables.<br>

3. **Edit Agronomist Profile**<br>
Description: Allows agronomist users to edit their profile.<br>
Template: agronomist_edit_profile.html<br>
Data Passed: Current user data for pre-population of form.<br>
Data Relationship: Enables the update of agronomist information in the database.<br>

4. **Change Password**<br>
Description: Allows agronomist users to change their password.<br>
Template: agronomist_change_password.html<br>
Data Passed: None explicitly, validation against the user session.<br>
Data Relationship: Facilitates password updates for the logged-in agronomist in the `user` table.<br>

5. **View Pest Directory**<br>
Description: Presents a directory of pests and weeds.<br>
Template: agronomist_pest_directory.html<br>
Data Passed: Lists of pests and weeds.<br>
Data Relationship: Retrieves pest and weed data from `pest_directory` table to display to the user.<br>

6. **View Specific Pest/Weed Details**<br>
Description: Shows details of a specific pest or weed.<br>
Template: agronomist_view_pest_weed_details.html<br>
Data Passed: Details of the selected pest or weed.<br>
Data Relationship: Fetches and displays detailed information from `pest_directory` based on the provided `agriculture_id`.<br>

7. **Sources**<br>
Description: Displays the sources or references page. <br/>
Template: agronomist_sources.html <br/>
Data Passed: None. <br/>
Data Relationship: Renders a static page with sources or references. <br/><p/>

8. **Logout**<br>
Role Required: None.<br>
Description: Logs out the current user and clears the session.<br>
Template: None. Redirects to the login route.<br>
Data Passed: None.<br>
Data Relationship: Clears session data and redirects to the login page.<br>


**Staff_Page Blueprint (staff.py)**
1. **Staff Dashboard ( /staff_dashboard ):** <br/>
Description: Displays the main dashboard for staff users. <br/>
Template: staff_home.html <br/>
Data Passed: Username from session. <br/>
Data Relationship: Directly presents the staff dashboard if the user is logged in and assigned a 'staff' role. Redirects to login otherwise. <br/><p/>

2. **Staff Home ( /staff/ ):** <br/>
Description: Duplicate of the staff dashboard, potentially for different staff-related home content. <br/>
Template: staff_home.html <br/>
Data Passed: Username from session. <br/>
Data Relationship: Similar to the staff_dashboard, checks for 'loggedin' session status and renders the staff homepage or redirects to login. <br/><p/>

3. **Staff Profile ( /staff/profile ):** <br/>
Description: Displays the profile details of the logged-in staff member. <br/>
Template: staff_profile.html <br/>
Data Passed: Account details from database query. <br/>
Data Relationship: Retrieves the staff user's details from the database and presents them on the profile page if logged in. Redirects to login if not logged in. <br/><p/>

4. **Edit Staff Profile ( /staff/edit_profile ):** <br/>
Description: Allows staff to edit their profile information. <br/>
Template: staff_edit_profile.html for GET, redirects on POST. <br/>
Data Passed: Profile data for form pre-filling on GET, updated data on POST. <br/>
Data Relationship: For GET requests, it pre-fills the form with existing user data. For POST requests, it updates the user's profile details in the database. <br/><p/>

5. **Change Staff Password ( /staff/change_password ):** <br/>
Description: Allows staff to change their password. <br/>
Template: staff_change_password.html for GET, redirects on POST. <br/>
Data Passed: Old and new passwords from form. <br/>
Data Relationship: Provides a form to change password on GET requests. Validates and updates the password in the database on POST requests. <br/><p/>

6. **View Agronomist Profile ( /staff/view_agronomist_profile ):** <br/>
Description: Lists profiles of agronomists for staff to view. <br/>
Template: staff_view_agronomist_profile.html <br/>
Data Passed: List of agronomists from the database. <br/>
Data Relationship: Retrieves and displays agronomist profiles from the database for staff to view. <br/><p/>

7. **View Pest Directory ( /staff/view_pest_directory ):** <br/>
Description: Lists pests and weeds for staff to manage. <br/>
Template: staff_pest_directory.html <br/>
Data Passed: Lists of pests and weeds, and a map of primary images. <br/>
Data Relationship: Retrieves and presents a comprehensive list of all pests and weeds from the pest_directory table, including their primary images. <br/><p/>

8. **View Pest/Weed Details ( /staff/view_pest_weed_details/int:agriculture_id ):** <br/>
Description: Shows detailed information for a specific pest or weed. <br/>
Template: staff_view_pest_weed_details.html <br/>
Data Passed: Details of a single pest or weed, along with associated images. <br/>
Data Relationship: Fetches and shows detailed data of a particular pest or weed entry from the pest_directory table and associated images from the images table, based on the provided agriculture_id. <br/><p/>

9. **Update Pest/Weed Details ( /staff/update_pest_weed_details/int:agriculture_id ):** <br/>
Description: Allows staff to update details of a specific pest or weed. <br/>
Template: staff_update_pest_weed_details.html for GET, redirects on POST. <br/>
Data Passed: Updated pest/weed details from form. <br/>
Data Relationship: For GET requests, pre-fills a form with existing pest/weed details. On POST, updates the database with the new details. <br/><p/>

10. **Add Pest/Weed ( /staff/add_pest_weed ):** <br/>
Description: Allows staff to add a new pest or weed to the database. <br/>
Template: staff_add_pest_weed.html for GET, redirects on POST. <br/>
Data Passed: Form data for the new pest or weed entry, and uploaded image file. <br/>
Data Relationship: On GET, displays a form to input new pest or weed details. On POST, it inserts the new entry into the pest_directory table and associates any uploaded image with the new entry in the images table. The user is redirected to the pest directory upon successful addition, or informed of errors otherwise. <br/><p/>

11. **Manage Images (/staff/manage_images/int:agriculture_id):** <br>
Description: Displays a list of images for a specific pest or weed, allowing the staff to manage them. <br>
Template: staff_manage_images.html <br>
Data Passed: agriculture_id for selecting images, images containing the list of images, common_name for display <br>
Data Relationship: Fetches and displays all images related to the specified agriculture_id from the images table. Provides options to upload a new image, set an image as primary, or delete an image. <br><p/>

12. **Upload Image** (/staff/upload_image/int:agriculture_id): <br>
Description: Handles the image upload process for a specific pest or weed. <br>
Template: Redirects to view_pest_weed_details on successful upload or back to manage_images on failure <br>
Data Passed: The uploaded image file <br>
Data Relationship: Inserts the new image into the images table and associates it with the agriculture_id. On success, adds the image to the server and database, flashes a success message, and redirects. On failure, flashes an error message and redirects to the referrer. <br><p/>

13. **Delete Image (/staff/delete_image/int:image_id):** <br>
Description: Deletes a specific image from the server and database. <br>
Template: Redirects to the referrer URL <br>
Data Passed: image_id of the image to be deleted <br>
Data Relationship: Deletes the image file from the server's filesystem and the corresponding record from the images table. <br><p/>

14. **Set Primary Image (/staff/set_primary_image/int:image_id/int:agriculture_id):** <br>
Description: Sets a specific image as the primary image for a pest or weed. <br>
Template: Redirects to manage_images for the specific agriculture_id <br>
Data Passed: image_id of the image to set as primary <br>
Data Relationship: Resets the status of all images for the item to 'active' and sets the selected image's status to 'primary' within the images table. <br><p/>

15. **Delete Pest/Weed ( /staff/delete_pest_weed/int:agriculture_id ):** <br/>
Description: Handles the deletion of a specific pest or weed from the database. <br/>
Template: Redirects after POST <br/>
Data Passed: agriculture_id to identify the pest/weed to delete. <br/>
Data Relationship: Deletes the specified pest/weed from the database and redirects to the pest directory. <br/><p/>

16. **Sources ( /staff/sources ):** <br/>
Description: Displays the sources or references page. <br/>
Template: staff_sources.html <br/>
Data Passed: None. <br/>
Data Relationship: Renders a static page with sources or references. <br/><p/>

17. **Logout ( /staff/logout ):** <br/>
Description: Logs out the current staff user and ends their session. <br/>
Template: None (redirects to login) <br/>
Data Passed: None. <br/>
Data Relationship: Clears the staff user's session data and redirects to the login page. <br/><p/>

**Admin_Page Blueprint (admin.py)**
1. **Admin Dashboard (/admin/admin_dashboard):** <br>
Description: Serves the dashboard for administrators after login. <br>
Template: admin_home.html <br>
Data Passed: username from session <br>
Data Relationship: The admin_dashboard route renders the admin_home.html template displaying the admin dashboard. It requires the user to be logged in and have the 'admin' role. <br><p/>

2. **Admin Home (/admin/):** <br>
Description: Identical to admin_dashboard, serves as an entry point to admin functions. <br>
Template: admin_home.html <br>
Data Passed: username from session <br>
Data Relationship: The admin_home route is an alternative URL that serves the same admin_home.html template as the admin_dashboard. <br><p/>

3. **Admin Profile (/admin/profile):** <br>
Description: Displays the admin's profile information. <br>
Template: admin_profile.html <br>
Data Passed: Account information fetched from database <br>
Data Relationship: Fetches the admin's account details from the database and passes it to the admin_profile.html template. <br><p/>

4. **Edit Profile (/admin/edit_profile):** <br>
Description: Allows the admin to update their profile details. <br>
Template: admin_edit_profile.html for GET, redirects to admin_profile on POST <br>
Data Passed: For GET, current user data to pre-fill the form; for POST, updated user data <br>
Data Relationship: Displays the current admin's information on the admin_edit_profile.html template and updates the database with any changes on POST submission. <br><p/>

5. **Change Password (/admin/change_password):** <br>
Description: Allows the admin to change their password. <br>
Template: admin_change_password.html <br>
Data Passed: None for GET, form data for POST <br>
Data Relationship: Renders a form to change password on GET request. On POST, validates and updates the new password in the database. <br><p/>

6. **Manage User Profile (/admin/manage_user_profile):** <br>
Description: Lists all users with options to edit or delete profiles. <br>
Template: admin_manage_user_profile.html <br>
Data Passed: Lists of agronomists and staff users <br>
Data Relationship: Fetches lists of users from the database and displays them on the page with options to edit or delete. <br><p/>

7. **Add User (/admin/add_user):** <br>
Description: Adds a new user to the system. <br>
Template: admin_add_user.html for GET, redirects to manage_user_profile on POST <br>
Data Passed: User data from form on POST <br>
Data Relationship: Renders a form to add a new user and inserts the user into the database on POST submission. <br><p/>

8. **edit_user (/edit_user/int:user_id):** <br>
Description: Allows editing of specific user details including common information and role-specific details. <br>
Template: admin_edit_user.html <br>
Data Passed: User details fetched from the database based on the provided user ID. <br>
Data Relationship: The user ID is extracted either from the URL or from a form submission depending on the method. Upon receiving the user ID, the corresponding user's details are fetched from the database, including common information and role-specific details. This data is then passed to the admin_edit_user.html template for display and editing. <br><p/>

9. **Change User Password (/admin/change_user_password/int:user_id):** <br>
Description: Allows changing another user's password. <br>
Template: admin_change_user_password.html <br>
Data Passed: User ID for whom the password is to be changed <br>
Data Relationship: Renders a form for admin to change a specific user's password and updates the database on POST submission. <br><p/>

10. **Delete User (/admin/delete_user/int:user_id):** <br>
Description: Deletes a user from the system. <br>
Template: None, redirects to manage_user_profile <br>
Data Passed: User ID of the user to be deleted <br>
Data Relationship: Removes the user from the database and redirects back to the user management page. <br><p/>

11. **View Pest Directory (/admin/view_pest_directory):** <br>
Description: Displays the list of pests and weeds. <br>
Template: admin_pest_directory.html <br>
Data Passed: Lists of pests and weeds, and a map of primary images.  <br>
Data Relationship: Retrieves and presents a comprehensive list of all pests and weeds from the pest_directory table, including their primary images for administrative overview. <br><p/>

12. **View Pest/Weed Details (/admin/view_pest_weed_details/int:agriculture_id):** <br>
Description: Displays details for a specific pest or weed. <br>
Template: admin_view_pest_weed_details.html <br>
Data Passed: Details of a single pest or weed, along with associated images.  <br>
Data Relationship: Fetches and shows detailed data of a particular pest or weed entry from the pest_directory table and associated images from the images table, based on the provided agriculture_id <br><p/>

13. **Update Pest/Weed Details (/admin/update_pest_weed_details/int:agriculture_id):** <br>
Description: Updates the details for a specific pest or weed. <br>
Template: admin_update_pest_weed_details.html for GET, redirects to view_pest_weed_details on POST <br>
Data Passed: Updated details of the pest or weed <br>
Data Relationship: Displays current details in the admin_update_pest_weed_details.html template for editing and updates the database on POST submission. <br><p/>

14. **Add Pest/Weed (/admin/add_pest_weed):** <br>
Description: Adds a new pest or weed entry to the database. <br>
Template: admin_add_pest_weed.html for GET, redirects to view_pest_directory on POST <br>
Data Passed: Form data for the new pest or weed entry, and uploaded image file. <br/>
Data Relationship: On GET, displays a form to input new pest or weed details. On POST, it inserts the new entry into the pest_directory table and associates any uploaded image with the new entry in the images table. The user is redirected to the pest directory upon successful addition, or informed of errors otherwise. <br/><p/>

15. **Manage Images (/admin/manage_images/int:agriculture_id):** <br>
Description: Displays a list of images for a specific pest or weed, allowing the admin to manage them. <br>
Template: admin_manage_images.html <br>
Data Passed: agriculture_id for selecting images, images containing the list of images, common_name for display <br>
Data Relationship: Fetches and displays all images related to the specified agriculture_id from the images table. Provides options to upload a new image, set an image as primary, or delete an image. <br><p/>

16. **Upload Image** (/admin/upload_image/int:agriculture_id): <br>
Description: Handles the image upload process for a specific pest or weed. <br>
Template: Redirects to view_pest_weed_details on successful upload or back to manage_images on failure <br>
Data Passed: The uploaded image file <br>
Data Relationship: Inserts the new image into the images table and associates it with the agriculture_id. On success, adds the image to the server and database, flashes a success message, and redirects. On failure, flashes an error message and redirects to the referrer. <br><p/>

17. **Delete Image (/admin/delete_image/int:image_id):** <br>
Description: Deletes a specific image from the server and database. <br>
Template: Redirects to the referrer URL <br>
Data Passed: image_id of the image to be deleted <br>
Data Relationship: Deletes the image file from the server's filesystem and the corresponding record from the images table. <br><p/>

18. **Set Primary Image (/admin/set_primary_image/int:image_id/int:agriculture_id):** <br>
Description: Sets a specific image as the primary image for a pest or weed. <br>
Template: Redirects to manage_images for the specific agriculture_id <br>
Data Passed: image_id of the image to set as primary <br>
Data Relationship: Resets the status of all images for the item to 'active' and sets the selected image's status to 'primary' within the images table. <br><p/>

19. **Delete Pest/Weed (/admin/delete_pest_weed/int:agriculture_id):** <br>
Description: Deletes a pest or weed entry from the database. <br>
Template: None, redirects to view_pest_directory <br>
Data Passed: agriculture_id of the pest or weed to be deleted <br>
Data Relationship: Removes the pest or weed entry from the database and redirects to the pest directory page. <br><p/>

20. **Sources (/admin/sources):** <br>
Description: Displays a page with references or sources of content. <br>
Template: admin_sources.html <br>
Data Passed: None <br>
Data Relationship: Renders the admin_sources.html template, which lists references or sources for the content. <br><p/>

21. **Logout (/admin/logout):** <br>
Description: Logs the admin out by clearing the session. <br>
Template: None, redirects to login <br>
Data Passed: None <br>
Data Relationship: Clears session data and redirects to the login page. <br><p/>

### Assumptions and design decisions: <br>
Throughout the development of the web application, several assumptions were made and design decisions were taken to guide the development process and address the requirements effectively. Below is a detailed account of these considerations.<br>
  **Assumptions:** <br>
- Profile Deletion Restrictions: Administrators and staff members do not have the capability to delete their own profiles to prevent accidental or malicious removal of essential users from the system. <br>
- Scalability and Customization: The web application is designed with future expansion in mind, allowing for the introduction of additional features and functionalities tailored to specific roles as the need arises.<br>
- User Registration Process: The platform mandates that all new user registrations occur directly through the website. <br>
- Security: The application assumes a basic level of security for user authentication and authorization, primarily through session management and password hashing.
- Staff Position: Staff position refers to the position 'admin' and 'staff.
- There are various departments, therefore no validation has been made. 

### Design decision: 
The website was crafted with an emphasis on both functionality and aesthetics. Here's a breakdown of the design decisions and their rationale:<br><br>
**Homepage Design**
- **Rationale**: The homepage was designed with visual appeal and functionality in mind, using engaging imagery to guide users towards their respective interfaces. This approach not only makes the site more inviting but also helps in conveying the purpose of the application intuitively.
- **Impact**: Enhanced user engagement from the first interaction, leading to a positive user experience. The distinct imagery for different user roles simplifies navigation, making it easier for users to find the information relevant to them.

**Navigation System**
- **Rationale**: Implementing a comprehensive and intuitive navigation system was crucial for enhancing usability. A well-structured navigation bar ensures users can easily access all parts of the application without confusion, significantly improving the overall user experience.
- **Impact**: Users benefit from a seamless and intuitive navigation experience, reducing frustration and increasing efficiency in completing tasks. The navigation system supports users in discovering all available features, leading to higher engagement and satisfaction.

**Role-Specific Templates**
- **Rationale**: Creating separate templates for different user roles (such as admin, staff, and agronomist) allows for a customized user experience that caters to the specific needs and permissions of each role. This design decision ensures that users only see content and options relevant to their responsibilities and access rights, enhancing security and usability.
- **Impact**: Improved clarity and efficiency for users by preventing information overload and reducing the risk of unauthorized access to sensitive functionalities. Role-specific templates streamline the user journey within the application, leading to a more focused and productive experience.

**Modular Architecture Using Blueprints**
- **Rationale**: To enhance the application's scalability and maintainability by segregating functionalities based on user roles.
- **Impact**: Facilitated role-based access control and streamlined the development process by allowing independent development and testing of each module.

**Role-Based Access Control**
- **Rationale**: To ensure users can only access information and functionalities relevant to their roles, enhancing security and user experience.
- **Impact**: Implemented through decorators, Role-Based Access Control prevents unauthorized access and simplifies navigation by presenting users with only the relevant options.

**Password Hashing for Security**
- **Rationale**: To secure user passwords against potential database breaches, ensuring that passwords are not stored in plain text.
- **Impact**: Increases user trust and application security. Utilizing Flask's `hashing` module provided an efficient way to implement this feature.

**Session Management for User State**
- **Rationale**: To maintain user state across requests, enabling personalized user experiences and security checks.
- **Impact**: Allowed seamless user experiences across different parts of the application while ensuring that users are authenticated and authorized for their actions.

**Agricultural Theme and Color Palette**
- **Rationale**: The choice of dark grey was used for the navigation bar and thematic photographs aimed to resonate with the agricultural domain, invoking a sense of growth, nature, and earthiness. 
- **Impact**: This design decision not only enriched the visual appeal of the platform but also reinforced its purpose. The use of relevant imagery and a carefully curated color palette fostered a more engaging and relatable environment for users, particularly those with a background or interest in agriculture.

## Image Sources: <br>
<p> AgPest » Pest directory. (n.d.). https://agpest.co.nz/pest-directory/ </p>
<p>Payman, A. (2018, April 14). green leafed plants during daytime. Unsplash. https://unsplash.com/photos/green-leafed-plants-during-daytime-2oYMwuFgnTg </p>
<p>Valio84sl. (2016, July 19). Tractor cultivating field at spring,aerial view. iStock. https://www.istockphoto.com/essential/photo/tractor-cultivating-field-at-spring-gm543212762-97439973</p>








