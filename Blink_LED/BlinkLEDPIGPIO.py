import pigpio
from time import sleep
pi=pigpio.pi()
pi.set_PWM_frequency(3, 1)
pi.set_PWM_dutycycle(3, 128)
x = 1
while x < 10:
    sleep(1)
    x = x + 1
pi.set_PWM_dutycycle(3, 0)
