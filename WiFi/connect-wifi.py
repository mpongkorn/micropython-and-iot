import network

wifi = 'Invincible_2.4G'
password = 'Oj81wN69'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(wifi,password)
wlan.isconnected()
wlan.ifconfig()

########
import socket

serverip = '192.168.0.100'
port = 9000

def send_data(data):
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(data.encode('utf-8'))
	data_server = server.recv(1024).decode('utf-8')
	print('Server:' , data_server)
	server.close()

#############
from machine import Pin

led = Pin(21,Pin.OUT)

led.on()
send_data('LED-ON')
led.off()
send_data('LED-OFF')
