import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

# Get the project folder path
project_folder = os.path.dirname(os.path.abspath(__file__))

def fetch_clinic_names():
    try:
        conn = sqlite3.connect(os.path.join(project_folder, 'DOC_AVAIL_1.db'))
        cursor = conn.cursor()
        cursor.execute('''SELECT DISTINCT CLINICS FROM DOC_AVAIL_1''')
        clinic_names = [row[0] for row in cursor.fetchall()]
        return clinic_names
    except sqlite3.Error as e:
        print("Error fetching clinic names from the database:", e)
        return []

def create_appointments_table():
    try:
        conn = sqlite3.connect(os.path.join(project_folder, 'patient_appointments.db'))
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY,
                        slot INTEGER,
                        patient_name TEXT,
                        age INTEGER,
                        gender TEXT,
                        phone_number TEXT,
                        clinic_name TEXT,
                        FOREIGN KEY (clinic_name) REFERENCES DOC_AVAIL_1(CLINICS)
                        )''')
        conn.commit()
        print("Appointments table created successfully.")
    except sqlite3.Error as e:
        print("Error creating appointments table:", e)

def store_appointment_data(slot, patient_name, age, gender, phone_number, clinic_name):
    try:
        conn = sqlite3.connect(os.path.join(project_folder, 'patient_appointments.db'))
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO appointments (slot, patient_name, age, gender, phone_number, clinic_name) 
                          VALUES (?, ?, ?, ?, ?, ?)''', (slot, patient_name, age, gender, phone_number, clinic_name))
        conn.commit()
        print("Appointment data stored successfully.")
    except sqlite3.Error as e:
        print("Error storing appointment data:", e)

def allocate_slot(clinic_name):
    try:
        conn = sqlite3.connect(os.path.join(project_folder, 'DOC_AVAIL_1.db'))
        cursor = conn.cursor()
        cursor.execute('''SELECT SLOTS_BOOKED FROM DOC_AVAIL_1 WHERE CLINICS = ?''', (clinic_name,))
        slots_booked = cursor.fetchone()[0]  # Get slots booked for the clinic
        cursor.execute('''UPDATE DOC_AVAIL_1 SET SLOTS_BOOKED = SLOTS_BOOKED + 1 WHERE CLINICS = ?''', (clinic_name,))
        conn.commit()
        slot_number = slots_booked + 1  # Calculate the allocated slot number
        return slot_number
    except sqlite3.Error as e:
        print("Error allocating slot:", e)
        return None

def fetch_data():
    try:
        conn = sqlite3.connect(os.path.join(project_folder, 'DOC_AVAIL_1.db'))
        cursor = conn.cursor()
        cursor.execute('''SELECT DOCTOR_NAME, SPECIALITY, AVAILABILITY FROM DOC_AVAIL_1''')
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        print("Error fetching data from the database:", e)
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/availability.html')
def availability():
    data = fetch_data()
    return render_template('availability.html', data=data)

@app.route('/template.html')
def template():
    return render_template('template.html')

@app.route('/doctors.html')
def doctors():
    return render_template('doctors.html')

@app.route('/appointment.html')
def appointment():
    clinic_names = fetch_clinic_names()
    return render_template('appointment.html', clinic_names=clinic_names)

@app.route('/submit-appointment', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':
        patient_name = request.form['patientName']
        age = request.form['age']
        gender = request.form['gender']
        phone_number = request.form['phoneNumber']
        clinic_name = request.form['clinicName']
        slot = allocate_slot(clinic_name)
        if slot is not None:
            create_appointments_table()  # Ensure appointments table exists
            store_appointment_data(slot, patient_name, age, gender, phone_number, clinic_name)
            return f'Appointment submitted successfully! Your slot number is {slot}. if any emergency cases arise then the appointment timing may be a bit extended'
        else:
            return 'Error in booking appointment.'

if __name__ == '__main__':
    create_appointments_table()  # Ensure appointments table exists
    app.run(debug=True)
