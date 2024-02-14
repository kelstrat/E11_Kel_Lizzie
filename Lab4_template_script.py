import sys
import random
import time
import csv

print(sys.argv)

start_time = time.time()
run_time = 30
now = start_time

filename = "test_data.csv"
file = open(filename, "w", newline ='')
dwriter = csv.writer(file)

metadata = ["Time", "Data"]
dwriter.writerow(metadata)
print(metadata)

while (now - start_time) < run_time:
    time.sleep(1)
    data = random.random()
    now = time.time()
    datalist = [now, data]
    dwriter.writerow(datalist)

file.close()
