import RPi.GPIO as GPIO
from time import sleep
# The Segments are:     A   B   C   D   E   F   G
gpioSevenSegmentPins = [27, 17, 18, 23, 24, 22, 5]
# Keypad Map:           x1  x2  x3  x4  y1  y2  y3  y4
gpioKeypadPins =       [21, 20, 16, 12 , 6 ,13, 19, 26]

#Possible Seven Segment Configurations
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
sevenSegmentA = (1,1,1,0,1,1,1)
sevenSegmentB = (0,0,1,1,1,1,1)
sevenSegmentC = (1,0,0,1,1,1,0)
sevenSegmentD = (0,1,1,1,1,0,1)
sevenSegmentOff = (0,0,0,0,0,0,0)

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

curVal = '0'

ssdOn = True

def readKeypad(rowNum, rowChar):
    global curVal
    GPIO.output(rowNum, GPIO.HIGH)

    if (GPIO.input(gpioKeypadPins[4]) == GPIO.HIGH):
        curVal = rowChar[0]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[5]) == GPIO.HIGH):
        curVal = rowChar[1]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[6]) == GPIO.HIGH):
        curVal = rowChar[2]
        print(curVal)
    elif (GPIO.input(gpioKeypadPins[7]) == GPIO.HIGH):
        curVal = rowChar[3]
        print(curVal)
    GPIO.output(rowNum,GPIO.LOW)

    return curVal

def sendToSSD(curVal):
    if (ssdOn):
        if (curVal == '0'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment0)
        if (curVal == '1'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment1)
        if (curVal == '2'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment2)
        if (curVal == '3'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment3)
        if (curVal == '4'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment4)
        if (curVal == '5'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment5)
        if (curVal == '6'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment6)
        if (curVal == '7'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment7)
        if (curVal == '8'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment8)
        if (curVal == '9'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment9)
        if (curVal == 'A'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentA)
        if (curVal == 'B'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentB)
        if (curVal == 'C'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentC)
        if (curVal == 'D'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentD)
        if (curVal == '#'):
            GPIO.output(gpioSevenSegmentPins, sevenSegmentOff)
            ssdOn = False
    else:
        if (curVal == '#'):
            GPIO.output(gpioSevenSegmentPins, sevenSegment0)
            ssdOn = True


clk.start(50)
while True:
    #sleep(0.5)[21, 20, 16, 12 , 6 ,13, 19, 26][21, 20, 16, 12 , 6 ,13, 19, 26]
        if (ssdOn):
            readKeypad(gpioKeypadPins[0], keypadMap[0])
            sendToSSD(curVal)
            #print("Read Input!");
            readKeypad(gpioKeypadPins[1], keypadMap[1])
            sendToSSD(curVal)
            #print("Read Input!");
            readKeypad(gpioKeypadPins[2], keypadMap[2])
            sendToSSD(curVal)
            #print("Read Input!");
            readKeypad(gpioKeypadPins[3], keypadMap[3])
            sendToSSD(curVal)
            #print("Read Input!");
        else:
            # If SSD is off
            readKeypad(gpioKeypadPins[3], keypadMap[3])
