import RPi.GPIO as GPIO
from time import sleep
# The Segments are:     A   B   C   D   E   F   G  DP
gpioSevenSegmentPins = [27, 17, 18, 23, 24, 22, 5, 7]
# Keypad Map:           x1  x2  x3  x4  y1  y2  y3  y4
gpioKeypadPins =       [21, 20, 16, 12 , 6 ,13, 19, 26]

#Possible Seven Segment Configurations
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
sevenSegmentA = (1,1,1,0,1,1,1,0)
sevenSegmentB = (0,0,1,1,1,1,1,0)
sevenSegmentC = (1,0,0,1,1,1,0,0)
sevenSegmentD = (0,1,1,1,1,0,1,0)
sevenSegmentDot = (0,0,0,0,0,0,0,1)
sevenSegmentOff = (0,0,0,0,0,0,0,0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Clock pin

GPIO.setup(4, GPIO.OUT)
clk = GPIO.PWM(4, 100)
GPIO.setup(gpioSevenSegmentPins, GPIO.OUT, initial = GPIO.LOW)

# Keypad Pins Setup

GPIO.setup(gpioKeypadPins[0:4], GPIO.OUT, initial = GPIO.LOW)


GPIO.setup(gpioKeypadPins[4], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(gpioKeypadPins[5], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(gpioKeypadPins[6], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(gpioKeypadPins[7], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


keypadMap = [['1', '2', '3', 'A'],

             ['4', '5', '6', 'B'],
             ['7', '8', '9', 'C'],
             ['*', '0', '#', 'D']
            ]

ssdOn = True

curVal = '0'
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

    if (GPIO.input(gpioKeypadPins[4]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[0]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[5]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[1]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[6]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[2]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[7]) == GPIO.HIGH):
        debounceLimiter()
        curVal = rowChar[3]
        print(curVal)
        
    GPIO.output(rowNum,GPIO.LOW)

    return curVal

#Sends curVal to SSD
def sendToSSD(currentVal):
    global ssdOn
    
    # If the SSD should be on
    if (ssdOn):
        if (currentVal == '0'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment0)
        if (currentVal == '1'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment1)
        if (currentVal == '2'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment2)
        if (currentVal == '3'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment3)
        if (currentVal == '4'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment4)
        if (currentVal == '5'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment5)
        if (currentVal == '6'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment6)
        if (currentVal == '7'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment7)
        if (currentVal == '8'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment8)
        if (currentVal == '9'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment9)
        if (currentVal == 'A'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentA)
        if (currentVal == 'B'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentB)
        if (currentVal == 'C'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentC)
        if (currentVal == 'D'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentD)
        if (currentVal == '*'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentDot)
        if (currentVal == '#'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentOff)
            ssdOn = False
    else:
        if (currentVal == '#'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment0)
            ssdOn = True
            
# Helps to prevent debouncing
def debounceLimiter():
    sleep(0.25)

clk.start(50)
while True:
    if (ssdOn):
        sendToSSD(readKeypad(gpioKeypadPins[0], keypadMap[0]))
        #print("Read Input!");
        
        sendToSSD(readKeypad(gpioKeypadPins[1], keypadMap[1]))
        #print("Read Input!");
        sendToSSD(readKeypad(gpioKeypadPins[2], keypadMap[2]))
        #print("Read Input!");
        sendToSSD(readKeypad(gpioKeypadPins[3], keypadMap[3]))
        #print("Read Input!");
    else:
        # If SSD is off
        sendToSSD(readKeypad(gpioKeypadPins[3], keypadMap[3]))
