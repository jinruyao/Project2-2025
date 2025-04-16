# Name: Jinru Yao
# Student Number: 20110012
# Date: 16/4/2025

# !/usr/bin/python
import RPi.GPIO as GPIO
import time

#GPIO SETUP
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print("Water not dectected!")
    else: 
        print("Water dectected!")
# let us know when th pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300) 
# assign function to GPIO PIN, Run function on change
GPIO.add_event_callback(channel, callback) 

# infinite loop
while True:
    time.sleep(1)
