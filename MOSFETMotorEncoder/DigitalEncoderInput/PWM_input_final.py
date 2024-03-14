import RPi.GPIO as GPIO
import time
# from time import sleep

# Defines the pins of the encoder
clk = 5
dt = 6
sw = 13

# Sets up the pins for GPIO use
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Holds value of previous clk state
lastClkState = GPIO.input(clk)


def debounceTimer():
    time.sleep(0.02)

# Holds value that the encoder is currently on.
counter = 0
print(counter)
while True:
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    swState = GPIO.input(sw)
    # If the rotary is turned
    if clkState != lastClkState:
        # Delay to help with noise
        debounceTimer()
        # If the rotary is turned to the right
        if dtState != clkState:
            counter += 1
            print("Clockwise")
        # If the rotary is turned to the left
        else:
            counter -= 1
            print("Counter-clockwise")
        print(counter)
    # Updates lastClkState with clkState so it's ready for next iteration
    lastClkState = clkState
    # If the rotary is pressed
    if (swState == 0):
        time.sleep(0.3)
        print("Pressed")
        
    
    

