#!/usr/bin/python
import random
from dotstar import Adafruit_DotStar

numpixels = 60
strip = Adafruit_DotStar(numpixels)
strip.begin()
strip.show(bytearray((0x00 if i % 4 != 0 else 0xFF) for i in xrange(numpixels * 4)))
