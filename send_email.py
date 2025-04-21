# send_email.py
# Description: send a email with time
# Name: Jinru Yao
# Student Number: W20110012
# Course & Year: Project3 & Year3
# Date: 20/4/2025

import smtplib
from email.message import EmailMessage
from datetime import datetime
import pytz  # Import the pytz library

# Email setup
from_email_addr = "917545827@qq.com"
from_email_pass = "hbraqqupstiabbij"
to_email_addr = "917545827@qq.com"

# Beijing timezone setup
beijing_tz = pytz.timezone('Asia/Shanghai')

# Create an email message object
msg = EmailMessage()

# Function to send email with the current time and plant status
def send_email():
    # Get current Beijing time
    current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
   
    # Email body with the current time
    email_body = f"Date and Time: {current_time}"

    msg.set_content(email_body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = 'Email time test'

    # Send the email
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(from_email_addr, from_email_pass)
        server.send_message(msg)
        print(f"Email sent successfully at {current_time}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Print current time to terminal
current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
print(f"Current Time (Beijing Time): {current_time}")

# Send the email with the current time
send_email()
