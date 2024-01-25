import pigpio
pi=pigpio.pi()
pi.set_PWM_frequency(3, 1)
pi.set_PWM_dutycycle(225)
x = 1
while x < 20:
    x = x + 1
pi.set_PWN_dutycycle(3, 0)