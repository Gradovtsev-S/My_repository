import RPi.GPIO as gp

gp.setmode(gp.BCM)

f = 6
led = 26
gp.setup(f, gp.IN)
gp.setup(led, gp.OUT)

while True:
    gp.output(led, not(gp.input(f)))
