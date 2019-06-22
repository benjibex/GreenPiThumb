# -*- coding: utf-8 -*-
#!/usr/bin/python

import pyrebase
import sys
import Adafruit_DHT
import json, requests

#create function to check sensor reading
def LSval (LSpin):
    reading = 0
    GPIO.setup(LSpin,GPIO.OUT)
    GPIO.output(LSpin,GPIO.LOW)
    time.sleep(1)
    GPIO.setup(LSpin,GPIO.IN)
    while (GPIO.input(LSpin) == GPIO.LOW):
        reading += 1
    return reading

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

#Light sensor =LS Light is LED
LED=21
LS=13

GPIO.setup(LED,GPIO.OUT)
config = {
    "apiKey": "AIzaSyCgqcrbXjJozIfM-0Bxk_tMDg78dci3xR0",
    "authDomain": "gtpdatabase.firebaseapp.com",
    "databaseURL": "https://gtpdatabase.firebaseio.com",
    "projectId": "gtpdatabase",
    "storageBucket": "gtpdatabase.appspot.com",
    "messagingSenderId": "791376230162"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#url = "https://gtpdatabase.firebaseio.com/temperature.json"
while True:
    humidity, temperature = Adafruit_DHT.read_retry(11,4)
    print("Temp: {0:0.1f} C Humidity: {1:0.1f} %".format(temperature, humidity))
    lightres = LSval(LS)
    updatedata = {"Temperature": temperature,
                  "Humidity": humidity,
                  "Light Resistance": lightres}
    db.child("plant1").child("Latest Readings").update(updatedata)
    #data = {'humidity': humidity, 'temperature': temperature}
    print(updatedata)

    #Read the database for LED status
    led = db.child("plant1").child("LED Switch").get().val()

    #check the number returned from the function and turn LED on or off as needed
    if led == 1:
        GPIO.output(LED,True)
        time.sleep(10)
    elif led == 0.5:
        if lightres>5000:
            GPIO.output(LED,True)
        else:
            GPIO.output(LED,False)
    else:
        GPIO.output(LED,False)
        time.sleep(10)
        
    db.child("plant1").update({"LED Switch": 0.5})
    #Update the database
    humidity_readings = db.child("plant1").child("Readings").child("Humidity").get()
    humidity_readings = humidity_readings.val()[1:] + [humidity]
    temp_readings = db.child("plant1").child("Readings").child("Temperature").get()
    temp_readings = temp_readings.val()[1:] + [temperature]
    lightres_readings = db.child("plant1").child("Readings").child("Light Resistance").get()
    lightres_readings = lightres_readings.val()[1:] + [lightres]
    db.child("plant1").child("Latest Readings").update(updatedata)
    update_readings = {"Humidity": humidity_readings,
                       "Temperature": temp_readings,
                       "Light Resistance": lightres_readings}
    db.child("plant1").child("Readings").update(update_readings)
    #requests.post(url, json.dumps(data))
#Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
#[GCC 6.3.0 20170124] on linux
#Type "copyright", "credits" or "license()" for more information.

GPIO.cleanup() 



