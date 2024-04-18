import RPi.GPIO as GPIO
import time

class EMA:
    def __init__(self, alpha):
        self.alpha = alpha
        self.ema = None

    def update(self, value):
        if self.ema is None:
            self.ema = value
        else:
            self.ema = self.alpha * value + (1 - self.alpha) * self.ema
        return self.ema

RPMPERTURN = 25

GPIO.setmode(GPIO.BCM)

IRpin = 26
encoderClk = 20
encoderDt = 16
encoderSw = 12
pwmPin = 21

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
counter = 1

motorOn = True

def encoderPress(counter):
    global motorOn
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
                

                
# Detects a rising edge from the IR sensor
# If it detects a rising edge from the IR sensor, the RPM will be calculated and printed to console
global irCallbackAlreadyRunning
irCallbackAlreadyRunning = False

rpm_ema_calculator = EMA(0.1)

def IRCallback(IRPin):
    global irCallbackAlreadyRunning
    if not irCallbackAlreadyRunning:
        irCallbackAlreadyRunning = True
        startTime = time.perf_counter()
        while (GPIO.input(IRpin) == 0):
            time.sleep(0.001)
        while (GPIO.input(IRpin) == 1):
            time.sleep(0.001)
        endTime = time.perf_counter()
        timeHigh = endTime - startTime
        periodOfWave = timeHigh * 2
        # Calculates RPM
        rpm = ((1 / periodOfWave) * 60) / 3
        avg_rpm = rpm_ema_calculator.update(rpm)
        print(f" Raw RPM: {rpm}, Avg_RPM:{avg_rpm},\n")
        irCallbackAlreadyRunning = False

print(counter)

# Allows for the program to detect if there is a callback function already running 
GPIO.add_event_detect(IRpin, GPIO.FALLING, callback=IRCallback)

while True:
    swState = GPIO.input(encoderSw)
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
            # Prevents the counter from becoming zero
            if counter <= 0:
                counter = 1
                
            pwm.ChangeFrequency(counter * RPMPERTURN)
        # Updates lastClkState with clkState so it's ready for next iteration
        lastClkState = clkState
        # If the rotary is pressed
        if (swState == 0):
            encoderPress(counter)
    if (swState == 0):
        encoderPress(counter)

    