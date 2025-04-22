# SoilSensorEmail.py
# Description: Send a email to notificate the plant status
# Name: Jinru Yao
# Student Number: W20110012
# Course & Year: Project3 & Year3
# Date: 22/4/2025

import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz
import time
import RPi.GPIO as GPIO

# Email setup
from_email_addr = "917545827@qq.com"
from_email_pass = "hbraqqupstiabbij"
to_email_addr = "917545827@qq.com"

# Beijing timezone setup
beijing_tz = pytz.timezone('Asia/Shanghai')

# GPIO setup for soil moisture sensor
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

# Global variable to store the moisture status
water_detected = None

# Callback function for soil moisture sensor
def callback(channel):
    global water_detected
    if GPIO.input(channel): # Assuming HIGH means dry
        print("Sensor reading: Dry")
        water_detected = False
    else: # Assuming LOW means wet
        print("Sensor reading: Wet")
        water_detected = True
    print(f"Water detected status updated to: {water_detected}")

# Add event detection for GPIO pin
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

# Function to send email with the plant status
def send_email(plant_status, water_detected_status):
    # Create a NEW email message object every time
    msg = EmailMessage()

    current_time = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    email_body = (
        f"Date and Time: {current_time}\n"
        f"Plant Status: {plant_status}\n\n"
        f"Water Detected: {'Yes' if water_detected_status else 'No'}\n\n"
        "This is an automated notification from your Raspberry Pi Plant Monitoring System.\n"
        "Keep taking good care of your plant!"
    )

    msg.set_content(email_body)
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = 'Plant Watering Notification'

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(from_email_addr, from_email_pass)
        server.send_message(msg)
        print(f"Email sent successfully at {current_time}")
    except Exception as e:
        print(f"Error sending email: {e}")
    finally:
        if 'server' in locals() and server:
             server.quit()

# Function to calculate the next send time based on the current time (Beijing time)
def get_next_send_time(start_hour=8, interval_hours=3):
    now = datetime.now(beijing_tz)
    target_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)

    # Calculate the next scheduled time if current time is past the start time
    if now > target_time:
        delta_hours = now.hour - start_hour
        intervals_passed = delta_hours // interval_hours
        if now.minute > 0 or now.second > 0 or (delta_hours % interval_hours != 0):
             intervals_passed += 1

        hours_to_add = intervals_passed * interval_hours
        target_time += timedelta(hours=hours_to_add)

        while target_time <= now:
             target_time += timedelta(hours=interval_hours)

    return target_time

# Main loop to send emails at specified intervals
def main():
    next_send_time = get_next_send_time(start_hour=8, interval_hours=3)
    print(f"First email scheduled for: {next_send_time} (Beijing Time)")

    send_count = 0
    while send_count < 5: # Example: send 5 emails
         now = datetime.now(beijing_tz)
         time_to_wait = (next_send_time - now).total_seconds()

         if time_to_wait > 0:
             print(f"Waiting {int(time_to_wait)} seconds until {next_send_time} (Beijing Time) for email #{send_count + 1}...")
             time.sleep(time_to_wait)

         now = datetime.now(beijing_tz)

         if now >= next_send_time:
             print(f"Sending email #{send_count + 1} at {now}...")

             # Use the global water_detected status from GPIO callback
             if water_detected is None:
                  print("Warning: No sensor data received yet. Skipping email.")
                  next_send_time += timedelta(hours=3)
                  print(f"Skipped email #{send_count + 1}. Next scheduled for: {next_send_time}")
                  continue

             plant_status = "Water NOT needed" if water_detected else "Please water your plant!"

             send_email(plant_status, water_detected)

             send_count += 1

             next_send_time += timedelta(hours=3)
             print(f"Email #{send_count} sent. Next scheduled for: {next_send_time}")

         else:
             print(f"Current time {now} is slightly before target {next_send_time}. Waiting briefly.")
             time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("Cleaning up GPIO...")
        GPIO.cleanup()
        print("GPIO cleanup complete.")

