#!/usr/bin/python
import time
import random
from dotstar import Adafruit_DotStar

numpixels = 60
strip = Adafruit_DotStar(numpixels)
strip.begin()

while True:
    strip.setBrightness(16)
    colors = bytearray((random.getrandbits(8) if i%4 != 0 else 0xFF) for i in xrange(numpixels * 4))
    strip.show(colors)
    time.sleep(1.0/2)