import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

b = 13
led = 26
gp.setup(b, gp.IN)
gp.setup(26, gp.OUT)

state = 0

while True:
    if gp.input(b):
        state = not state
        gp.output(led, state)
        time.sleep(0.2)
