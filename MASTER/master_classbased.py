import customtkinter as ctk
import paho.mqtt.client as MqttClient
import json
import threading
from datetime import datetime as dt

class consoleColors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'
    ERROR = '\033[91m'

class Globals():
    def __init__(self):
        global CONNECTED

    def getConn():
        return CONNECTED

    def setConn(value):
        CONNECTED = value

class Client(MqttClient.Client):
    def __init__(self, callbackAPI, app):
        super().__init__(callbackAPI)

        # Declare the interface variable so we can change the interface from this class
        self.interface = app

        # Local Details
        broker_address = "localhost"
        port = 1883
        user = "master"
        password = "mast3r"
        global Connected

        self.username_pw_set(user,password=password)

        self.on_connect = self.on_client_connect
        self.on_message = self.on_client_message

        try:
            # Connect to the MQTT server
            connect_code = self.connect(broker_address, port=port)

            # Method is already multi-threaded
            self.loop_start()
        except Exception as e:
            print(f'{consoleColors.ERROR}ERROR: Could not connect to broker{consoleColors.ENDC}')
            self.interface.stop_client()

    def on_client_connect(self,userdata,flags,rc,properties):
        if rc == 0:
            self.subscribe("root/master")

            Connected = True

            self.interface.update_master_node(self.interface,True)

            print(f'{consoleColors.OK}SUCCESS: Connected to Broker{consoleColors.ENDC}')
        else:
            print(f'{consoleColors.ERROR}ERROR: Connection Failed to Broker{consoleColors.ENDC}')
            self.interface.stop_client()

    def on_client_message(self,userdata,message):
        try:
            json_message = message.payload.decode("utf-8")
            parsed_JSON = json.loads(str(json_message))
        except Exception as e:
            parsed_json = None



class App(ctk.CTk):

    # good_color = '#57FF97'
    # bad_color = '#FF5757'

    def __init__(self):
        super().__init__()

        self.good_color = '#57FF97'
        self.bad_color = '#FF5757'

        global Connected
        self.client_thread = None

        self.title('Sensor Interface')
        self.geometry('1100x700')

                
        self.resizable(width=False,height=False)
        self.configure(bg='#252525')

        self.menu = ctk.CTkFrame(master=self,width=270,height=700,fg_color='#323232')
        self.menu.place(x=0,y=0)
        self.status_frame = ctk.CTkFrame(master=self,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525')
        self.status_frame.place(x=270,y=0)
        self.button_frame = ctk.CTkFrame(master=self,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525')
        self.button_frame.place(x=686,y=0)
        self.readings_frame = ctk.CTkFrame(master=self,width=830,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525')
        self.readings_frame.place(x=270,y=350)

        # Menu

        self.titleLbl = ctk.CTkLabel(master=self.menu,font=('Helvetica', 28, 'bold'),text='W&T Sensor Panel',text_color=self.good_color,fg_color='#323232')
        self.titleLbl.place(x=10,y=12)

        self.menu_item_1 = ctk.CTkFrame(master=self.menu,width=270,height=62,fg_color='#4D4D4D').place(x=0,y=62)
        self.menu_item_1_lbl = ctk.CTkLabel(master=self.menu_item_1,text='Home',width=136,font=('Helvetica', 22, 'bold'),text_color=self.good_color,justify='left',anchor='w',fg_color='#4D4D4D').place(x=72,y=80)

        self.quit_button = ctk.CTkButton(master=self.menu,text='QUIT',font=('Helvetica', 24, 'bold'),border_color=self.good_color,border_width=1,fg_color='#323232',bg_color='#323232',width=212,height=60,corner_radius=28,hover_color='#9F9F9F',command=quit)
        self.quit_button.place(x=28,y=588)

        # Status Frame
        self.started_since = ctk.StringVar()
        self.started_since.set('Offline')
        self.server_stat_var = ctk.StringVar()
        self.server_stat_var.set('Offline')


        self.server_stat_lbl = ctk.CTkLabel(master=self.status_frame,text='Server Status: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=196,anchor='w')
        self.server_stat_lbl.place(x=44,y=58)
        self.server_stat = ctk.CTkLabel(master=self.status_frame,textvariable=self.server_stat_var,font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.server_stat.place(x=258,y=58)

        # server_stat = CustomLabel((528,58),server_stat_var,status_frame)
        self.server_since_lbl = ctk.CTkLabel(master=self.status_frame,text='Since: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=50,anchor='w')
        self.server_since_lbl.place(x=78,y=86)
        self.server_since = ctk.CTkLabel(master=self.status_frame,textvariable=self.started_since,font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.server_since.place(x=258,y=86)

        self.master_node_lbl = ctk.CTkLabel(master=self.status_frame,text='Master Node Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w')
        self.master_node_lbl.place(x=44,y=114)
        self.master_node_var = ctk.StringVar(master=self.status_frame)
        self.master_node_var.set('Offline')
        self.master_node = ctk.CTkLabel(master=self.status_frame,textvariable=self.master_node_var,font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.master_node.place(x=258,y=114)

        self.sensors_lbl = ctk.CTkLabel(master=self.status_frame,text='Sensors Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w')
        self.sensors_lbl.place(x=44,y=180)
        self.sensors_num = ctk.CTkLabel(master=self.status_frame,text='0',font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.sensors_num.place(x=258,y=180)

        self.actuators_lbl = ctk.CTkLabel(master=self.status_frame,text='Actuators Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w')
        self.actuators_lbl.place(x=44,y=204)
        self.actuators_num = ctk.CTkLabel(master=self.status_frame,text='0',font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.actuators_num.place(x=258,y=204)

        # Button Frame

        self.server_lbl = ctk.CTkLabel(master=self.button_frame,text='Server',font=('Helvetica', 24, 'bold'),fg_color='#252525')
        self.server_lbl.place(x=34,y=54)

        self.start_button = ctk.CTkButton(master=self.button_frame,text='Start',font=('Helvetica', 16, 'bold'),border_color=self.good_color,border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#00993b',command=self.start_client)
        self.stop_button = ctk.CTkButton(master=self.button_frame,text='Stop',font=('Helvetica', 16, 'bold'),border_color=self.bad_color,border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#cc0000',command=self.stop_client)

        self.start_button.place(x=148,y=48)
        self.stop_button.place(x=248,y=48)
        # Readings Frame

        self.lbl = ctk.CTkLabel(master=self.readings_frame,text='Incoming Payloads:',font=('Helvetica', 16, 'bold'),justify='left',anchor='w',fg_color='#252525')
        self.lbl.place(x=28,y=36)

        self.readings_box = ctk.CTkTextbox(master=self.readings_frame,width=784,height=258,fg_color='#353535')
        self.readings_box.configure(state=ctk.DISABLED)
        self.readings_box.place(x=28,y=76)

    def start_client(self):
        print('Server Started')
        self.update_server_status(True)

        try:
            self.client_thread = threading.Thread(target=lambda : {Client(MqttClient.CallbackAPIVersion.VERSION2,self)})
            # client = Client(MqttClient.CallbackAPIVersion.VERSION2)
            self.client_thread.start()
        except Exception as e:
            print(e.with_traceback())

    def stop_client(self):
        print('Stopping Server')
        self.update_server_status(False)

    def update_server_status(self, online):
        if online:
            self.server_stat_var.set('Online')
            self.server_stat.configure(text_color=self.good_color)

            self.started_since.set(f'{dt.now().strftime('%d/%m/%Y - %H:%M')}')
            self.server_since.configure(text_color=self.good_color)
        else:
            self.server_stat_var.set('Offline')
            self.server_stat.configure(text_color=self.bad_color)

            self.started_since.set('Offline')
            self.server_since.configure(text_color=self.bad_color)

    def update_master_node(self,online):
        if online:
            self.master_node_var.set('Online')
            self.master_node.configure(text_color=self.good_color)

        else:
            self.master_node_var.set('Offline')
            self.master_node.configure(text_color=self.bad_color)

app = App()

app.mainloop()