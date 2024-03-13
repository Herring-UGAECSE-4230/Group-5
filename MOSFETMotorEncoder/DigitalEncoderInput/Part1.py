import RPi.GPIO as GPIO
from time import sleep

# Defines the pins of the encoder
clk = 1
dt = 2
sw = 3

# Sets up the pins for GPIO use
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Holds value of previous clk state
lastClkState = GPIO.input(clk)

# Holds value that the encoder is currently on.
counter = 0
while True:
    clkState=GPIO.input(clk)
    dtState=GPIO.input(dt)
    if clkState!=lastClkState:
        if dtState!=clkState:
            counter+=1
        else:
            counter-=1
    lastClkState=clkState
    print(counter)

