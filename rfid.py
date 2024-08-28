import serial
import sqlite3

# Open serial port for communication with RFID reader
ser = serial.Serial('COM6', 9600)  # Replace 'COM6' with the appropriate port and baud rate

# Function to read RFID tag UID
def read_rfid():
    try:
        ser.write(b'READ')  # Send command to RFID reader to read tag
        tag_data = ser.readline().strip()  # Read response from RFID reader
        tag_uid = tag_data.decode('utf-8')  # Decode data received from RFID reader
        print("Received UID:", tag_uid)  # Debug: Print received UID
        # Check if the received data is a looping message
        if "UID tag :" in tag_uid:
            return tag_uid.split(':')[1].strip()  # Extract UID from the message
        return None  # Return None if it's not a UID message
    except serial.SerialException as e:
        print("Serial port error:", e)
        return None

# Function to create DOC_AVAIL_1 table in SQLite database
def create_doc_avail_1_table():
    try:
        conn = sqlite3.connect('DOC_AVAIL_1.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS DOC_AVAIL_1 (
                        UID TEXT PRIMARY KEY,
                        DOCTOR_NAME TEXT NOT NULL,
                        SPECIALITY TEXT NOT NULL,
                        AVAILABILITY TEXT,
                        NEW_COLUMN TEXT  -- New column added
                        )''')
        # Insert initial data
        cursor.execute('''INSERT OR IGNORE INTO DOC_AVAIL_1 (UID, DOCTOR_NAME, SPECIALITY, AVAILABILITY, NEW_COLUMN) 
                          VALUES (?, ?, ?, ?, ?)''', ('6D 03 85 37', 'Dr JOSHI', 'DENTAL', '', ''))  # AVAILABILITY and NEW_COLUMN columns are empty
        cursor.execute('''INSERT OR IGNORE INTO DOC_AVAIL_1 (UID, DOCTOR_NAME, SPECIALITY, AVAILABILITY, NEW_COLUMN) 
                          VALUES (?, ?, ?, ?, ?)''', ('D3 45 9B 92', 'Zubair', 'Children Doctor', '', ''))  # Insertion for the second row
        conn.commit()
        print("DOC_AVAIL_1 table created successfully.")
    except sqlite3.Error as e:
        print("Error creating DOC_AVAIL_1 table:", e)
    finally:
        conn.close()

# Function to toggle AVAILABILITY column in DOC_AVAIL_1 database
def toggle_availability(uid):
    try:
        conn = sqlite3.connect('DOC_AVAIL_1.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT AVAILABILITY FROM DOC_AVAIL_1 WHERE UID = ?''', (uid,))
        current_availability = cursor.fetchone()[0]  # Get current availability
        new_availability = 'AVAILABLE' if current_availability != 'AVAILABLE' else ''  # Toggle availability
        cursor.execute('''UPDATE DOC_AVAIL_1 SET AVAILABILITY = ? WHERE UID = ?''', (new_availability, uid))
        conn.commit()
        print(f"AVAILABILITY toggled to {new_availability} for UID {uid}.")
    except sqlite3.Error as e:
        print("Error toggling AVAILABILITY:", e)
    finally:
        conn.close()

# Main function
def main():
    create_doc_avail_1_table()  # Create the DOC_AVAIL_1 table and insert initial data

    # Continuous loop to read RFID tags
    while True:
        uid = read_rfid()  # Read RFID tag UID
        print("Detected UID:", uid)  # Debug: Print detected UID
        if uid:
            print("Matching UID detected:", uid)  # Debug: Print UID match message
            toggle_availability(uid)  # Toggle availability for detected UID

if __name__ == "__main__":
    main()
