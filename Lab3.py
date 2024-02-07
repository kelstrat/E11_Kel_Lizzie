# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

# pylint: disable=unused-import
import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import csv

#create file and meta data list
meta_data = ["Time", "PM10", "PM25", "PM100"]
file = open("air_quality_data.csv", "w", newline = '')

#make a writer to write into the file
data_writer = csv.writer(file)
data_writer.writerow(meta_data)



reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)


print("Found PM2.5 sensor, reading data...")

#starting time
start = time.time()

while ((time.time() - start) < 30):
    time.sleep(1)

    #makes sure the sensor isn't erroring
    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    #collect our data points
    time_data = time.time()
    pm10_data = aqdata["pm10 standard"]
    pm25_data = aqdata["pm25 standard"]
    pm100_data = aqdata["pm100 standard"]
    
    #put into a single line of data to put into the CSV file
    data_line = [time_data, pm10_data, pm25_data, pm100_data]
    
    #write into csv
    data_writer.writerow(data_line)



    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )

