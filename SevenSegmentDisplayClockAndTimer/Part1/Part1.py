import RPi.GPIO as GPIO
from time import sleep
# The Segments are:     A   B   C   D   E   F   G
gpioSevenSegmentPins = [12, 16, 23, 18, 4, 25, 24]
# Keypad Map:           x1  x2  x3  x4  y1  y2  y3  y4
gpioKeypadPins =       [26, 19, 13, 16, 5,  22, 26, 17] 
#In order from 0 to 9
sevenSegment0 = [1,1,1,1,1,1,0]
sevenSegment1 = [0,1,1,0,0,0,0]
sevenSegment2 = [1,1,0,1,1,0,1]
sevenSegment3 = [1,1,1,1,0,0,1]
sevenSegment4 = [0,1,1,0,0,1,1]
sevenSegment5 = [1,0,1,1,0,1,1]
sevenSegment6 = [0,0,1,1,1,1,1]
sevenSegment7 = [1,1,1,0,0,0,0]
sevenSegment8 = [1,1,1,1,1,1,1]
sevenSegment9 = [1,1,1,0,0,1,1]

GPIO.setup(gpioSevenSegmentPins, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(gpioKeypadPins, GPIO.IN, initial = GPIO.LOW)

keypadMap = [['1', '2', '3', 'A'],
             ['4', '5', '6', 'B'],
             ['7', '8', '9', 'C'],
             ['*', '0', '#', 'D']
            ]

curVal = '0'

def readKeypad(rowNum, rowChar):

    GPIO.output(rowNum, GPIO.HIGH)

    if (GPIO.input(gpioKeypadPins[4]) == GPIO.HIGH):
        curVal = rowChar[0]
    elif (GPIO.input(gpioKeypadPins[5]) == GPIO.HIGH):
        curVal = rowChar[1]
    elif (GPIO.input(gpioKeypadPins[6]) == GPIO.HIGH):
        curVal = rowChar[2]
    elif (GPIO.input(gpioKeypadPins[7]) == GPIO.HIGH):
        curVal = rowChar[3]
    GPIO.output(rowNum,GPIO.LOW)

    return curVal

def sendToSSD(curVal):
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

    
while True:
    sleep(0.5)
    if gpioKeypadPins[0] == GPIO.HIGH:
        readKeypad(gpioKeypadPins[0], keypadMap[0])
        sendToSSD(curVal)
    if gpioKeypadPins[1] == GPIO.HIGH:
        readKeypad(gpioKeypadPins[1], keypadMap[1])
        sendToSSD(curVal)
    if gpioKeypadPins[2] == GPIO.HIGH:
        readKeypad(gpioKeypadPins[2], keypadMap[2])
        sendToSSD(curVal)
    if gpioKeypadPins[3] == GPIO.HIGH:
        readKeypad(gpioKeypadPins[3], keypadMap[3])
        sendToSSD(curVal)