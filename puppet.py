# This file is responsible for the puppet nodes which are directly connected to the sensors
# Possible library to be used for interfacing with the DHT22 - https://github.com/adafruit/Adafruit_CircuitPython_DHT
# Python => PI + DHT22 sensor guide - https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

from datetime import datetime
import logging
import json

pin = input('Enter the PIN name: ') or 12
if not isinstance(pin, int):
    pin = int(pin)
name = input('Enter the Sensors name: ') or "Empty"

debug_on = input('Enter Debug Mode? ') or False

def write_to_JSON(filePath, newData):
    with open(file=filePath, mode='r') as f:
        data = f.read()

    # Add robustness in case the file is not in the correct format

    obj = json.loads(data)

    obj['records'].append(newData)

    with open(filePath, 'w') as f:
        json.dump(obj, f)

running_flag = True

if not debug_on:
    import adafruit_dht as dht
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    device = dht.DHT22(pin=pin)
else:
    counter = 0

while running_flag:

    if not debug_on:
        temperature = device.temperature

        humidity = device.humidity

    else:
        temperature = 21
        humidity = 0.6
        counter = counter + 1
        if (counter > 5):
            running_flag = False

    newData = {
        "name": "Sensor1",
        "data": [temperature,humidity],
        "time": datetime.now().timestamp()
    }

    filePath = "wiredandtiredIDTP/records/record.json"

    # Call writing function
    write_to_JSON(filePath, newData)

    