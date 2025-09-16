import RPi.GPIO as gp
import time

gp.setmode(gp.BCM)

gp.setup(26, gp.OUT)

state = 0
period = 1.0

while True:
    gp.output(26, state)
    state = not state
    time.sleep(period/2)
