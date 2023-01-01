from tkinter import *
import threading
import socket


def runserver():
        #####################
        serverip = '192.168.1.106'
        port = 9000
        #####################

        buffsize = 4096

        while True:
                server = socket.socket()
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
                server.bind((serverip,port))
                server.listen(1)
                print('waiting micropython...')

                client, addr = server.accept()
                print('connected from:', addr)

                data = client.recv(buffsize).decode('utf-8')
                print('Data from MicroPython: ',data)
                # data = 'LED1:ON' / 'LED1:OFF'
                data_split = data.split(':')
                if data_split[1] == 'ON':
                    v_status.set('{} status is {}'.format(data_split[0],data_split[1]))
                    L3.configure(fg='green')
                else:
                    v_status.set('{} status is {}'.format(data_split[0],data_split[1]))
                    L3.configure(fg='red')

                #wifistatus = client.recv(buffsize).decode('utf-8')
                #print('Wifi status from MicroPython: ',wifistatus)
                ## data = 'connecting to network' / 'wifi is connected'
                #if wifistatus == 'wifi is connected':
                #    v_wifi.set('wifi is connected')
                #   L2.configure(fg='green')
                #else:
                #    v_wifi.set('connecting to network')
                #    L2.configure(fg='red')
                    
                client.send('received your messages.'.encode('utf-8'))
                client.close()


GUI = Tk()
GUI.geometry('500x500')
GUI.title('LED status from Micropython')

Font = ('Angsana New',30)

# ข้อความแสดง - ไม่เปลี่ยนแปลง
L1 = Label(GUI,text='LED status from Micropython',font=Font)
L1.pack()

v_wifi = StringVar()
v_wifi.set('wifi is not connected')
L2 = Label(GUI,textvariable=v_wifi,font=Font)
L2.configure(fg='red')
L2.pack()


# ข้อความแสดง - มีเปลี่ยนแปลง
v_status = StringVar() # ตัวแปรเก็บค่าสถานะ
v_status.set('<<< No Status >>>')
L3 = Label(GUI,textvariable=v_status,font=Font)
L3.configure(fg='red')
L3.pack()


#################### RUNSERVER #####################
task = threading.Thread(target=runserver)
task.start()
#################### RUNSERVER #####################


GUI.mainloop()