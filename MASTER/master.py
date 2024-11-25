import paho.mqtt.client as mqttClient
import time
import json
from datetime import datetime
import threading

# GLOBAL VARIABLES
global Connecting
Connecting = False
global Terminate
Terminate = False


# THIS FILE IS FOR THE MASTER NODE WHICH WILL BE RECIEVING DATA FROM THE PUPPETS

now = str(datetime.now())

class console_colours:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    ERROR = '\033[91m'

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        client.subscribe("root/mstnode")

        global connected
        connected = True

        print(console_colours.OK + "SUCCESS: Connected to Broker" + console_colours.ENDC)
    else:
        print(console_colours.ERROR + "ERROR: Connection Failed" + console_colours.ENDC)

def on_message(client, userdata, message):
    # Save Message Contents
    # Contains:
        # name  : String    - The name of the sensor/device that the information came from
        # value : Any       - The returned value from the device or sensor. Possibly in Array format if sensor is returning multiple readings
        # type  : String    - The type of sensor reading being recorded (Temperature, Water Level, Fan Speed, etc.). Possibly in Array format if sensor is returning multiple readings
        # time  : Integer   - The timestamp of the moment of capture related to the data from sensor
    
    try:
        json_message = message.payload.decode("utf-8")
        parsed_JSON = json.loads(str(json_message))

        # Sort for displaying on interface
        name = parsed_JSON['name']
        value = parsed_JSON['value']
        unit = parsed_JSON['type']
        time = parsed_JSON['time']

    except Exception as e:
        parsed_JSON = None
        name = None
        value = None
        time = None
        print(console_colours.ERROR + "ERROR: Could not parse message" + console_colours.ENDC)

def write_data(entry, file):
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(console_colours.WARNING + "ERROR: JSON File not formatted correctly." + console_colours.ENDC)
    
    try:
        with open(file, "w") as f:
            data[len(data)] = entry
            f.write(data)
    except FileNotFoundError:
        print(console_colours.ERROR + "ERROR: File not Found." + console_colours.ENDC)
    
    ###

global Connected
Connected = False

# Will store the passed parameters into a .csv file that contains all recent sensor readings from connected nodes
def save_reading(name, value, time, filename="readings.json"):
    entry = {
        "name": name,
        "value": value,
        "time": time
    }

    try:
        # try to open the file
        with open(filename, "r+") as f:
            try:
                read_JSON = json.load(f)
            except json.JSONDecodeError:
                read_JSON = []
    except FileNotFoundError:
            # If file doesn't exist, create new file with initial structure
        read_JSON = []

    read_JSON.append(entry)

    with open(filename, "w") as f:
        json.dump(read_JSON, f, indent=4)

# Sends a message to the MQTT Server and to all nodes, usually to be used for ACK messages with the relevant roomCode supplied
def send_message(client, name, value):
    payload = [name, value]
    client.publish("root/mstnode", payload, 0)


# Local Details
broker_address = "localhost"
port = 1883
user = "master"
password = "mast3r"

# Define client object
client = mqttClient.Client(mqttClient.CallbackAPIVersion.VERSION2)

# Set the username and password for the client
client.username_pw_set(user, password=password)

# Link the callback functions to the corresponding defined functions
client.on_connect = on_connect

client.on_message = on_message

def connect_server(client, broker_address, port):


    connect_code = None
        
    try:
        # Connect to the MQTT server
        connect_code = client.connect(broker_address, port=port)
        client.loop_start()
    except Exception:
        print(f'{console_colours.ERROR}ERROR:{console_colours.ENDC} Could not connect to broker')

    # If the connection isn't refused immediately then execute below
    if (connect_code == 0):

        # Wait for the on_connect function to fire, keep notifying the user that the system is trying to connect
        try:
            while Connected != True:
                print(console_colours.WARNING + "WARN: Reattempting Connection" + console_colours.ENDC)
                time.sleep(0.1)
        except KeyboardInterrupt:
            print(console_colours.ERROR + "ERROR: Could not Connect" + console_colours.ENDC)

        # Keep the program looping for the callback functions (on_message)
        try:
            while Terminate == False:
                time.sleep(1)
            # Terminate if the user forcibly closes loop (Also include a condition for if the interface wants to be able to close the listener)
        except KeyboardInterrupt:
            client.disconnect()
            client.loop_stop()
    elif (connect_code == None):
        print(f'{console_colours.ERROR}ERROR:{console_colours.ENDC} Broker not responding')

## CUSTOMTKINTER GUI

# class CustomLabel(ct.CTk):
#     def __init__(self,position,textvar,masterEle):
#         super().__init__()
#         self.label = ct.CTkLabel(self,textvariable=textvar,master=masterEle)
#         self.label.place(position)

#     def update_label_color(self, value):
#         self.label.configure(text_color=value)
#         self.label.update()

import tkinter
import customtkinter as ct

def start_server():
    if Connecting == False:
        started_since.set(f'{datetime.now().hour}:{datetime.now().minute}')
        server_stat_var.set('Online')
        server_stat.update_label_color("green")
        # app.update()
        print(f'{console_colours.OK}Starting Client...{console_colours.ENDC}')
        Connecting = True
        if Terminate == True:
            Terminate = False
        t1 = threading.Thread(target=connect_server, args=(client,broker_address,port))
        t1.start()
    else:
        print(f'{console_colours.WARNING}Client Already starting...{console_colours.ENDC}')

def stop_server():
    print(f'{console_colours.OK}Stopping Client...{console_colours.ENDC}')
    global Terminate
    Terminate = True

app = ct.CTk()
app.geometry('1100x700')
app.title('Sensor Panel')
# ct.set_appearance_mode('dark')

app.resizable(width=False,height=False)
app.configure(bg='#252525')

menu = ct.CTkFrame(master=app,width=270,height=700,fg_color='#323232').place(x=0,y=0)
status_frame = ct.CTkFrame(master=app,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=270,y=0)
button_frame = ct.CTkFrame(master=app,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=686,y=0)
readings_frame = ct.CTkFrame(master=app,width=830,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=270,y=350)

# Menu

titleLbl = ct.CTkLabel(master=menu,font=('Helvetica', 28, 'bold'),text='W&T Sensor Panel',text_color='#57FF97',fg_color='#323232').place(x=10,y=12)

menu_item_1 = ct.CTkFrame(master=menu,width=270,height=62,fg_color='#4D4D4D').place(x=0,y=62)
menu_item_1_lbl = ct.CTkLabel(master=menu_item_1,text='Home',width=136,font=('Helvetica', 22, 'bold'),text_color='#57FF97',justify='left',anchor='w',fg_color='#4D4D4D').place(x=72,y=80)

quit_button = ct.CTkButton(master=menu,text='QUIT',font=('Helvetica', 24, 'bold'),border_color='#57FF97',border_width=1,fg_color='#323232',bg_color='#323232',width=212,height=60,corner_radius=28,hover_color='#9F9F9F',command=quit).place(x=28,y=588)

# Status Frame
started_since = ct.StringVar()
started_since.set(f'00:00')
server_stat_var = ct.StringVar()
server_stat_var.set('Offline')


server_stat_lbl = ct.CTkLabel(master=status_frame,text='Server Status: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=196,anchor='w').place(x=314,y=58)
server_stat = ct.CTkLabel(master=status_frame,textvariable=server_stat_var,font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=58)

# server_stat = CustomLabel((528,58),server_stat_var,status_frame)
server_since_lbl = ct.CTkLabel(master=status_frame,text='Since: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=50,anchor='w').place(x=375,y=86)
server_since = ct.CTkLabel(master=status_frame,textvariable=started_since,font=('Helvetica', 16),text_color='#57FF97',fg_color='#252525',justify='right',anchor='e').place(x=528,y=86)


master_node_lbl = ct.CTkLabel(master=status_frame,text='Master Node Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=114)
master_node = ct.CTkLabel(master=status_frame,text='Offline',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=114)

sensors_lbl = ct.CTkLabel(master=status_frame,text='Sensors Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=180)
sensors_num = ct.CTkLabel(master=status_frame,text='0',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=180)

actuators_lbl = ct.CTkLabel(master=status_frame,text='Actuators Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=204)
actuators_num = ct.CTkLabel(master=status_frame,text='0',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=204)

# Button Frame

server_lbl = ct.CTkLabel(master=button_frame,text='Server',font=('Helvetica', 24, 'bold'),fg_color='#252525').place(x=720,y=54)

start_button = ct.CTkButton(master=button_frame,text='Start',font=('Helvetica', 16, 'bold'),border_color='#57FF97',border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#00993b',command=start_server)
stop_button = ct.CTkButton(master=button_frame,text='Stop',font=('Helvetica', 16, 'bold'),border_color='#FF5757',border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#cc0000',command=stop_server).place(x=970,y=48)


# start_button.configure(command=lambda arg1=Connecting, arg2=Terminate, arg3=server_stat : start_server(arg1,arg2,arg3))

start_button.place(x=868,y=48)
# Readings Frame

lbl = ct.CTkLabel(master=readings_frame,text='Incoming Payloads:',font=('Helvetica', 16, 'bold'),justify='left',anchor='w',fg_color='#252525').place(x=298,y=386)

readings_box = ct.CTkTextbox(master=readings_frame,width=784,height=258,fg_color='#353535').place(x=298,y=418)

app.mainloop()