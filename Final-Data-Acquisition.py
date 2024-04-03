import sys
import random
import time
import csv
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_bme680
from adafruit_pm25.uart import PM25_UART
import RPi.GPIO as GPIO

#creating start time, grabbing user inputted run time
start_time = time.time()
run_time = int(sys.argv[1])
now = start_time
count_time = int(sys.argv[2])

#creating file and file writer according to user input
filename = "/home/pi/" + sys.argv[3] + ".csv"
file = open(filename, "w", newline ='')
dwriter = csv.writer(file)

#writing metadata of the CSV
metadata = ["Time", "CPM", "PM10", "PM25", "PM100", "Temperature", "Gas", "Humidity","Pressure", "Altitude"]
dwriter.writerow(metadata)


#create sensor objects
###################################### AQ and PTH Sensors ####################################################

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

###################################### Radiation Sensor ####################################################

#create callback function
def my_callback(channel):
    print('\n* Interaction detected at ' + str(time.time()))
    global cpm
    cpm +=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.add_event_detect(17, GPIO.FALLING, callback = my_callback)

#variable to keep track of how long to track for cpm
cpm_counter = time.time()
cpm_data = 0
cpm = 0

#collect first data point for PTH but dont write in because its weird
temp_data = round(bme680.temperature, 1)
gas_data = round(bme680.gas, 1)
humidity_data = round(bme680.relative_humidity, 1)
pressure_data = round(bme680.pressure, 3)
altitude_data = round(bme680.altitude, 2)

while ((now - start_time) < run_time):
    time.sleep(1)
    
    #air quality data
    aqdata = pm25.read()
    pm10_data = aqdata["pm10 standard"]
    pm25_data = aqdata["pm25 standard"]
    pm100_data = aqdata["pm100 standard"]

    #PTH data
    temp_data = round(bme680.temperature, 1)
    gas_data = round(bme680.gas, 1)
    humidity_data = round(bme680.relative_humidity, 1)
    pressure_data = round(bme680.pressure, 3)
    altitude_data = round(bme680.altitude, 2)
    
    #radiation data
    if (now - cpm_counter >= count_time):
        print(cpm, f"\n counts in {count_time} seconds")
        cpm_data = cpm
        cpm_counter = time.time()
        cpm = 0
    
    #collect and write data to CSV
    time_data = time.time()
    datalist = [time_data, cpm_data, pm10_data, pm25_data, pm100_data, temp_data, gas_data, humidity_data, pressure_data, altitude_data]
    
    dwriter.writerow(datalist)
    print()
    print(datalist)
    
    #reset variables for the loop
    now = time.time()

file.close()
