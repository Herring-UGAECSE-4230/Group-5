import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Initalizes the SSDs pins
#           A   B   C  D   E   F   G
ssd_pins = [22, 18, 5, 25, 24, 27, 17]
ssd_dot = 6

GPIO.setup(ssd_pins, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(ssd_dot, GPIO.OUT, initial = GPIO.LOW)

# Since that only the pound key '#' will be used, the only two pins from 
# the keypad that will be used will be for row 1 and column 3.

keypadRow1Pin = 21
keypadColumn3Pin = 19

GPIO.setup(keypadRow1Pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(keypadColumn3Pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


# Sets the clock pins for the DFFs

clock1pin = 23
clock2pin = 4
clock3pin = 3
clock4pin = 2

GPIO.setup(clock1pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock2pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock3pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock4pin, GPIO.OUT, initial = GPIO.LOW)

clk1 = GPIO.PWM(clock1pin, 100)
clk2 = GPIO.PWM(clock2pin, 100)
clk3 = GPIO.PWM(clock3pin, 100)
clk4 = GPIO.PWM(clock4pin, 100)

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

# Sends binary data to SSDs
def sendToSSD(curVal):
    if (curVal == '0'):
        GPIO.output(ssd_pins, sevenSegment0)
    if (curVal == '1'):
        GPIO.output(ssd_pins, sevenSegment1)
    if (curVal == '2'):
        GPIO.output(ssd_pins, sevenSegment2)
    if (curVal == '3'):
        GPIO.output(ssd_pins, sevenSegment3)
    if (curVal == '4'):
        GPIO.output(ssd_pins, sevenSegment4)
    if (curVal == '5'):
        GPIO.output(ssd_pins, sevenSegment5)
    if (curVal == '6'):
        GPIO.output(ssd_pins, sevenSegment6)
    if (curVal == '7'):
        GPIO.output(ssd_pins, sevenSegment7)
    if (curVal == '8'):
        GPIO.output(ssd_pins, sevenSegment8)
    if (curVal == '9'):
        GPIO.output(ssd_pins, sevenSegment9)

# Variable will change if '#' on the keypad is pressed
isOn = True
isPM = False

# Starts the clks

clk1.start(50)
clk2.start(50)
clk3.start(50)
clk4.start(50)

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
    sendToSSD(hour[0])
    sendToSSD(hour[1])
    sendToSSD(minute[0])
    sendToSSD(minute[1])

    #If the '#' key was pressed, turns the ssds on and off
    if GPIO.input(keypadColumn3Pin) == GPIO.HIGH:
        if (isOn):
            #Turn SSDs off
            isOn = False
            GPIO.output(ssd_pins, GPIO.LOW)

        else:
            #Turn SSDs on
            isOn = True
            GPIO.output(ssd_pins, GPIO.HIGH)

    GPIO.output(keypadRow1Pin, GPIO.LOW)







    




