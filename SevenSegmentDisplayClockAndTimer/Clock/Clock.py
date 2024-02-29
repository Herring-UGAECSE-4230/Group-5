import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
from time import perf_counter

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# Initalizes the SSDs pins
#           A   B   C  D   E   F   G  DP
ssd_pins = [27, 17, 18, 23, 24, 22, 5, 25] 
# Initalize the Keypad Pins
#              x1  x2  x3  x4  y1 y2  y3  y4
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

clk1 = GPIO.PWM(clock1pin, 500)
clk2 = GPIO.PWM(clock2pin, 500)
clk3 = GPIO.PWM(clock3pin, 500)
clk4 = GPIO.PWM(clock4pin, 500)

clks = [clk1, clk2, clk3, clk4]

# Sets up the LED pin
led_pin = 11
GPIO.setup(led_pin, GPIO.OUT, initial = GPIO.LOW)

# Defines each number so that the GPIO can send out the correct signals
# to each pin to display said number on the SSD.

sevenSegment0 = (1,1,1,1,1,1,0,0)
sevenSegment1 = (0,1,1,0,0,0,0,0)
sevenSegment2 = (1,1,0,1,1,0,1,0)
sevenSegment3 = (1,1,1,1,0,0,1,0)
sevenSegment4 = (0,1,1,0,0,1,1,0)
sevenSegment5 = (1,0,1,1,0,1,1,0)
sevenSegment6 = (1,0,1,1,1,1,1,0)
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

# On every button press, shiftClocks will switch over to the next clock.
# This is to allow the inputted number to be displayed on the SSD correlating to the clock.
# Example: If the program is currently on the 1st clock, 
# The old positions are:
#  0  1  2  3
# [1, 2, 3, 4]    
# and the button input is 5,
# The new positions showing on the ssds should be
#  0  1  2  3
# [5, 2, 3, 4]

def shiftClocks():
    global ssdOn
    global clk1On
    global clk2On
    global clk3On
    global clk4On
    global number_positions
    if (ssdOn):
        # If clk n is on, clk n is turned off, and clk n + 1 turns on.
        if (clk1On):
            stopClk(clk_pins[0])
            clk1On = False
            number_positions[0] = curVal
            startClk(clk_pins[1])
            clk2On = True
            sendToSSD(number_positions[1])
            

        elif (clk2On):
            stopClk(clk_pins[1])
            clk2On = False
            number_positions[1] = curVal
            startClk(clk_pins[2])
            clk3On = True
            sendToSSD(number_positions[2])

        elif (clk3On):
            stopClk(clk_pins[2])
            clk3On = False
            number_positions[2] = curVal
            startClk(clk_pins[3])
            clk4On = True
            sendToSSD(number_positions[3])

        elif (clk4On):
            stopClk(clk_pins[3])
            clk4On = False
            number_positions[3] = curVal
            startClk(clk_pins[0])
            # This sleep function helps to prevent the first SSD from only
            # taking in some parts of the sendToSSD function.
            sleep(0.07)
            clk1On = True
            sendToSSD(number_positions[0])

        for i in range(4):
            print(f"Index {i} = {number_positions[i]}")
            
            


        
# Helper function to start a clock at a specific pin
def startClk(clk):
    GPIO.output(clk, 0)

# Helper function to stop a clock at a specific pin
def stopClk(clk):
    GPIO.output(clk, 1)

# Sends binary data to SSDs
def sendToSSD(currentVal):
    global ssdOn
    global buttonPressed
    global clk1On
    global clk2On
    global clk3On
    global clk4On
    global now
    global hour
    global minute
    global automaticClockOn
    global manualClockOn
    if (ssdOn):
        # Valid Cases; will turn LED pin off
        if (currentVal == '#' ):
            # Starts the clocks so that the SSDs can be turned off
            startClk(clk_pins[0])
            startClk(clk_pins[1])
            startClk(clk_pins[2])
            startClk(clk_pins[3])
            GPIO.output(ssd_pins, sevenSegmentOff)
            GPIO.output(led_pin, GPIO.LOW)
            ssdOn = False
            # Delays the time so that the SSDs can successfully turn off
            for i in range(4):
                number_positions[i] = 0
            sleep(0.1)
            stopClk(clk_pins[0])
            stopClk(clk_pins[1])
            stopClk(clk_pins[2])
            stopClk(clk_pins[3])
            clk1On = False
            clk2On = False
            clk3On = False
            clk4On = False
            
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
            
        # Automatic Clock
        if (currentVal == 'A'):
            manualClockOn = False
            # Gets the current time the button was pressed.
            now = datetime.now()
            hour = '{0:02d}'.format(now.hour)
            minute = '{0:02d}'.format(now.minute)

            # Begins sending out data for the time.
            # Sends out hour data
            clk1On = True
            for i in range(2):
                shiftClocks()
                sendToSSD(hour[0])
            # Sends out minute data
            for i in range(2):
                shiftClocks()
                sendToSSD(minute[0])

            automaticClockOn = True
            


        # Manual Clock
        if (currentVal == 'B'):
            print("Not implemented yet")
        if (currentVal == 'C' or currentVal == 'D'):
            GPIO.output(led_pin, GPIO.HIGH)
            # Since that it was an invalid button press, buttonPressed = False
            buttonPressed = False
    else:
        if (currentVal == '#'):
            startClk(clk_pins[0])
            startClk(clk_pins[1])
            startClk(clk_pins[2])
            startClk(clk_pins[3])
            GPIO.output(ssd_pins, sevenSegment0)
            ssdOn = True
            sleep(0.1)
            stopClk(clk_pins[0])
            stopClk(clk_pins[1])
            stopClk(clk_pins[2])
            stopClk(clk_pins[3])
            # Sets up SSD1 to be ready to recieve input
            stopClk(clk_pins[0])
            startClk(clk_pins[0])
            clk1On = True


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
clk1.stop()
clk2.stop()
clk3.stop()
clk4.stop()
clk2On = False
clk3On = False
clk4On = False

stopClk(clk_pins[0])
startClk(clk_pins[0])

# Sets up the time variable so that when the automatic clock is triggered,
# it is already initialized

now = datetime.now()
hour = '{0:02d}'.format(now.hour)
minute = '{0:02d}'.format(now.minute)
automaticClockOn = False
manualClockOn = False

# To keep track of how much time has passed between each loop
loopStart = 0.0
loopEnd = 0.0


while True:
    buttonPressed = False
    # Checks for any input on the keypad.
    if (ssdOn):

        if (automaticClockOn):
            now = datetime.now()
            hour = '{0:02d}'.format(now.hour)
            minute = '{0:02d}'.format(now.minute)
            # Begins sending out data for the time.
            # Sends out hour data
            clk1On = True
            for i in range(2):
                shiftClocks()
                sendToSSD(hour[0])
            # Sends out minute data
            for i in range(2):
                shiftClocks()
                sendToSSD(minute[0])


        """
        sendToSSD(readKeypad(keypad_pins[0], keypadMap[0])) 
        sendToSSD(readKeypad(keypad_pins[1], keypadMap[1]))
        sendToSSD(readKeypad(keypad_pins[2], keypadMap[2]))
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))
        """
        # If there was a button press
        if (buttonPressed):
            debounceLimiter()
            shiftClocks()

    else:
        # If SSD is off
        sendToSSD(readKeypad(keypad_pins[3], keypadMap[3]))







    




