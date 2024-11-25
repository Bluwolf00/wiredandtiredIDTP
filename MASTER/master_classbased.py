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

class Client(MqttClient.Client):
    def __init__(self, callbackAPI):
        super().__init__(callbackAPI)

        # Local Details
        broker_address = "localhost"
        port = 1883
        user = "master"
        password = "mast3r"

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

    def on_client_connect(self,userdata,flags,rc,properties):
        if rc == 0:
            self.subscribe("root/master")

            global Connected
            Connected = True

            print(f'{consoleColors.OK}SUCCESS: Connected to Broker{consoleColors.ENDC}')
        else:
            print(f'{consoleColors.ERROR}ERROR: Connection Failed to Broker{consoleColors.ENDC}')

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

        self.title('Sensor Interface')
        self.geometry('1100x700')

                
        self.resizable(width=False,height=False)
        self.configure(bg='#252525')

        self.menu = ctk.CTkFrame(master=self,width=270,height=700,fg_color='#323232').place(x=0,y=0)
        self.status_frame = ctk.CTkFrame(master=self,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=270,y=0)
        self.button_frame = ctk.CTkFrame(master=self,width=416,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=686,y=0)
        self.readings_frame = ctk.CTkFrame(master=self,width=830,height=350,border_width=1,border_color='black',corner_radius=0,fg_color='#252525').place(x=270,y=350)

        # Menu

        self.titleLbl = ctk.CTkLabel(master=self.menu,font=('Helvetica', 28, 'bold'),text='W&T Sensor Panel',text_color=self.good_color,fg_color='#323232').place(x=10,y=12)

        self.menu_item_1 = ctk.CTkFrame(master=self.menu,width=270,height=62,fg_color='#4D4D4D').place(x=0,y=62)
        self.menu_item_1_lbl = ctk.CTkLabel(master=self.menu_item_1,text='Home',width=136,font=('Helvetica', 22, 'bold'),text_color=self.good_color,justify='left',anchor='w',fg_color='#4D4D4D').place(x=72,y=80)

        self.quit_button = ctk.CTkButton(master=self.menu,text='QUIT',font=('Helvetica', 24, 'bold'),border_color=self.good_color,border_width=1,fg_color='#323232',bg_color='#323232',width=212,height=60,corner_radius=28,hover_color='#9F9F9F',command=quit).place(x=28,y=588)

        # Status Frame
        self.started_since = ctk.StringVar()
        self.started_since.set('Offline')
        self.server_stat_var = ctk.StringVar()
        self.server_stat_var.set('Offline')


        self.server_stat_lbl = ctk.CTkLabel(master=self.status_frame,text='Server Status: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=196,anchor='w').place(x=314,y=58)
        self.server_stat = ctk.CTkLabel(master=self.status_frame,textvariable=self.server_stat_var,font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.server_stat.place(x=528,y=58)

        # server_stat = CustomLabel((528,58),server_stat_var,status_frame)
        self.server_since_lbl = ctk.CTkLabel(master=self.status_frame,text='Since: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=50,anchor='w').place(x=375,y=86)
        self.server_since = ctk.CTkLabel(master=self.status_frame,textvariable=self.started_since,font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e')
        self.server_since.place(x=528,y=86)

        self.master_node_lbl = ctk.CTkLabel(master=self.status_frame,text='Master Node Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=114)
        self.master_node = ctk.CTkLabel(master=self.status_frame,text='Offline',font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e').place(x=528,y=114)

        self.sensors_lbl = ctk.CTkLabel(master=self.status_frame,text='Sensors Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=180)
        self.sensors_num = ctk.CTkLabel(master=self.status_frame,text='0',font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e').place(x=528,y=180)

        self.actuators_lbl = ctk.CTkLabel(master=self.status_frame,text='Actuators Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=204)
        self.actuators_num = ctk.CTkLabel(master=self.status_frame,text='0',font=('Helvetica', 16),text_color=self.bad_color,fg_color='#252525',justify='right',anchor='e').place(x=528,y=204)

        # Button Frame

        self.server_lbl = ctk.CTkLabel(master=self.button_frame,text='Server',font=('Helvetica', 24, 'bold'),fg_color='#252525').place(x=720,y=54)

        self.start_button = ctk.CTkButton(master=self.button_frame,text='Start',font=('Helvetica', 16, 'bold'),border_color=self.good_color,border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#00993b',command=self.start_server)
        self.stop_button = ctk.CTkButton(master=self.button_frame,text='Stop',font=('Helvetica', 16, 'bold'),border_color=self.bad_color,border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#cc0000',command=self.stop_server).place(x=970,y=48)


        # start_button.configure(command=lambda arg1=Connecting, arg2=Terminate, arg3=server_stat : start_server(arg1,arg2,arg3))

        self.start_button.place(x=868,y=48)
        # Readings Frame

        self.lbl = ctk.CTkLabel(master=self.readings_frame,text='Incoming Payloads:',font=('Helvetica', 16, 'bold'),justify='left',anchor='w',fg_color='#252525').place(x=298,y=386)

        self.readings_box = ctk.CTkTextbox(master=self.readings_frame,width=784,height=258,fg_color='#353535').place(x=298,y=418)

    def start_server(self):
        print('Server Started')
        self.update_server_status(True)

    def stop_server(self):
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

try:
    t1 = threading.Thread(target=lambda : {Client(MqttClient.CallbackAPIVersion.VERSION2)})
    # client = Client(MqttClient.CallbackAPIVersion.VERSION2)
    t1.start()
except Exception as e:
    print(e.with_traceback())
app = App()

app.mainloop()