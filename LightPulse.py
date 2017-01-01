#!/usr/bin/python

#pulse for each input

import time
import random
from dotstar import Adafruit_DotStar

numpixels = 60
strip = Adafruit_DotStar(numpixels)
strip.begin()

def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (((r << 8) + g) << 8) + b

height = numpixels
while True:
    raw_input()
    up = True
    done = False
    color2 = getRandomColor()
    print hex(color2)
    head = 0
    while not done:
        color = color2 if up else 0
        strip.setPixelColor(head, color)
        strip.show()
        time.sleep(1.0 / 500)

        head = head + 1 if up else head - 1
        if head == height:
            up = False
            head -= 1
        elif head == 0:
            done = True
            head += 1

