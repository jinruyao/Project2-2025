# SoilSensorEmail.py
# Description: Send a email to notificate the plant status
# Name: Jinru Yao
# Student Number: W20110012
# Course & Year: Project3 & Year3
# Date: 20/4/2025

import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz  # Import the pytz library
import time

# Email setup
from_email_addr = "917545827@qq.com"
from_email_pass = "hbraqqupstiabbij"
to_email_addr = "917545827@qq.com"

# Beijing timezone setup
beijing_tz = pytz.timezone('Asia/Shanghai')

# Create an email message object
msg = EmailMessage()

# Function to send email with the plant status
def send_email(plant_status, email_number, water_detected):
    current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    email_body = (
        f"Date and Time: {current_time}\n"
        f"Email Number Today: {email_number}\n"
        f"Plant Status: {plant_status}\n\n"
        f"Water Detected: {'Yes' if water_detected else 'No'}\n\n"
        "This is an automated notification from your Raspberry Pi Plant Monitoring System.\n"
        "Keep taking good care of your plant!"
    )

    msg.set_content(email_body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = f'Plant Watering Notification #{email_number}'

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(from_email_addr, from_email_pass)
        server.send_message(msg)
        print(f"Email #{email_number} sent successfully at {current_time}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        server.quit()

# Function to check the moisture level and determine the plant's watering need
def check_moisture():
    water_detected = True  # Simulating water detection (change to False to test no water)
    if water_detected:
        print("Water detected!")
        return "Water NOT needed", water_detected
    else:
        print("Water not detected!")
        return "Please water your plant!", water_detected

# Function to calculate the next send time based on the current time (Beijing time)
def get_next_send_time(start_hour=8, interval_hours=3):
    now = datetime.now(beijing_tz)
    target_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
   
    # If the current time is already past the start time, calculate the next available time
    if now > target_time:
        # Find the next time after the current time that is a multiple of the interval (3 hours)
        hours_to_next_send = ((now.hour - start_hour) // interval_hours + 1) * interval_hours
        target_time += timedelta(hours=hours_to_next_send)
   
    return target_time

# Main loop to send 5 emails starting from 8 AM at 3-hour intervals
def main():
    # Get the start time (first email time)
    next_send_time = get_next_send_time(start_hour=8, interval_hours=3)

    # Send 5 emails at 3-hour intervals
    for i in range(5):  # Sending 5 emails per day
        time_to_wait = (next_send_time - datetime.now(beijing_tz)).total_seconds()
        if time_to_wait > 0:
            print(f"Waiting until {next_send_time} (Beijing Time) for the next email...")
            time.sleep(time_to_wait)  # Wait until it's time to send the email

        # Check the moisture and send an email
        plant_status, water_detected = check_moisture()
        send_email(plant_status, i + 1, water_detected)

        # Update the next send time by adding the interval (3 hours)
        next_send_time += timedelta(hours=3)

# Start the program
if __name__ == "__main__":
    main()

