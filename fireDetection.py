import cv2   
import threading 
import playsound 
import smtplib    
from email.mime.text import MIMEText
import mysql.connector 
import re

fire_cascade = cv2.CascadeClassifier('fire_detection_cascade_model.xml')

# open webcam
vid = cv2.VideoCapture(0)  

runOnce = False 

def get_employee_contacts():
    try:
        #sql
        conn = mysql.connector.connect(
            host='localhost',          
            user='root', 
            password='ilasm28Rw!', 
            database='employeedb'
        )
        cursor = conn.cursor()

        #get email + phone #
        cursor.execute("SELECT email, phone, carrier FROM add_employee")
        contacts = cursor.fetchall()

        #close connection
        conn.close()

        return contacts 

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

def play_alarm_sound_function():
    playsound.playsound('fire_alarm.mp3', True)  # To play alarm sound
    print("Fire alarm ended")

def send_alerts_function():
    contacts = get_employee_contacts()  
    print("Contacts fetched from database:", contacts)

    sender_email = "shinyrose8821@gmail.com"
    sender_password = "cqtr xczv lypu egry"

    try:
        #connect
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.set_debuglevel(1)

        #message
        subject = "Fire Alert: Emergency Notification"
        body = "Warning: A fire accident has been reported. Please take necessary actions."
        message = f"Subject: {subject}\n\n{body}"

        sms_body = "Fire Alert: A fire accident has been reported. Take action immediately."
        sanitized_message = re.sub(r"X-CMAE-Envelope:.*", "", sms_body)

        #text carrier
        carrier_gateways = {
            "AT&T": "@txt.att.net",
            "T-Mobile": "@tmomail.net",
            "Verizon": "@vtext.com",
            "Sprint": "@messaging.sprintpcs.com",
        }

        # send email + text
        for email, phone, carrier in contacts:
            # email notif
            server.sendmail(sender_email, email, message)
            print(f"Alert email sent successfully to {email}")

            # text notif
            if carrier in carrier_gateways:
                sms_address = phone + carrier_gateways[carrier]

                msg = MIMEText(sanitized_message)
                msg['From'] = sender_email
                msg['To'] = sms_address
                msg['Subject'] = subject

                server.sendmail(msg["From"], msg["To"], msg.as_string())
                print(f"Alert SMS sent successfully to {phone} via {sms_address}")
            else:
                print(f"SMS not sent: Carrier gateway for {phone} is unknown")

        # close connection
        server.close()

    except Exception as e:
        print(f"Error sending alerts: {e}")

while(True):
    ret, frame = vid.read()
    if not ret: 
        print("Error: Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

    #rectangle for fire
    for (x, y, w, h) in fire:
        cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)

        print("Fire alarm initiated")
        threading.Thread(target=play_alarm_sound_function).start()

        if not runOnce:
            print("Alert send initiated")
            threading.Thread(target=send_alerts_function).start()
            runOnce = True
        else:
            print("Alerts are already sent once")

    cv2.imshow('Fire Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
