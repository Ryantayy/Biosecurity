# COMP639 Studio Project – Semester 1 2024
Individual Assignment
**Name**: Ryan Tay Peng Yeow <br>
**Student ID**: 1157892

## Biosecurity Guide - Web Application Structure:
### Structure Overview:

<p> My web application follows the typical structure of Flask projects. The application is organized with a combination of routes and their associated functions, and templates to render the appropriate views. This structure aids in maintaining a clean separation of concerns between data processing and presentation. <p/>

### Routes & Functions:

1. **Home ( / ):** <br>
Description: Serves the homepage. <br>
Template: home.html <br>
Data Passed: None. <br>
Data Relationship: The root or index route uses the home.html template to serve as a home page with introductory information. Can add more information in the future related to the current user and recent news or events. <br><p/>

2. **listcourses (/listcourses):** <br>
Description: Displays the list of available courses. <br>
Template: course_list.html <br>
Data Passed: List of courses with their details. <br>
Data Relationship: The /course_list route fetches a list of available courses from the database in the course_list() function and provides this list to the course_list.html template to display. The templates allow for clickable images. <br><p/>

3. **select_driver (/select_driver):** <br>
Description: Displays a selection list of drivers. <br>
Template: driver_selection.html <br>
Data Passed: List of drivers with their details. <br>
Data Relationship: The /select_driver route fetches a list of drivers from the database in the select_driver() function and provides this list to the driver_selection.html template to display. <br><p/>

4. **driver_run_details (/driver_run_details):** <br>
Description: Displays details of a specific driver and their runs. <br>
Template: driver_run_details.html <br>
Data Passed: Driver details and their corresponding run details. <br>
Data Relationship: Depending on the method, either it fetches the driver ID from the list driver URL or from the POST request via a form submission. Using this ID, it fetches the driver's and their run details from the database. This data is then passed to the driver_run_details.html template for display. <br><p/>

5. **listdrivers (/listdrivers):** <br>
Description: Displays a list of all drivers. <br>
Template: driverlist.html <br>
Data Passed: List of drivers with their details. <br>
Data Relationship: The /listdrivers route fetches a list of drivers from the database in the listdrivers() function and provides this list to the driverlist.html template to display. <br><p/>

6. **overallresults (/overallresults):** <br>
Description: Displays overall results for each driver across different courses. <br>
Template: overallresults.html <br>
Data Passed: Run totals of drivers across courses. <br>
Data Relationship: The /overallresults route fetches run totals of drivers across different courses and then provides this data to the overallresults.html template to display. <br><p/>

7. **showgraph (/graph):** <br>
Description: Displays a graph showing top 5 drivers based on their overall results. <br>
Template: top5graph.html <br>
Data Passed: List of top 5 drivers and their results. <br>
Data Relationship: The /graph route fetches the top 5 driver's results and provides this data to the top5graph.html template to display as a graph. <br><p/>

8. **adminInterface (/admin:):** <br>
Description: Displays the admin interface. <br>
Template: adminHome.html <br>
Data Passed: None. <br>
Data Relationship: Direct rendering of the adminHome.html template. <br><p/>

9. **junior_driver_list (/admin/junior-drivers):** <br>
Description: Displays a list of junior drivers. <br>
Template: junior_driver_list.html <br>
Data Passed: List of junior drivers and their details. <br>
Data Relationship: The /admin/junior-drivers route fetches a list of junior drivers from the database and provides this list to the junior_driver_list.html template to display. <br><p/>

10. **driverInterface (/driverInterface):** <br>
Description: Displays the driver interface. For administrator to return to the driver interface. <br>
Template: home.html <br>
Data Passed: None. <br>
Data Relationship: Direct rendering of the home.html template for drivers. <br><p/>

11. **search_driver (/search_driver):** <br>
Description: Allows users to search for drivers based on keywords and displays the results. <br>
Template: search_results.html <br>
Data Passed: Search results based on the keyword. <br>
Data Relationship: Users input a keyword, and the search_driver() function fetches relevant results from the database. These results are then displayed using the search_results.html template. <br><p/>

12. **edit_runs (/edit_runs):** <br>
Description: Allows users to edit the runs for specific drivers and courses. <br>
Template: edit_runs.html <br>
Data Passed: List of drivers, courses, and runs based on selected criteria, success message. <br>
Data Relationship: Users select a driver and/or course, and the corresponding run details are fetched from the database. This data is then passed to the edit_runs.html template for display and editing. Upon successful update, the success message will then display. <br><p/>

13. **edit_individual_run (/edit_individual_run):** 
Description: Allows users to edit the details of an individual run.<br>
Template: edit_individual_run.html <br>
Data Passed: Details of the selected run, errors(if there are validation errors in the form), success message. <br>
Data Relationship: Run details are fetched from the database based on the provided driver ID, course ID, and run number. If the users submit the form with updates, the data is validated and, if valid the run details are updated in the database. If there are validation errors, the errors list is passed to the edit_individual_run.html template along with the run details for display and editing. On successful update, the same data will then be passed to the edit_run route and the updated data and success message will then display. <br><p/>

14. **add_driver (/add_driver):** <br>
Description: Allows the user to add a new driver. <br>
Template: add_driver.html <br>
Data Passed: Details of the new driver, list of available cars, caregivers, potential error messages and success message. <br>
Data Relationship: When the page is loaded, the add_driver() function fetches the list of available cars and caregivers from the database, which is then passed to the add_driver.html template to populate the respective dropdowns. When a form submission is detected (via POST request), the same add_driver() function is responsible for data validation and database insertion. If there are any validation errors, the function repopulates the form fields with the entered data and shows relevant error messages. Upon successful update, the success message will display. <br><p/>

### Assumptions and design decisions: <br>
Assumptions: 
- Drivers aged 17 and older should not have a designated caredriver.
- The age of the driver is limited to 10 to 100.
- The data for cones is either None or an integer.
- The data for wd is either 0 or 1.
- A car model can be associated with more than one car_num (Eg. MX-5).
- Driver's name is to be sorted in surname and last name order but displayed in a conventional way.
- Only course A-F is available for this competition. 

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








