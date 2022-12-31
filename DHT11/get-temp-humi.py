import dht
import machine
import time

d = dht.DHT11(machine.Pin(21))
rtc = machine.RTC()


while True:  
    now = rtc.datetime() # get date and time
    d.measure()
    time.sleep(1)
    d.temperature() # eg. 23 (°C)
    d.humidity()    # eg. 41 (% RH)
    
    print("Date: {}/{}/{}".format(now[2], now[1], now[0]))
    print("Time: {}:{}:{}".format(now[4], now[5], now[6]))
    
    print('Temperature: ' + str(d.temperature()) + ' °C')
    print('Humidity: ' + str(d.humidity()) + '% RH ')
