import wiringpi

wiringpi.wiringPiSetup()
wiringpi.wiringPiSetUpGpio()
wiringpi.softToneCreate(3)
wiringpi.softToneWrite(3, 1)
x = 1
while x < 20:
    x = x + 1
wiringpi.softToneWrite(3, 0)
