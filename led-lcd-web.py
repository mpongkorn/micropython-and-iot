from machine import Pin, SoftI2C
import network
import time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import socket
import _thread


#LED
led = Pin(13, Pin.OUT)
led.value(1) #turn OFF led


#LCD
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # 2 บรรทัด 16 ตัวอักษร
time.sleep(1)
lcd.clear()

text = 'Starting...'
lcd.putstr(text)


#CONNECT WIFI
wifi = 'Invincible_2.4G'
password = 'Oj81wN69'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
time.sleep(2)
wlan.connect(wifi, password)
time.sleep(2)
status = wlan.isconnected()
print(status)
ip, _, _, _ = wlan.ifconfig() # _ คือตัวแปรที่ไม่ได้ใช้
print(ip)

if status == True:
    lcd.clear()
    text = 'IP:{}'.format(ip)
    lcd.putstr('Wifi connected')
    lcd.move_to(0,1)
    lcd.putstr(text)
else:
    lcd.clear()
    lcd.putstr('Cannot connect')
    lcd.move_to(0,1)
    lcd.putstr('Invincible 2.4G')

html = '''

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Hugo 0.84.0">
    <title>ESP32 - Status</title>
    <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/pricing/">
  <link href="https://getbootstrap.com/docs/5.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  </head>
  <body>
  <div class="container">
  <form>
    <center>
      <img src="https://raw.githubusercontent.com/UncleEngineer/MicroPython-IoT/main/light-bulb-on.png" width="300">
     <h3>LED 1</h3>
          <button  class="btn btn-primary" name="LED" value="ON" type="submit">ON</button>&nbsp;
        <button  class="btn btn-danger" name="LED" value="OFF" type="submit">OFF</button>
    </center>
   </form>
  </div>
    
  </body>
</html>
'''

html_off = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">
    <meta name="generator" content="Hugo 0.84.0">
    <title>ESP32 - Status</title>
    <link rel="canonical" href="https://getbootstrap.com/docs/5.0/examples/pricing/">
  <link href="https://getbootstrap.com/docs/5.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  </head>
  <body>
  <div class="container">
  <form>
    <center>
      <img src="https://raw.githubusercontent.com/UncleEngineer/MicroPython-IoT/main/light-bulb-off.png" width="300">
     <h3>LED 1</h3>
          <button class="btn btn-primary" name="LED" value="ON" type="submit">ON</button>&nbsp;
        <button class="btn btn-danger" name="LED" value="OFF" type="submit">OFF</button>
    </center>
    </form>
  </div>
    
  </body>
</html>

'''

global led_status
led_status = 'OFF'

def runserver():
    global led_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP/IP , UTP
    host = ''
    port = 80 #default port of HTTP
    s.bind((host,port))
    s.listen(5)

    led_status = 'OFF'

    while True:
        client, addr = s.accept()
        print('Connection from: ', addr)
        data = client.recv(1024).decode('utf-8')
        print([data]) # list of data
        
        # check led status
        try:
            
            check = data.split()[1].replace('/','').replace('?','')
            print('CHECK: ', check)
            
            if check != '':
                led_name, led_value = check.split('=')
                if led_value == 'ON':
                    print('TURN ON LED')
                    led.value(0)
                    client.send(html)
                    client.close()
                    lcd.clear()
                    lcd.putstr('{}: TURNED {}'.format(led_name, led_value))
                    led_status = 'ON'
                    
                elif led_value == 'OFF':
                    print('TURN OFF LED')
                    led.value(1)
                    client.send(html_off)
                    client.close()
                    lcd.clear()
                    lcd.putstr('{}: TURNED {}'.format(led_name, led_value))
                    led_status = 'OFF'
            else:
                if led_status == 'OFF':
                    client.send(html_off)
                elif led_status == 'ON':
                    client.send(html)
                    
        except:
            pass

def loop_led():
    global led_status
    led_name = 'LED'
    for i in range(100):        
        led.value(0)
        lcd.clear()
        lcd.putstr('{}: ON (AUTO)'.format(led_name))
        led_status = 'ON'
        time.sleep(10)
        
        led.value(1)
        lcd.clear()
        lcd.putstr('{}: OFF'.format(led_name))
        led_status = 'OFF'
        time.sleep(10)


_thread.start_new_thread(runserver,()) # start thread ทำให้โปรแกรม run parallel ได้
_thread.start_new_thread(loop_led,())
    
    
    
