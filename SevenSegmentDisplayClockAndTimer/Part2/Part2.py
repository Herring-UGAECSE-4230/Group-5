import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

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

# Keeps track of the numbers on the SSDs
global number_positions
number_positions = ['0', '0', '0', '0']

# Status of any input pressed
# Note: Will be true on start so that the initial
# state of the SSDs can display zero
global buttonPressed
buttonPressed = True


# Sets the clock pins for the DFFs

clock1pin = 15
clock2pin = 4
clock3pin = 3
clock4pin = 2

# Booleans for if each clock is on or not

global clk1On
global clk2On
global clk3On
global clk4On

clk1On = True
clk2On = True
clk3On = True
clk4On = True

# Array holding each clock pin
clk_pins = [clock1pin, clock2pin, clock3pin, clock4pin]

GPIO.setup(clock1pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock2pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock3pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(clock4pin, GPIO.OUT, initial = GPIO.LOW)

clk1 = GPIO.PWM(clock1pin, 2)
clk2 = GPIO.PWM(clock2pin, 2)
clk3 = GPIO.PWM(clock3pin, 2)
clk4 = GPIO.PWM(clock4pin, 2)

clks = [clk1, clk2, clk3, clk4]

# Sets up the LED pin
led_pin = 11
GPIO.setup(led_pin, GPIO.OUT, initial = GPIO.OUT)

# Defines each number so that the GPIO can send out the correct signals
# to each pin to display said number on the SSD.

sevenSegment0 = (1,1,1,1,1,1,0,0)
sevenSegment1 = (0,1,1,0,0,0,0,0)
sevenSegment2 = (1,1,0,1,1,0,1,0)
sevenSegment3 = (1,1,1,1,0,0,1,0)
sevenSegment4 = (0,1,1,0,0,1,1,0)
sevenSegment5 = (1,0,1,1,0,1,1,0)
sevenSegment6 = (0,0,1,1,1,1,1,0)
sevenSegment7 = (1,1,1,0,0,0,0,0)
sevenSegment8 = (1,1,1,1,1,1,1,0)
sevenSegment9 = (1,1,1,0,0,1,1,0)
sevenSegmentDot = (0,0,0,0,0,0,0,1)
sevenSegmentOff = (0,0,0,0,0,0,0,0)

ssdOn = True
curVal = '0'

keypadMap = [['1', '2', '3', 'A'],

             ['4', '5', '6', 'B'],
             ['7', '8', '9', 'C'],
             ['*', '0', '#', 'D']
            ]

# Mostly copied from Part1.py code
# Returns the button pressed based on the inputted row and
# the characters in said row
def readKeypad(rowNum, rowChar):
    global ssdOn
    global curVal
    global buttonPressed
    
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
        buttonPressed = True
    elif (GPIO.input(keypad_pins[5]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[1]
        print(curVal)
        buttonPressed = True
    elif (GPIO.input(keypad_pins[6]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[2]
        print(curVal)
        buttonPressed = True
    elif (GPIO.input(keypad_pins[7]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[3]
        print(curVal)
        buttonPressed = True
        
    GPIO.output(rowNum,GPIO.LOW)

    return curVal

# Copied from Part1.py code
# Helps to prevent debouncing
def debounceLimiter():
    sleep(0.25)

# Shifts values down the row of SSDs and places the parameter into the first position
# Example: If the old positions are:
#  0  1  2  3
# [1, 2, 3, 4]    
# and the new value is 5,
# The new positions showing on the ssds should be
#  0  1  2  3
# [5, 1, 2, 3]

def shiftClocks():
    global ssdOn
    global clk1On
    global clk2On
    global clk3On
    global clk4On
    #global number_positions
    if (ssdOn):
        # If clk n is on, clk n is turned off, and clk n + 1 turns on.
        if (clk1On):
            stopClk(clk1)
            clk1On = False
            startClk(clk2)
            clk2On = True

        elif (clk2On):
            stopClk(clk2)
            clk2On = False
            startClk(clk3)
            clk3On = True

        elif (clk3On):
            stopClk(clk3)
            clk3On = False
            startClk(clk4)
            clk4On = True

        elif (clk4On):
            stopClk(clk4)
            clk4On = False
            startClk(clk1)
            clk1On = True


        
# Helper function to start a clock at a specific pin
def startClk(clk):
    clk.start(50)

# Helper function to stop a clock at a specific pin
def stopClk(clk):
    clk.stop()

# Sends binary data to SSDs
def sendToSSD(currentVal):
    global ssdOn
    global buttonPressed
    if (ssdOn and buttonPressed):
        # Valid Cases; will turn LED pin off
        if (currentVal == '0'):
            GPIO.output(ssd_pins, sevenSegment0)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '1'):
            GPIO.output(ssd_pins, sevenSegment1)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '2'):
            GPIO.output(ssd_pins, sevenSegment2)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '3'):
            GPIO.output(ssd_pins, sevenSegment3)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '4'):
            GPIO.output(ssd_pins, sevenSegment4)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '5'):
            GPIO.output(ssd_pins, sevenSegment5)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '6'):
            GPIO.output(ssd_pins, sevenSegment6)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '7'):
            GPIO.output(ssd_pins, sevenSegment7)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '8'):
            GPIO.output(ssd_pins, sevenSegment8)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '9'):
            GPIO.output(ssd_pins, sevenSegment9)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '*' ):
            GPIO.output(ssd_pins, sevenSegmentDot)
            GPIO.output(led_pin, GPIO.LOW)
        if (currentVal == '#' ):
            # Starts the clocks so that the SSDs can be turned off
            startClk(clks[0])
            startClk(clks[1])
            startClk(clks[2])
            startClk(clks[3])
            GPIO.output(ssd_pins, sevenSegmentOff)
            GPIO.output(led_pin, GPIO.LOW)
            ssdOn = False
            # Delays the time so that the SSDs can successfully turn off
            for i in range(4):
                number_positions[i] = 0
            sleep(0.1)
            stopClk(clks[0])
            stopClk(clks[1])
            stopClk(clks[2])
            stopClk(clks[3])
        # Invalid Cases
        if (currentVal == 'A' or currentVal == 'B' or currentVal == 'C' or currentVal == 'D'):
            GPIO.output(led_pin, GPIO.HIGH)
            # Since that it was an invalid button press, buttonPressed = False
            buttonPressed = False
    else:
        if (currentVal == '#'):
            startClk(clks[0])
            startClk(clks[1])
            startClk(clks[2])
            startClk(clks[3])
            GPIO.output(ssd_pins, sevenSegment0)
            ssdOn = True
            sleep(0.1)
            stopClk(clks[0])
            stopClk(clks[1])
            stopClk(clks[2])
            stopClk(clks[3])
            


# Starts the clks

clk1.start(50)
clk2.start(50)
clk3.start(50)
clk4.start(50)
clk1On = True
clk2On = True
clk3On = True
clk4On = True


# Brings up initial state of clock

sendToSSD('0')
sleep(0.1)

# Stops the clks

clk2.stop()
clk3.stop()
clk4.stop()
clk2On = False
clk3On = False
clk4On = False

while True:
    buttonPressed = False
    # Checks for any input on the keypad.
    if (ssdOn):
        sendToSSD(readKeypad(keypad_pins[0], keypadMap[0])) 
        sendToSSD(readKeypad(keypad_pins[1], keypadMap[1]))
        sendToSSD(readKeypad(keypad_pins[2], keypadMap[2]))
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))
        
        # If there was a button press
        if (buttonPressed):
            debounceLimiter()
            shiftClocks()

    else:
        # If SSD is off
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))







    




