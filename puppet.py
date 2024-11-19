# This file is responsible for the puppet nodes which are directly connected to the sensors
# Possible library to be used for interfacing with the DHT22 - https://github.com/adafruit/Adafruit_CircuitPython_DHT
# Python => PI + DHT22 sensor guide - https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/

from datetime import datetime
import logging
import json
import random
import time
import tkinter as tk
from tkinter import ttk
import ttkthemes
# import customtkinter as csTk
import threading

def write_to_JSON(filePath, newData):
    with open(file=filePath, mode='r') as f:
        data = f.read()

    # Add robustness in case the file is not in the correct format

    obj = json.loads(data)

    obj['records'].append(newData)

    with open(filePath, 'w') as f:
        json.dump(obj, f, indent=4)

# m = ttkthemes.ThemedTk(screenName=None,baseName=None,className='Tk',useTk=1,theme='equilux')
m = ttkthemes.ThemedTk()
m.title('Sensor Panel')
# print(f'Available Themes: {m.get_themes()}')

def sensor_loop(debug_on, pin, name):

    running_flag = True

    if debug_on == False:
        import adafruit_dht as dht
        import RPi.GPIO as GPIO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        device = dht.DHT22(pin=pin)
    else:
        counter = 0
        device = None

    while running_flag:

        if debug_on == False:
            temperature = device.temperature

            humidity = device.humidity
        else:
            temperature = (random.randrange(1,60))
            humidity = (random.random())
            counter = counter + 1
            if (counter > 5):
                running_flag = False
            print(f'Debug Mode: {debug_on}, Pin: {pin}, Temperature Recorded: {temperature}, Humidity Recorded: {humidity}')
            reading_lists.insert(tk.END,f'Sensor: {name} - Temperature: {temperature} - Humidity: {humidity} - Time: {datetime.now().timestamp().__int__()}\n')

        newData = {
            "name": name,
            "data": [temperature,humidity],
            "time": datetime.now().timestamp().__int__()
        }

        filePath = "wiredandtiredIDTP/records/record.json"

        # Call writing function
        write_to_JSON(filePath, newData)

        # Wait for DHT to refresh
        time.sleep(2)

def start_button():
    print('none')
    name = text_field_1.get()
    debug_on = bool(text_field_2.get())
    pin = int(text_field_3.get())

    t1 = threading.Thread(target=sensor_loop,args=(debug_on,pin,name))
    t1.start()

lbl1 = ttk.Label(m,text='Sensor Name')
lbl1.pack()
text_field_1 = ttk.Entry(m,width=50)
text_field_1.pack()

lbl2 = ttk.Label(m,text='Debug Mode')
lbl2.pack()
text_field_2 = ttk.Entry(m,width=50)
text_field_2.pack()

lbl3 = ttk.Label(m,text='Pin Number')
lbl3.pack()
text_field_3 = ttk.Entry(m,width=50)
text_field_3.pack()

button = ttk.Button(m,text='Run',width=25,command=start_button)
button.pack()

frame = ttk.Frame(m)
frame.pack(fill='both',expand=True)

reading_lists = tk.Text(frame,wrap='none',font=('Helvetica',8))
vsb = ttk.Scrollbar(frame,command=reading_lists.yview,orient='vertical')
reading_lists.configure(yscrollcommand=vsb.set)

frame.grid_rowconfigure(0,weight=1)
frame.grid_columnconfigure(0,weight=1)

vsb.grid(row=0,column=1,sticky="ns")
reading_lists.grid(row=0,column=0,sticky='nsew')

m.geometry('500x500')

m.mainloop()

# pin = input('Enter the PIN name: ') or 12

# if not isinstance(pin, int):
#     pin = int(pin)

# name = input('Enter the Sensors name: ') or "Empty"

# debug_on = input('Enter Debug Mode? ') or False

# running_flag = True

# if not debug_on:
#     import adafruit_dht as dht
#     import RPi.GPIO as GPIO
#     GPIO.setwarnings(False)
#     GPIO.setmode(GPIO.BCM)
#     GPIO.cleanup()
#     device = dht.DHT22(pin=pin)
# else:
#     counter = 0    