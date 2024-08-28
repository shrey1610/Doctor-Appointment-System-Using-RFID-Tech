from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string
import os

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    conn = sqlite3.connect('project_folder/templates/DOC_AVAIL_1.db')
    return conn

# Function to check if the email exists in the database
def check_email(email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row

# Function to generate random OTP
def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for OTP generation page
@app.route('/otp', methods=['GET', 'POST'])
def generate_otp():
    if request.method == 'POST':
        email = request.form['email']
        row = check_email(email)
        if row:
            otp = generate_otp()
            # You might want to store this OTP in the database for verification
            # For simplicity, I'm just passing it to the template
            return render_template('otp.html', otp=otp)
        else:
            return "Email not found in database"
    else:
        return redirect('/')

# Route for OTP verification page
@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    entered_otp = request.form['otp']
    # Here you would typically verify the OTP entered by the user
    # For simplicity, let's assume OTP is "1234"
    if entered_otp == "1234":
        return "OTP Verified Successfully!"
    else:
        return "Invalid OTP!"

if __name__ == '__main__':
    app.run(debug=True)
