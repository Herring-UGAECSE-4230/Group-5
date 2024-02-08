import RPi.GPIO as GPIO
from datetime import datetime
# Initalizes the SSDs pins
ssd_pins = []
ssd_dot = 3

GPIO.setup(ssd_pins, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(ssd_dot, GPIO.OUT, initial = GPIO.LOW)

# Since that only the pound key '#' will be used, the only two pins from 
# the keypad that will be used will be for row 1 and column 3.

keypadRow1Pin = 4
keypadColumn3Pin = 5

# Defines each number so that the GPIO can send out the correct signals
# to each pin to display said number on the SSD.

sevenSegment0 = (1,1,1,1,1,1,0)
sevenSegment1 = (0,1,1,0,0,0,0)
sevenSegment2 = (1,1,0,1,1,0,1)
sevenSegment3 = (1,1,1,1,0,0,1)
sevenSegment4 = (0,1,1,0,0,1,1)
sevenSegment5 = (1,0,1,1,0,1,1)
sevenSegment6 = (0,0,1,1,1,1,1)
sevenSegment7 = (1,1,1,0,0,0,0)
sevenSegment8 = (1,1,1,1,1,1,1)
sevenSegment9 = (1,1,1,0,0,1,1)



# Variable will change if '#' on the keypad is pressed
isOn = True
isPM = False

while True:
    # Gets the current time
    GPIO.output(keypadRow1Pin, GPIO.HIGH)
    now = datetime.now()

    # Checks if it is currently PM (if the hour variable past 12).
    if now.hour - 12 >= 0:
        isPM = True
        now.hour - 12
        GPIO.output(ssd_dot, GPIO.HIGH)
    else:
        isPM = False
        GPIO.output(ssd_dot, GPIO.LOW)

    # Formats the hour and minute to become strings
    hour = '{0:02d}'.format(now.hour)
    minute = '{0:02d}'.format(now.minute)


    # Sends data out to SSDs

    

    #If the '#' key was pressed, turns the ssds on and off
    if GPIO.input(keypadColumn3Pin) == GPIO.HIGH:
        if (isOn):
            #Turn SSDs off
            isOn = False
        else:
            #Turn SSDs on
            isOn = True
    GPIO.output(keypadRow1Pin, GPIO.LOW)







    




