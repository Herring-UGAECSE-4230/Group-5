import RPi.GPIO as GPIO
import time

RPMPERTURN = 25

GPIO.setmode(GPIO.BCM)

IRpin = 4
encoderClk = 5
encoderDt = 6
encoderSw = 7
pwmPin = 8

GPIO.setup(IRpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderClk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderDt, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderSw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pwmPin, GPIO.OUT, initial = GPIO.LOW)

#Sets up PWM function (pwmPin, frequency)
pwm = GPIO.PWM(pwmPin, 10)
#Changes pwm frequency (frequency)
pwm.ChangeFrequency(10)
#Starts pwm (duty cycle)
pwm.start(50)

# Holds value of previous encoderClk state
lastClkState = GPIO.input(encoderClk)



def debounceTimer():
    time.sleep(0.02)

# Holds value that the encoder is currently on.
counter = 0

motorOn = True

def encoderPress(counter):
    global motorOn
    if (swState == 0):
            time.sleep(0.3)
            print("Pressed")
            # If the motor was previously on
            if motorOn:
                motorOn = False
                pwm.stop()
            else:
                motorOn = True
                pwm.start(50)
                pwm.ChangeFrequency(counter * RPMPERTURN)

def IRCallback(IRPin):
    startTime = time.perf_counter()
    GPIO.wait_for_edge(IRPin, GPIO.FALLING)
    endTime = time.perf_counter()
    timeHigh = endTime - startTime
    periodOfWave = timeHigh * 2
    # Calculates RPM
    rpm = (60 / periodOfWave) / 3
    print(rpm, "\n")

print(counter)
while True:
    while motorOn:
        clkState = GPIO.input(encoderClk)
        dtState = GPIO.input(encoderDt)
        swState = GPIO.input(encoderSw)
        irState = GPIO.input(IRpin)
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
            pwm.ChangeFrequency(counter * RPMPERTURN)
        # Updates lastClkState with clkState so it's ready for next iteration
        lastClkState = clkState
        # If the rotary is pressed
        encoderPress(counter)
        # Detects a rising edge from the IR sensor
        # If it detects a rising edge from the IR sensor, the RPM will be calculated
        GPIO.add_event_detect(IRpin, GPIO.RISING, callback=IRCallback)

    