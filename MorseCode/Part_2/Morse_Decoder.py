import RPi.GPIO as GPIO
import time
import numpy as np

# Placeholders for now
ledPin = 4
speakerPin = 6
telegraphPin = 18

# Default value for dot = 1
dot = 1
dash = dot * 3
symbol_gap = dot
letter_gap = dot * 3
word_gap = dot * 7
freq = 500
global turnOnSpeakerAndLED
turnOnSpeakerAndLED = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(speakerPin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(telegraphPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(speakerPin, freq)

# Copied from Part 1:
#morse code dictionary: an array that assigns each letter its morse code representation
MC_Letters = {
    'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..',
    'e':'.', 'f':'..-.', 'g':'--.', 'h':'....',
    'i':'..', 'j':'.---', 'k':'-.-', 'l':'.-..', 
    'm':'--', 'n':'-.', 'o':'---', 'p':'.--.', 
    'q':'--.-', 'r':'.-.', 's':'...', 't':'-', 
    'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 
    'y':'-.--', 'z':'--..',
    '1':'.----', '2':'..---', '3':'...--',
    '4':'....-', '5':'.....', '6':'-....',
    '7':'--...', '8':'---..', '9':'----.',
    '0':'-----',
    ' ':'       ', #space representation
    'attention':'-.-.-', #attention
    'over':'-.-', #over
    'out':'.-.-.', #out
}

Letters_MC = dict()
for key in MC_Letters: 
    val = MC_Letters[key]
    Letters_MC[val] = key




def file_read(input): #REALLY NEED TO DEFINE PATH
    with open("input.txt") as file: #opens file and reads
        lines = [line.rstrip() for line in file.readlines()] #makes a list for read lines 
    return lines

#End of stuff from Part 1

# Returns the amount of time the telegraph was either held (1) or not held (0).
def timeOfPressOrRest(stateOnCall):
    startTime = time.perf_counter()
    print(startTime,"\n")
    # Placeholder
    endTime = time.perf_counter()
    # If stateOnCall was high at the time of the call
    if (stateOnCall == 1):#function to convert letters to morse code
        time.sleep(0.02)
        pwm.start(50)
        GPIO.output(ledPin, GPIO.HIGH)
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        GPIO.output(ledPin, GPIO.LOW)
        pwm.stop()
        endTime = time.perf_counter()
    # If stateOnCall was low at the time of the call
    else:
        time.sleep(0.02)
        GPIO.wait_for_edge(telegraphPin, GPIO.RISING, timeout= int((dot * 7)*1000))
        endTime = time.perf_counter()
    print(endTime,"\n")
    timeOfHolding = endTime - startTime
    return timeOfHolding
    
# Returns a morse code character based on the amount of time the telegraph
# was pressed/released
def timeToMorseChar(time, stateOnCall):
    # Dots and Dashes
    if (stateOnCall == 1):
        # Dash
        if (time >= (dot * 2)):
            return '-'
        # Dot
        else:
            return '.'
    # Spaces
    if (stateOnCall == 0):
        # Word Space
        if (time >= (dot * 7)):
            return '       '
        # letter Space
        elif (time >= (dot * 3)):
            return '   '
        # Symbol Space
        else:
            return ''
    return ''

# Sets the average time the user takes to make a dot and a dash
def determineAverageDot():
    global dot
    # Placeholder values
    averageDot = 0.1
    totalTimeOnDots = 0.0
    # Order of dots and dashes:
    # Dash
    # Symbol space (dot)
    # Dot
    # Symbol space (dot)
    # Dash
    # Symbol space (dot)
    # Dot
    # Symbol space (dot)
    # Dash
    # Waits for the user to begin signing "attention"
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    # Dash 1
    totalTimeOnDots += (timeOfPressOrRest(1))/3
    # Space 1
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dot 1
    totalTimeOnDots += timeOfPressOrRest(1)
    # Space 2
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dash 2
    totalTimeOnDots += (timeOfPressOrRest(1))/3
    # Space 3
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dot 2
    totalTimeOnDots += timeOfPressOrRest(1)
    # Space 4
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dash 3
    totalTimeOnDots += (timeOfPressOrRest(1))/3

    averageDot = totalTimeOnDots / 9

    dot = averageDot

# Returns the letter representation of the morse parameter
def morse_to_letter(morse):
    if (morse in Letters_MC):
        return Letters_MC[morse]
    else:
        return '?'

# Decodes the user input and returns the word
def decodeUserInput(file):
    # Placeholders
    morseInput = ""
    morseChar = ""
    decodedWord = ""
    decodedLetter = ""
    # Waits for the user to start inputting morse code
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    # While morseChar is not a word space
    while (morseChar != "       "):
        # While morseChar is not a letter space or a word space
        while ((morseChar != "   ") and (morseChar != "       ")):
            timePressed = timeOfPressOrRest(1)
            morseChar = timeToMorseChar(timePressed, 1)
            print("MorseChar:",morseChar)
            morseInput += morseChar
            print("MorseInput:",morseInput)
            timeRested = timeOfPressOrRest(0)
            morseChar = timeToMorseChar(timeRested, 0)
            print(morseChar)
            morseInput += morseChar
        # Removes the letter/word space from morseInput
        if (morseChar == "       "):
            morseInput = morseInput[:-7]
        elif (morseChar == "   "):
            morseInput = morseInput[:-3]
        decodedLetter = morse_to_letter(morseInput)
        # Adds a space for simplicity
        morseInput += " "
        print("DecodedLetter:", decodedLetter)
        if (decodedLetter == 'over'):
            file.write("-.- | over\n")
        elif (decodedLetter == 'out'):
            file.write(".-.-. | out")
        else:
            file.write(morseInput)
        decodedWord += decodedLetter
        # Clears morseChar if it is not a word space
        if (morseChar != "       "):
            morseChar = ""
            morseInput = ""
    print(decodedWord + '\n')
    return decodedWord

with open("output.txt", "w") as file:

    print("Reached this point!")
    determineAverageDot()
    print(dot,"\n")

    file.write("-.-.- | attention\n")
    while True:
        decodedWord = decodeUserInput(file)
        if decodedWord == "out":
            file.close()
            break
        elif decodedWord == "over":
            file.write("")
        else:
            file.write("| " + decodedWord + "\n")


