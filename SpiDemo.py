import spidev
import time

def convertToStripData(colors):
    for color in colors:
        yield int(color >> 24)
        color = int(color & 0x00ffffff)
        yield color & 0x0000FF #blue
        yield (color & 0x00FF00) >> 8 #green
        yield color >> 16 # red

def getColors():
    for i in xrange(20):
        yield 0xE1ff0000
        yield 0xE100ff00
        yield 0xFF0000ff

def getSteep():
    brightness = 0xE1
    for i in xrange(60):
        if i % 2 == 0:
            brightness += 1
        yield (brightness << 24) + 0xffffff

def rotateColor(c):
    return c[-2:] + c[:-2]

spi = spidev.SpiDev()
spi.open(0,0)
# color frames
colors = list(getSteep())

while True:
    # start frame
    spi.xfer2([0x00, 0x00, 0x00, 0x00])
    # spi.xfer2([0xff,0xff,0x00,0x00])
    spi.xfer2(list(convertToStripData(colors)))
    # end frame
    spi.xfer2([0xFF, 0xFF, 0xFF, 0xFF])
    colors = rotateColor(colors)
    time.sleep(1.0/100)