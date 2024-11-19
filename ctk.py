import tkinter
import customtkinter as ct

def start_server():
    print('Starting Server')

def stop_server():
    print('Stopping Server')

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

server_stat_lbl = ct.CTkLabel(master=status_frame,text='Server Status: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=196,anchor='w').place(x=314,y=58)
server_stat = ct.CTkLabel(master=status_frame,text='Offline',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=58)
server_since_lbl = ct.CTkLabel(master=status_frame,text='Since: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',width=50,anchor='w').place(x=375,y=86)
server_since = ct.CTkLabel(master=status_frame,text='00:00',font=('Helvetica', 16),text_color='#57FF97',fg_color='#252525',justify='right',anchor='e').place(x=528,y=86)

master_node_lbl = ct.CTkLabel(master=status_frame,text='Master Node Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=114)
master_node = ct.CTkLabel(master=status_frame,text='Offline',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=114)

sensors_lbl = ct.CTkLabel(master=status_frame,text='Sensors Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=180)
sensors_num = ct.CTkLabel(master=status_frame,text='0',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=180)

actuators_lbl = ct.CTkLabel(master=status_frame,text='Actuators Connected: ',font=('Helvetica', 16, 'bold'),justify='left',fg_color='#252525',anchor='w').place(x=314,y=204)
actuators_num = ct.CTkLabel(master=status_frame,text='0',font=('Helvetica', 16),text_color='#FF5757',fg_color='#252525',justify='right',anchor='e').place(x=528,y=204)

# Button Frame

server_lbl = ct.CTkLabel(master=button_frame,text='Server',font=('Helvetica', 24, 'bold'),fg_color='#252525').place(x=720,y=54)

start_button = ct.CTkButton(master=button_frame,text='Start',font=('Helvetica', 16, 'bold'),border_color='#57FF97',border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#00993b',command=start_server).place(x=868,y=48)
stop_button = ct.CTkButton(master=button_frame,text='Stop',font=('Helvetica', 16, 'bold'),border_color='#FF5757',border_width=1,fg_color='#252525',bg_color='#252525',width=92,height=42,corner_radius=20,hover_color='#cc0000',command=stop_server).place(x=970,y=48)

# Readings Frame

lbl = ct.CTkLabel(master=readings_frame,text='Incoming Payloads:',font=('Helvetica', 16, 'bold'),justify='left',anchor='w',fg_color='#252525').place(x=298,y=386)

readings_box = ct.CTkTextbox(master=readings_frame,width=784,height=258,fg_color='#353535').place(x=298,y=418)

app.mainloop()