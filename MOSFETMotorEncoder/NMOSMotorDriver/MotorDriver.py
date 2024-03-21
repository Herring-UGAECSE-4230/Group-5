import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pwmPin = 5

#Sets up PWM pin
GPIO.setup(pwmPin, GPIO.OUT, initial = GPIO.LOW)

#Sets up PWM function (pwmPin, frequency)
pwm = GPIO.PWM(pwmPin, 10)
#Changes pwm frequeny (frequency)
pwm = pwm.ChangeFrequency(100)
#Starts pwm (duty cycle)
pwm.start(50)

i = 0
while i < 1000():
    i = i + 1
    
#Stops pwm
pwm.stop()
    