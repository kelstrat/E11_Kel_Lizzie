import time

import RPi.GPIO as GPIO
 
def radiation_callback(channel):
    if GPIO.input(channel) == GPIO.LOW:
        print('\n* Interraction detected at ' + str(time.time()))
 
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.IN)
    GPIO.add_event_detect(17, GPIO.LOW, callback=radiation_callback)
 
    message = raw_input('\nPress any key to exit.\n')

#GPIO.wait_for_edge(channel, GPIO.FALLING)
 
finally:
    GPIO.cleanup()