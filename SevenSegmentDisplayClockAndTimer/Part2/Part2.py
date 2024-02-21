import RPi.GPIO as GPIO
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Initalizes the SSDs pins
#           A   B   C  D   E   F   G  DP
ssd_pins = [27, 17, 18, 23, 24, 22, 5, 25] 
# Initalize the Keypad Pins
#             x1  x2  x3  x4  y1 y2  y3  y4
keypad_pins = [21, 20, 16, 12, 6, 13, 19, 7]

GPIO.setup(ssd_pins, GPIO.OUT, initial = GPIO.LOW)
# Sets up the output pins for the keypad
GPIO.setup(keypad_pins[0:4], GPIO.OUT, initial = GPIO.LOW)
# Sets up the input pins from the keypad
GPIO.setup(keypad_pins[4:8], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)


# Sets the clock pins for the DFFs

clock1pin = 15
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
sevenSegmentDot = (0,0,0,0,0,0,0,1)
sevenSegmentOff = (0,0,0,0,0,0,0,0)

ssdOn = True
curVal = '0'

keypadMap = [['1', '2', '3', 'A'],

             ['4', '5', '6', 'B'],
             ['7', '8', '9', 'C'],
             ['*', '0', '#', 'D']
            ]

# Copied from Part1.py code
# Returns the button pressed based on the inputted row and
# the characters in said row
def readKeypad(rowNum, rowChar):
    global ssdOn
    global curVal
    
    # Checks if the SSD is on. If it's not, no value will be displayed
    # until '#' is pressed again
    if (not ssdOn):
        curVal = None
    
    # Checks if curVal is still '#' while the SSD is on.
    # To prevent the SSD from turning back off
    if (curVal == '#' and ssdOn):
        curVal = '0'
        
    GPIO.output(rowNum, GPIO.HIGH)

    if (GPIO.input(keypad_pins[4]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[0]
        print(curVal)
    elif (GPIO.input(keypad_pins[5]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[1]
        print(curVal)
    elif (GPIO.input(keypad_pins[6]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[2]
        print(curVal)
    elif (GPIO.input(keypad_pins[7]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[3]
        print(curVal)
        
    GPIO.output(rowNum,GPIO.LOW)

    return curVal

# Copied from Part1.py code
# Helps to prevent debouncing
def debounceLimiter():
    sleep(0.25)

# Sends binary data to SSDs
def sendToSSD(currentVal):
    global ssdOn
    if (ssdOn):
        if (currentVal == '0'):
            GPIO.output(ssd_pins, sevenSegment0)
        if (currentVal == '1'):
            GPIO.output(ssd_pins, sevenSegment1)
        if (currentVal == '2'):
            GPIO.output(ssd_pins, sevenSegment2)
        if (currentVal == '3'):
            GPIO.output(ssd_pins, sevenSegment3)
        if (currentVal == '4'):
            GPIO.output(ssd_pins, sevenSegment4)
        if (currentVal == '5'):
            GPIO.output(ssd_pins, sevenSegment5)
        if (currentVal == '6'):
            GPIO.output(ssd_pins, sevenSegment6)
        if (currentVal == '7'):
            GPIO.output(ssd_pins, sevenSegment7)
        if (currentVal == '8'):
            GPIO.output(ssd_pins, sevenSegment8)
        if (currentVal == '9'):
            GPIO.output(ssd_pins, sevenSegment9)
        if (currentVal == '*' ):
            GPIO.output(ssd_pins, sevenSegmentDot)
        if (currentVal == '#' ):
            GPIO.output(ssd_pins, sevenSegmentOff)
            ssdOn = False
    else:
        if (currentVal == '#'):
            GPIO.output(ssd_pins, sevenSegmentOff)
            ssdOn = True
            


# Starts the clks

clk1.start(50)
clk2.start(50)
clk3.start(50)
clk4.start(50)

while True:

    # Sends data out to SSDs
    if (ssdOn):
        sendToSSD(readKeypad(keypad_pins[0], keypadMap[0])) 
        sendToSSD(readKeypad(keypad_pins[1], keypadMap[1]))
        sendToSSD(readKeypad(keypad_pins[2], keypadMap[2]))
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))

    else:
        # If SSD is off
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))







    




