import RPi.GPIO as GPIO
import time
import numpy as np
import simpleaudio as sa

LED = 18
dot = 0.1
dash = dot * 3
symbol_gap = dot
letter_gap = dot * 3
word_gap = dot * 7
freq = 500
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)
pwm = GPIO.PWM(LED, freq)

#Function to Create the PWM Tone
def play_tone(pwm, duration):
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
    ' ':'       ', #space representation
    'attention':'-.-.-', #attention
    'over':'-.-', #over
    'out':'.-.-.', #out
}

#Function to read the text file
def file_read(file_path): #REALLY NEED TO DEFINE PATH
    with open(file_path) as file: #opens file and reads
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
def morse_encoder(input_file_path, output_file_path):
    lines = file_read(input_file_path)
    with open(output_file_path, 'w') as file:
        attention_morse = MC_Letters['attention']
        output_mc(attention_morse + " ")
        file.write(". - . - | attention\n")
        for line in lines:
            morse_line = letter_to_morse(line)
            output_mc(morse_line)
            file.write("- . - | over\n")
            output_mc(MC_Letters['over'] + " ")

        output_mc(MC_Letters['out'])
        file.write(". - . - . | out\n")