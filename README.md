# Military Officers Management System
This project is a comprehensive web application developed during military service to streamline officer management processes. The platform, built using Django, centralizes critical functionalities such as leave management, attendance tracking, and officer scheduling, significantly reducing dependency on manual and paper-based workflows.

![homepage](https://github.com/user-attachments/assets/aa51f351-6275-4929-96b0-926e593849e6)


## Features
1. Role-Based Permissions  
    * A secure login system tailored to officer roles.
    * Permissions to view, edit, or delete data are assigned based on user roles and hierarchy.
2. Officer Data Management
    * A searchable with filters, interface to list and manage officer profiles.
    * Provides a quick overview of officer availability (present, on leave, etc.).
3. Leave Management System
      * Officers can request leave by specifying type and dates.
      * Requests pass through a multi-level approval process (e.g., supervisor → boss → institute manager).
      * Approvals and rejections are tracked digitally.
4. Nabatshia Scheduling
    * Create, assign, and view shift schedules.
    * Officers can request shift swaps, which require mutual agreement.
5. Daily Attendance Tracking
    * Allows recording and monitoring of attendance data.
    * Provides attendance summaries for administrators.
6. Notification System
    * Alerts users when actions (e.g., leave approval, shift swaps) are required.
    * Notifications are prominently displayed to ensure timely responses.

## Advantages
  * Digitized processes eliminate the need for paper-based records.
  * A single platform for handling attendance, leave, and scheduling.
  * Reduces manual work, saving time and improving accuracy.

## Technologies Used
  * Backend: Django
  * Frontend: Django Templates, Bootstrap, Vanilla JavaScript
  * Database: Microsoft SQL Server or sqlite

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AbdalrahmanHafez/ISI-Django-Project
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt  
    ```

3. Configure the database:
    Update database settings in settings.py to connect to Microsoft SQL Server.

5. Run migrations:
    ```bash
    python manage.py migrate  
    ```

6. Create an admin user:
    ```bash
    python manage.py createsuperuser  
    ```

7.Run the development server:
    ```
    python manage.py runserver
    ```
8. Access the application at http://127.0.0.1:8000/.

## Screenshots
  * Automatic light or dark mode:
    ![black or white 2](https://github.com/user-attachments/assets/7a02adca-6bef-4ffc-b147-dce40b5e2603)
    ![black or white](https://github.com/user-attachments/assets/9c9d90ad-df7b-43d9-897d-c27170996f6f)

  * Login and Permissions:
    ![chrome_ONQYBKb0Ra](https://github.com/user-attachments/assets/51a696c2-631b-47ea-9e1e-a7c45e22e870)

  * Officer Management:
    * Search and filter officer profiles.
    * View details like leave status, shift assignments, and attendance records.
    ![chrome_dOhcavrPQs](https://github.com/user-attachments/assets/1017e8d5-c124-40ca-8be6-be8dad6c588c)

  * Leave Requests:
    * Submit leave requests for review.
    * Approve or reject requests based on user hierarchy.
    ![chrome_GIbqWQq9wn](https://github.com/user-attachments/assets/5c4136a9-6c9c-4d08-af79-a94c87b469df)

  * Shift Scheduling:
    * Assign or request changes to shift schedules.
    * Accept or decline swap requests.
    ![chrome_G5e7b7tvTt](https://github.com/user-attachments/assets/c7a2770b-7a63-49f6-980b-e6146a04a552)
    ![chrome_rLLwn5d2YL](https://github.com/user-attachments/assets/35444ec4-44ce-4146-8c39-73cedfd15c77)
    ![chrome_gVNgcZiWJd](https://github.com/user-attachments/assets/bb6e0932-e351-4ced-88b5-ace30c0c68eb)

    
  * Notifications:
    * Receive alerts for pending approvals or actions.
    ![chrome_5I2ZcibF6Q](https://github.com/user-attachments/assets/2bc06847-ef9b-4aa1-a4c6-8275a38911ac)

## Future Enhancements
  * Add detailed analytics for attendance and leave trends.
  * Implement email notifications for critical actions.

## Contributing
Contributions are welcome! Fork the repository, create a branch, and submit a pull request with your improvements.

