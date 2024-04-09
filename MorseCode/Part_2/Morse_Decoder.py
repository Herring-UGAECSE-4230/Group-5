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

# Returns the amount of time the telegraph was either held or not held.
def timeOfPressOrRest(stateOnCall):
    startTime = time.perf_counter()
    endTime = time.perf_counter()
    # If stateOnCall was high at the time of the call
    if (stateOnCall == 1):
        while (stateOnCall == 1):
            pass
        endTime = time.perf_counter()
    # If stateOnCall was low at the time of the call
    else:
        while (stateOnCall == 0):
            pass
        endTime = time.perf_counter()
    timeOfHolding = endTime - startTime
    return timeOfHolding
    
# Returns a morse code character based on the amount of time the telegraph
# was press/released
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
            return ' '
    return ''

# Sets the average time the user takes to make a dot and a dash
def determineAverageDotandDash():
    global dot
    global dash
    # Placeholder values
    averageDot = 0.1
    averageDash = 0.3
    # Used to track when the user either does one dot or three
    numOfDots = 0
    # Keeps track of when a dash/dot space starts
    startTime = time.perf_counter()
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

    # Dash 1
    while numOfDots is not 3:
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        if (GPIO.input(telegraphPin)):
            numOfDots += 1
    numOfDots = 0
    endTime = time.perf_counter()
    totalTimeOnDashes += startTime - endTime
    # Space 1
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Dot 1
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Space 2
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Dash 2
    while numOfDots is not 3:
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        if (GPIO.input(telegraphPin)):
            numOfDots += 1
    numOfDots = 0
    endTime = time.perf_counter()
    totalTimeOnDashes += startTime - endTime
    # Space 3
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Dot 2
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Space 4
    startTime = time.perf_counter()
    GPIO.wait_for_edge(telegraphPin, GPIO.RISING)
    endTime = time.perf_counter()
    totalTimeOnDots += startTime - endTime
    # Dash 3
    while numOfDots is not 3:
        GPIO.wait_for_edge(telegraphPin, GPIO.FALLING)
        if (GPIO.input(telegraphPin)):
            numOfDots += 1
    numOfDots = 0
    endTime = time.perf_counter()
    totalTimeOnDashes += startTime - endTime

    averageDot = totalTimeOnDots / 6
    averageDash = totalTimeOnDashes / 3

    dot = averageDot
    dash = averageDash

# Returns the letter
def morse_to_letter(morse):
    if (morse in Letters_MC):
        return Letters_MC[morse]
    else:
        return '?'



