from flask import Flask, render_template, request, redirect, url_for, session
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'szstp2003@gmail.com'
app.config['MAIL_PASSWORD'] = 'bpnf vfow psua jhec'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Dummy doctor data (replace with actual data from your database)
doctors = {
    'doctor1@example.com': {'name': 'Doctor 1', 'available': False},
    'doctor2@example.com': {'name': 'Doctor 2', 'available': False},
    # Add more doctor entries as needed
}

# Function to send email with OTP
def send_otp(email):
    try:
        otp = secrets.token_hex(3)  # Generate a random 3-digit OTP
        session['otp'] = otp  # Store OTP in session for verification
        msg = Message('OTP Verification', sender='szstp2003@gmail.com', recipients=[email])
        msg.body = f'Your OTP is: {otp}'
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False

# Route to enter doctor's email for OTP verification
@app.route('/verify_email.html', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email = request.form['email']
        if email in doctors:
            if send_otp(email):
                session['email'] = email
                return redirect(url_for('enter_otp.html'))
            else:
                return "Error sending OTP email"
        else:
            return "Doctor not found"
    return render_template('verify_email.html')

# Route to enter OTP
@app.route('/enter_otp.html', methods=['GET', 'POST'])
def enter_otp():
    if request.method == 'POST':
        otp_entered = request.form['otp']
        if 'email' in session and 'otp' in session and otp_entered == session['otp']:
            doctors[session['email']]['available'] = True
            del session['email']
            del session['otp']
            return "Availability updated successfully"
        else:
            return "Invalid OTP"
    return render_template('enter_otp.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running Flask application: {e}")