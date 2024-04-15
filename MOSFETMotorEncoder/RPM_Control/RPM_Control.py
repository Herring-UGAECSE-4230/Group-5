import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
IR_pin = 4

encoderClk = 5
encoderDt = 6
encoderSw = 7
pwmPin = 8

GPIO.setup(encoderClk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderDt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderSw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pwmPin, GPIO.OUT, initial = GPIO.LOW)

#Sets up PWM function (pwmPin, frequency)
pwm = GPIO.PWM(pwmPin, 10)
#Changes pwm frequeny (frequency)
pwm.ChangeFrequency(10)
#Starts pwm (duty cycle)
pwm.start(50)

# Holds value of previous encoderClk state
lastClkState = GPIO.input(encoderClk)


def debounceTimer():
    time.sleep(0.02)

# Holds value that the encoder is currently on.
counter = 0
print(counter)
while True:
    clkState = GPIO.input(encoderClk)
    dtState = GPIO.input(encoderDt)
    swState = GPIO.input(encoderSw)
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
pwm.stop()
    
    