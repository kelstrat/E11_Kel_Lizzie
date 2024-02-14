import time
import adafruit_pm25
import csv

meta_data = ["Time", "PM25", "PM10"]

file = open("air_quality_data.csv", "w", newline = '')

data_writer = CSV.writer(file)
data_writerow(meta_data)

while True:
    #get the data and get the timestamp
    # ex. data = pm25.get_data()

    #put your data points into a list 

    #write into file
    #data_writer.writerow(data)

    #wait an amount of seconds
    #time.sleep(2)

