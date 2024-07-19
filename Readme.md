README
Overview
This project is a web application built using Django and React. It includes functionalities for managing appointments between doctors and patients, with separate dashboards and calendar management features. This document provides an overview of the key features and functionality implemented in the project.

Features
1. Doctor Calendar Generation at Login Using Signals
Upon logging in, a doctor's calendar is automatically generated. This is accomplished using Django signals. When a doctor logs into the system, a signal is triggered to create a calendar entry for the doctor. This process ensures that each doctor has an up-to-date calendar ready for managing their appointments.

Implementation Details:

Signal Used: post_save signal on the CustomerUserProfile model.
Calendar Generation: The signal handler creates calendar entries based on the doctor's profile and availability.
2. Segregated Dashboards Based on User Type
The application features distinct dashboards for patients and doctors, tailored to their specific needs.

Patient Dashboard: Accessible to users with the patient user type. Provides an overview of upcoming appointments, health records, and other patient-specific information.
Doctor Dashboard: Accessible to users with the doctor user type. Includes functionalities for managing appointments, viewing patient details, and updating availability.
Implementation Details:

Conditional Rendering: The dashboard displayed is based on the user_type field in the CustomerUserProfile model.
Navbar Navigation: Different components are shown in the Navbar based on the user type, such as Dashboard for patients and Appointments for doctors.
3. Calendar and Events Update via the API
Calendars and events are managed and updated through a RESTful API. This allows for seamless integration and real-time updates between the frontend and backend.

API Endpoints:
/api/calendar: Manages calendar entries and events.
/api/appointments: Handles appointment scheduling and updates.
Implementation Details:

Django REST Framework: Utilized to create API endpoints for managing calendars and events.
React Integration: The frontend makes API calls to fetch and update calendar data as needed.
4. Aware and Naive Timezones
The application supports both aware and naive timezones to accommodate various user preferences and locations.

Aware Timezones: Timezones that are aware of daylight saving time (DST) and other local time changes.
Naive Timezones: Timezones without DST awareness, used for simpler time calculations.
Implementation Details:

Timezone Management: Handled using Python’s pytz library and Django’s timezone utilities.
Frontend Handling: React components are designed to manage and display time in both aware and naive formats as required.
