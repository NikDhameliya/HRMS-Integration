### Task Description for Upwork

**Title:** Custom Odoo Module Development for HRM Data Migration


**Key Features of the Custom Module "Import HR Data from API"**

1. **Settings Screen:**
   - Ability to enter API key and base URL of the existing HRM system's API.
   - A "Start"/"Stop" button to initiate or interrupt the import process.
   - A real-time log panel to display the import job execution progress.

2. **Data Import Functionality:**
   - Import organizational departments/teams hierarchy.
   - Import all employee data from the HRM system API and create user accounts for current employees, maintaining their relationships to departments and teams.
   - Import all absence data to replicate the history of time-offs in Odoo.
   - Ensure all imported entities store their external ID for reference.
   - Ensure pagination is implemented to handle large amounts of data efficiently.
   - Ensure no duplicate records are created in Odoo.
   - No need to restore the state of the import process after a system failure. New run will start from the beginning, but the import process should prevent data duplication.

**Requirements:**

- You will be responsible for building the custom module only. Sample JSON responses from the HRM system API will be provided for data extraction purposes. You can use them to understand the structure of the data and mock the API responses.
- The migration process will be performed by our team.

**API Descriptions:**
The HRM system's API descriptions are available in the following documents:
- GET Departments.md
- GET Employees.md
- Get OutOfOffice.md

These documents contain detailed information about the API endpoints, including request methods, query parameters, sample requests, and sample responses.




# Plan

1.
hrms.settings (Put this inside general settings or create a new app settings)
Add this settings url  (Ref Franchisee)

   API key
   base URL
   version(default v1)
   department url path
   employees url path
   outofoffice url path


2. Employees menu, open tree view and form view

3. Departments menu, open tree view and form view

4. outofoffice menu, open tree view and form view

5. Refer Operations menu in shopify app
   Add a menu Operations
   It should open a wizard with 

   Operations = Import Emp
                Import dept
                Import OOF
   On Submit create a new import record

   Import record should have log lines, imported records entry


5. Add a Dashboard with counters, last sync dates, Import screen section with start and stop buttons