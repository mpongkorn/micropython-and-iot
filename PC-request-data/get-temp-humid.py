# get-temp-humid.py
# PC ---> ESP32--(t, h) ---> csv ---> GUI ---> Table

import socket
import threading
import time
import csv
from datetime import datetime

def writecsv(data):
    with open('data.csv','a',newline='',encoding='utf-8') as file: # a คือ append เก็บค่าเรื่อยๆ เป็นการ stamp
        fw = csv.writer(file)
        fw.writerow(data)
        
            
serverip = '192.168.1.105'
port = 80

# get temperature data
def gettemp():
    while True:
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        server.connect((serverip, port))
        server.send('PC|TEMP'.encode('utf-8')) # convert ข้อความธรรมดาเป็น byte
        data = server.recv(1024).decode('utf-8') #recv(1024) = 1024 byte       
        server.close() #ESP32 ไม่เหมาะกับการเปิด server ไว้

        stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # strftime.org
        print(data)
        t,h = data.split('_')
        dt = [stamp,t,h]
        writecsv(dt)
        
        time.sleep(5)

gettemp()
        
        
