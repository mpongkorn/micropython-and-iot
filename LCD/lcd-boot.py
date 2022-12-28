# MicroPython and IoT - EP.10

import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

print(i2c.scan()) #scan ตัวเลข address ของ lcd จากนั้นต้องแปลงเป็น hex
print('Address: ', hex(i2c.scan()[0]))

lcd = I2cLcd(i2c, 0x27, 2, 16) # 2 บรรทัด 16 ตัวอักษร

# String
#lcd.putstr('Happy New Year\n2023')

# CHAR from ROM
# lcd.putstr(chr(int(0b01111110))) # 0b นำหน้า binary

#custom char 0-7
smile = bytearray([0x00, 0x00, 0x0A, 0x00, 0x00, 0x11, 0x0E, 0x00])
angry = bytearray([0x00, 0x00, 0x0A, 0x00, 0x0E, 0x11, 0x00, 0x00])

lcd.custom_char(0, smile)
lcd.custom_char(1, angry)

lcd.putstr(chr(0))

lcd.move_to(15,0) # move to column 16 (index 15) row 1 (index 0)
lcd.putstr(chr(1))

#lcd.backlight_off() # ปิด back light ของจอ

for i in range(10):
    lcd.display_off()
    time.sleep(1)
    lcd.display_on()
    time.sleep(1)
    
    


