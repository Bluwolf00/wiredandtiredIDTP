import paho.mqtt.client as mqttClient
import time
import json
from datetime import datetime

now = str(datetime.now())

class console_colours:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    ERROR = '\033[91m'

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        client.subscribe("root/msr")

        global connected
        connected = True

        print(console_colours.OK + "SUCCESS: Connected to Broker" + console_colours.ENDC)
    else:
        print(console_colours.ERROR + "ERROR: Connection Failed" + console_colours.ENDC)

def on_message(client, userdata, message):
    # Save Message Contents
    # Contains:
        # name  : String    - The name of the sensor/device that the information came from
        # value : Any       - The returned value from the device or sensor
        # type  : ENUM      - The type of sensor reading being recorded (Temperature, Water Level, Fan Speed, etc.)
        # unit  : String    - The unit of measurement for the recorded data
    
    try:
        parsed_JSON = json.loads(str(message.payload.decode("utf-8")))

        # Sort for displaying on interface
        name = parsed_JSON['name']
        value = parsed_JSON['value']
        unit = parsed_JSON['unit']
        time = message.timestamp

    except Exception as e:
        parsed_JSON = None
        name = None
        value = None
        time = None
        print(console_colours.ERROR + "ERROR: Could not parse message" + console_colours.ENDC)

def write_data(entry, file):
    try:
        with open("nodes.json", "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(console_colours.WARNING + "ERROR: JSON File not formatted correctly." + console_colours.ENDC)
    
    try:
        with open("nodes.json", "w") as f:
            data[len(data)] = entry
            f.write(data)
    except FileNotFoundError:
        print(console_colours.ERROR + "ERROR: File not Found." + console_colours.ENDC)
    
    ###

global Connected
Connected = False

# Will store the passed parameters into a .csv file that contains all recent sensor readings from connected nodes
def save_reading(name, room_node, device_name, device_value, time, filename="readings.json"):
    entry = {
        "name": name,
        "roomNode": room_node,
        "value": device_value,
        "deviceName": device_name,
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
def send_message(client, room_code, value):
    payload = [room_code, value]
    client.publish("root/masterInstr", payload, 0)


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

# Connect to the MQTT server
connect_code = client.connect(broker_address, port=port)
client.loop_start()

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
        while True:
            time.sleep(1)
    # Terminate if the user forcibly closes loop (Also include a condition for if the interface wants to be able to close the listener)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()