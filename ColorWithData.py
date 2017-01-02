#!/usr/bin/python
import random
from dotstar import Adafruit_DotStar

rOffset = 3
gOffset = 2
bOffset = 1

brightness = 0xFF

def convertToStripData(colors):
    for color in colors:
        yield brightness # 000XXXXX brightness
        yield color & 0x0000FF #blue
        yield (color & 0x00FF00) >> 8 #green
        yield color >> 16 # red

def convertToLEDData(colors):
    a = bytearray(convertToStripData(colors))
    return "".join(map(lambda b: format(b, "02x"), a))

def subGreen(color, i):
    green = (color & 0x00FF00) >> 8
    green = max(green - i, 0)
    return color & 0xFF00FF | (green << 8)

numpixels = 60
strip = Adafruit_DotStar()
strip.begin()
# strip.show(convertToLEDData(subGreen(0xf369ff, i*3) for i in xrange(60)))
while True:
    raw_input()
    print brightness
    strip.show(convertToLEDData(0xFF0000 for i in xrange(60)))
    print strip.getPixelColor(10)
    brightness -= 2



