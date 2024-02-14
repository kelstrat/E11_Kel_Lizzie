import sys
import random
import time
import csv

print(sys.argv)

start_time = time.time()
run_time = int(sys.argv[1])
now = start_time

filename = sys.argv[2] + ".csv"
file = open(filename, "w", newline ='')
dwriter = csv.writer(file)

metadata = ["Time", "Data"]
dwriter.writerow(metadata)

while ((now - start_time) < run_time):
    time.sleep(1)
    data = random.random()
    now = time.time()
    datalist = [now, data]
    dwriter.writerow(datalist)
    print(datalist)

file.close()
