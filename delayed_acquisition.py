import sys
import random
import time
import csv
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

#import sensor packages
import adafruit_bme680
from adafruit_pm25.uart import PM25_UART


#creating start time, grabbing user imputted run time
start_time = time.time()
run_time = int(sys.argv[1])
now = start_time
delay_time = int(sys.argv[2])

#creating file and file writer according to user imput
filename = "/home/pi/" + sys.argv[3] + ".csv"
file = open(filename, "w", newline ='')
dwriter = csv.writer(file)

#writing metadata of the CSV
metadata = ["Time", "PM10", "PM25", "PM100", "Temperature", "Gas", "Humidity","Pressure", "Altitude"]
dwriter.writerow(metadata)


#create sensor objects

#bme680 Pressure, temp, gas, etc. sensor
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)
#setting location sea level pressure (hPa)
bme680.sea_level_pressure = 1013.25



#pm25 Air Quality Sensor
reset_pin = None
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin)


while ((now - start_time) < run_time):
    time.sleep(1)
    
    #update current time
    now = time.time()
    
    #collect our data points
    if (now - start_time) > delay_time:

        #air quality data
        aqdata = pm25.read()
        pm10 = aqdata["pm10 standard"]
        pm25_data = aqdata["pm25 standard"]
        pm100 = aqdata["pm100 standard"]

        #PTH data
        temp = round(bme680.temperature, 1)
        gas = round(bme680.gas, 1)
        humidity = round(bme680.relative_humidity, 1)
        pressure = round(bme680.pressure, 3)
        altitude = round(bme680.altitude, 2)

        #put into a single line of data to put into the CSV file
        datalist = [now, pm10, pm25_data, pm100, temp, gas, humidity, pressure, altitude]

        #write into CSV
        dwriter.writerow(datalist)
        print(datalist)

file.close()
