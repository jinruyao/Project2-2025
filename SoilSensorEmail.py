# SoilSensorEmail.py
# Description: Send a email to notificate the plant status
# Name: Jinru Yao
# Student Number: W20110012
# Course & Year: Project3 & Year3
# Date: 20/4/2025

import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz  # Import the pytz library

# GPIO setup
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# Email setup
from_email_addr = "917545827@qq.com"
from_email_pass = "hbraqqupstiabbij"
to_email_addr = "917545827@qq.com"

# Beijing timezone setup
beijing_tz = pytz.timezone('Asia/Shanghai')

# Create an email message object
msg = EmailMessage()

# Function to send email with the plant status

def send_email(plant_status, email_number):
    current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    email_body = (
        f"Date and Time: {current_time}\n"
        f"Email Number Today: {email_number}\n"
        f"Plant Status: {plant_status}\n\n"
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
    if GPIO.input(channel):
        print("Water not detected!")
        return "Please water your plant!"
    else:
        print("Water detected!")
        return "Water NOT needed"

# Function to calculate the next send time based on the current time (Beijing time)
def get_next_send_time(start_hour=7, interval_hours=3):
    now = datetime.now(beijing_tz)
    target_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    if now > target_time:
        hours_to_next_send = ((now.hour - start_hour) // interval_hours + 1) * interval_hours
        target_time += timedelta(hours=hours_to_next_send)
    return target_time

# Main loop to take 4 readings each day at regular intervals (every 3 hours)
def main():
    next_send_time = get_next_send_time()
    for i in range(4):
        time_to_wait = (next_send_time - datetime.now(beijing_tz)).total_seconds()
        if time_to_wait > 0:
            print(f"Waiting until {next_send_time} (Beijing Time) for the next email...")
            time.sleep(time_to_wait)

        plant_status = check_moisture()
        send_email(plant_status, i + 1)
        next_send_time += timedelta(hours=3)

# Run the main function for 3 days
def run_for_three_days():
    for day in range(3):
        print(f"Day {day+1} - Starting moisture checks")
        main()
        print(f"Day {day+1} - Completed moisture checks")

# Start the program
if __name__ == "__main__":
    run_for_three_days()
