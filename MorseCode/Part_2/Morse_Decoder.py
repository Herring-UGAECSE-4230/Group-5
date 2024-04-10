import RPi.GPIO as GPIO
import time
import numpy as np

# Placeholders for now
ledPin = 4
speakerPin = 5
telegraphPin = 6

# Default value for dot = 0.1
dot = 0.1
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
pwm = GPIO.PWM(ledPin, freq)

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



#Function to Create the PWM Tone
def play_tone(pwm, duration):
    if (turnOnSpeakerAndLED):
        pwm.start(50)
        time.sleep(duration)
        pwm.stop()

#Funtion to Output Morse Code
def output_mc(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            play_tone(pwm, dot)
            time.sleep(symbol_gap)
        elif symbol == '-':
            play_tone(pwm, dash)
            time.sleep(symbol_gap)
        elif symbol == ' ':
            time.sleep(letter_gap)
        else :
            time.sleep(word_gap)

#function to convert letters to morse code
def letter_to_morse(text):
    morse_code = ''
    for char in text:
        if char in MC_Letters:
            morse_code += MC_Letters[char] + ' '
        else:
            morse_code += '?'
    return morse_code.strip()

def file_read(input): #REALLY NEED TO DEFINE PATH
    with open("input.txt") as file: #opens file and reads
        lines = [line.rstrip() for line in file.readlines()] #makes a list for read lines 
    return lines

#Morse Code Encoding Funciton
def morse_encoder(input,output):
    lines = file_read(input)
    with open("output.txt", 'w') as file:
        attention_morse = MC_Letters['attention']
        output_mc(attention_morse + " ")
        file.write("- . - . - | attention\n")
        for line in lines:
            lineInParts = line.split()
            for word in lineInParts:
                morse_line = letter_to_morse(word)
                output_mc(morse_line)
                file.write(morse_line + "| " + word + "\n")
                file.write("       ")
                # Will trigger a word pause
                output_mc('@')
            #file.write(line + "\n")
            file.write("- . - | over\n")
            output_mc(MC_Letters['over'] + " ")

        output_mc(MC_Letters['out'])
        file.write(". - . - . | out\n")

#End of stuff from Part 1

# Returns the amount of time the telegraph was either held (1) or not held (0).
def timeOfPressOrRest(stateOnCall):
    startTime = time.perf_counter()
    # Placeholder
    endTime = time.perf_counter()
    # If stateOnCall was high at the time of the call
    if (stateOnCall == 1):
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        endTime = time.perf_counter()
    # If stateOnCall was low at the time of the call
    else:
        GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
        endTime = time.perf_counter()
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
        elif (time >= (dot * 2)):
            return '   '
        # Symbol Space
        else:
            return ''
    return ''

# Sets the average time the user takes to make a dot and a dash
def determineAverageDotandDash():
    global dot
    global dash
    # Placeholder values
    averageDot = 0.1
    averageDash = 0.3
    totalTimeOnDots = 0.0
    totalTimeOnDashes = 0.0
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
    # No. of Dots = 6
    # No. of Dashes = 3
    # Waits for the user to begin signing "attention"
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    # Dash 1
    totalTimeOnDashes += timeOfPressOrRest(1)
    # Space 1
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dot 1
    totalTimeOnDots += timeOfPressOrRest(1)
    # Space 2
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dash 2
    totalTimeOnDashes += timeOfPressOrRest(1)
    # Space 3
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dot 2
    totalTimeOnDots += timeOfPressOrRest(1)
    # Space 4
    totalTimeOnDots += timeOfPressOrRest(0)
    # Dash 3
    totalTimeOnDots += timeOfPressOrRest(1)

    averageDot = totalTimeOnDots / 6
    averageDash = totalTimeOnDashes / 3

    dot = averageDot
    dash = averageDash

# Returns the letter representation of the morse parameter
def morse_to_letter(morse):
    if (morse in Letters_MC):
        return Letters_MC[morse]
    else:
        return '?'

# Decodes the user input and returns the word
def decodeUserInput():
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
            morseInput += morseChar
            timeRested = timeOfPressOrRest(0)
            morseChar = timeToMorseChar(timeRested, 0)
        # Removes the letter/word space from morseInput
        if (morseChar == "       "):
            morseInput = morseInput[:-7]
        elif (morseChar == "   "):
            morseInput = morseInput[:-3]
        decodedLetter = morse_to_letter(morseInput)
        if (decodedLetter == 'over'):
            file.write("- . - | over\n")
        elif (decodedLetter == 'out'):
            file.write(". - . - . | out")
        else:
            file.write(morseInput + "   ")
        decodedWord += decodedLetter
        # Clears morseChar if it is not a word space
        if (morseChar != "       "):
            morseChar = ""
    return decodedWord

file = open("output.txt", "w")

determineAverageDotandDash()
print(dot + "\n")
print(dash + "\n")

while True:
    decodedWord = decodeUserInput()
    if decodedWord == "out":
        file.close()
    file.write(decodedWord + "\n")


