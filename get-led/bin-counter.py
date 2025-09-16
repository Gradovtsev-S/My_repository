import RPi.GPIO as gp
import time

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

gp.setmode(gp.BCM)

leds = [16, 12, 25, 17, 27, 23, 22, 24]
up, down = 9, 10

gp.setup(leds, gp.OUT)
gp.setup((up, down), gp.IN)
gp.output(leds, 0)

num = 0
sleep_time = 0.2

while True:
    if gp.input(up):
        if num != 255:
            num += 1
            # print(num, dec2bin(num))
            time.sleep(sleep_time)
    if gp.input(down):
        if num != 0:
            num -= 1
            # print(num, dec2bin(num))
            time.sleep(sleep_time)
    for i in range(len(leds)):
        gp.output(leds[i], dec2bin(num)[i])
