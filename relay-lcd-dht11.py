import dht
import machine
import time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


# DEFINE RELAY
relay = machine.Pin(13,machine.Pin.OUT)
relay.value(1) #initial turn off relay


#RELAY
def relay_on():
    relay.value(0)
    print('Relay: ON')
    
def relay_off():
    relay.value(1)
    print('Relay: OFF')
   
   
   
#TEMPERATURE AND HUMIDITY SENSOR DHT11
d = dht.DHT11(machine.Pin(19))
rtc = machine.RTC()

def get_temp_humid(): 
    now = rtc.datetime() # get date and time
    d.measure()
    time.sleep(1)
    temp = d.temperature() # eg. 23 (°C) #t
    humid = d.humidity()    # eg. 41 (% RH) #h
    text_temp = 'Temp: {:.1f} C'.format(temp) #tp
    text_humid = 'Humid: {:.1f} % RH'.format(humid) #th
    return(text_temp, text_humid, temp, humid)
    
tp, th, t, h = get_temp_humid()



#DEFINE LCD
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)
#print(i2c.scan()) #scan ตัวเลข address ของ lcd จากนั้นต้องแปลงเป็น hex
#print('Address: ', hex(i2c.scan()[0]))
lcd = I2cLcd(i2c, 0x27, 2, 16) # 2 บรรทัด 16 ตัวอักษร

def show_lcd(line1, line2):
    lcd.clear()
    lcd.putstr(line1)
    lcd.move_to(0,1) #lcd.move_to(COLUMN, ROW)
    lcd.putstr(line2)
    
for i in range(10):
    tp, th, t, h = get_temp_humid()
    show_lcd(tp, th)
    if t > 30:
        relay_on()
    else:
        relay_off()
    print(tp)
    print(th)
    time.sleep(1)





