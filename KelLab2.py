import adafruit_bme680
import time
import board

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # uses board.SCL and board.SDA
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

#keep track of the time the sensor starts taking data
start_time = time.time()

#keep track of an print the data
data_output = []

#run for 10 seconds
while (time.time() - start_time < (10)):
    time = time.localtime(time().time)
    temp = round(bme680.temperature, 1)
    gas = round(bme680.gas, 1)
    humidity = round(bme680.relative_humidity, 1)
    pressure = round(bme680.pressure, 3)
    altitude = round(bme680.altitude, 2)

    data_line = f"{time} | {temp} C, {gas} ohm, {humidity} %, {pressure} hPa, {altitude} meters"
    data_output.append(data_line) 

    #print("\nTemperature: %0.1f C" % bme680.temperature)
    #print("Gas: %d ohm" % bme680.gas)
    #print("Humidity: %0.1f %%" % bme680.relative_humidity)
    #print("Pressure: %0.3f hPa" % bme680.pressure)
    #print("Altitude = %0.2f meters" % bme680.altitude)
    #print("Time:", time.localtime(time().time))

    time.sleep(2)

#need python3 for this so not sure if it would work! just got from looking up stuff
print(*data_output, sep = '\n')