import RPi.GPIO as GPIO
import time
import numpy as np

LED = 4
dot = 0.1
dash = dot * 3
symbol_gap = dot
letter_gap = dot * 3
word_gap = dot * 7
freq = 500
global turnOnSpeakerAndLED
turnOnSpeakerAndLED = True


GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, freq)

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
        else:
            time.sleep(word_gap)

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

#Function to read the text file
def file_read(input): #REALLY NEED TO DEFINE PATH
    with open("input.txt") as file: #opens file and reads
        lines = [line.rstrip() for line in file.readlines()] #makes a list for read lines 
    return lines

#function to convert letters to morse code
def letter_to_morse(text):
    morse_code = ''
    for char in text:
        if char in MC_Letters:
            morse_code += MC_Letters[char] + ' '
    return morse_code.strip()

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
    
unitOfTime = int(input("Enter the number of ms you want your dot to run: "))
dot = unitOfTime / 1000
if (dot <= 0.05):
    turnOnSpeakerAndLED = False
print(turnOnSpeakerAndLED)
morse_encoder("/home/group5/Desktop/Group-5/MorseCode/input.txt", "/home/group5/Desktop/Group-5/MorseCode/output.txt")