import RPi.GPIO as GPIO
import time

telegraph = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(telegraph, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    if GPIO.input(telegraph):
        print("High")
        time.sleep(0.01)
    else:
        print("Low")
        time.sleep(0.01)