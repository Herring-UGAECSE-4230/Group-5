import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3,GPIO.OUT, initial=GPIO.LOW)


while True:
    sleep(0.00001)
    GPIO.output(3, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(3, GPIO.LOW)