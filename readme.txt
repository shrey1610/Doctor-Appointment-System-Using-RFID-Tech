# Doctor Appointment System using RFID Technology

## Project Description
The **Doctor Appointment System using RFID Technology** is a comprehensive web-based application aimed at improving the efficiency of managing patient appointments and doctor availability in a hospital or clinic setting. It leverages **RFID (Radio Frequency Identification)** technology to track the availability status of doctors in real-time, making the system more responsive and dynamic.

The system allows patients to book appointments, verify their identity through OTP and email verification, and view real-time doctor availability based on RFID data. For administrators, the system provides tools to manage patient records, oversee appointments, and monitor doctors’ schedules automatically through RFID tracking.

## Features
- **Patient Authentication**: Patients verify their identity through secure OTP and email verification before accessing the system.
- **RFID-based Doctor Availability**: The RFID system tracks the presence and availability of doctors in the hospital, updating their status dynamically in the system.
- **Appointment Booking**: Patients can easily view available time slots and book appointments with doctors.
- **Real-time Availability Updates**: Doctors' availability status is updated automatically using RFID technology, ensuring patients and staff have the most up-to-date information.
- **Administrative Dashboard**: Clinic or hospital administrators have access to manage appointments, patient records, and monitor doctors' schedules based on RFID data.

## Project Structure
```
hack_doc_avail/
    app.py
    DOC_AVAIL_1.db
    enter_otp.html
    patient_appointments.db
    rfid.py
    temparory.py
    verify_email.html
    database/
        patient_appointments.db
    manager/
        index.html
        otp.html
        python.py
    static/
        appointment.jpeg.jpg
        availability.jpeg.jpg
        ballari.png
        joshi.png
        logo.png
        priyanka.png
        images/
    templates/
        about.html
        appointment.html
        availability.html
        doctors.html
        index.html
        template.html
```

## Technologies Used
- **Python**:
  - **Flask**: Flask is the micro-framework used to develop the backend of this web application. It handles routing, server-side logic, and communication with the databases.
  - **RFID Integration**: Python scripts (`rfid.py`) are used to interface with the RFID hardware to track doctor availability. The RFID data is fed into the system to automatically update doctors’ status, providing real-time information on their availability.
  
- **SQLite**:
  - **Database Storage**: The project uses SQLite databases to store patient appointment data, doctor schedules, and other necessary information. This includes `patient_appointments.db` and `DOC_AVAIL_1.db`, which store patient and doctor information.

- **HTML/CSS/JavaScript**:
  - **Frontend Design**: HTML, CSS, and JavaScript are used to design the user interface and ensure an interactive experience. The templates (`about.html`, `appointment.html`, `availability.html`, etc.) create dynamic web pages that patients and administrators use to interact with the system.

- **RFID Technology**:
  - **Doctor Availability Management**: RFID readers are used to detect the presence of doctors when they enter or exit the hospital. This information is sent to the backend system, which automatically updates the doctor's availability status. For example, when a doctor enters a certain RFID-enabled area (e.g., their office or consultation room), their status is updated to “Available,” and when they leave, it is set to “Unavailable.”
  
- **Email/OTP Verification**:
  - **Security and Authentication**: The system uses OTP (One-Time Password) and email verification (`enter_otp.html` and `verify_email.html`) to ensure that only authorized patients can access the system. This adds a layer of security, protecting sensitive patient information and appointment data.



## Usage
- **Patients**: Register or log in, verify their identity using OTP and email verification, book appointments, and check real-time doctor availability.
- **Administrators**: Manage patient records, schedule appointments, and oversee doctor availability using the RFID system.
- **RFID System**: Automatically tracks when doctors are available or unavailable based on their proximity to RFID readers within the hospital.

## Technologies Used
- **Python** (Flask)
- **RFID Technology** (Doctor availability management)
- **SQLite** (Database)
- **HTML/CSS/JavaScript** (Frontend)
- **OTP and Email Verification** (Security)

