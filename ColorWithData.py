#!/usr/bin/python
import random
from dotstar import Adafruit_DotStar

rOffset = 3
gOffset = 2
bOffset = 1

def convertToStripData(colors):
    for color in colors:
        yield 0xFF # each pixel start with FF
        yield color & 0x0000FF #blue
        yield (color & 0x00FF00) >> 8 #green
        yield color >> 16 # red

def convertToLEDData(colors):
    return bytearray(convertToStripData(colors))

def subGreen(color, i):
    green = (color & 0x00FF00) >> 8
    green = max(green - i, 0)
    return color & 0xFF00FF | (green << 8)

numpixels = 60
strip = Adafruit_DotStar(numpixels)
strip.begin()
strip.show(convertToLEDData(subGreen(0xf369ff, i*3) for i in xrange(60)))


