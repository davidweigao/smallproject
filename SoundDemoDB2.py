# Python 2.7 code to analyze sound and interface with Arduino

import pyaudio  # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy  # from http://numpy.scipy.org/
import audioop
import sys
import math
import struct
from LEDStrip import LEDStrip

led_strip = LEDStrip(60)

'''
Sources

http://www.swharden.com/blog/2010-03-05-realtime-fft-graph-of-audio-wav-file-or-microphone-input-with-python-scipy-and-wckgraph/
http://macdevcenter.com/pub/a/python/2001/01/31/numerically.html?page=2

'''

MAX = 0


def list_devices():
    # List all audio input devices
    p = pyaudio.PyAudio()
    i = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i) + '. ' + dev['name']
        i += 1


def arduino_soundlight():
    chunk = 2 ** 11  # Change if too fast/slow, never less than 2**11
    scale = 50  # Change if too dim/bright
    exponent = 5  # Change if too little/too much difference between loud and quiet sounds
    samplerate = 44100

    # CHANGE THIS TO CORRECT INPUT DEVICE
    # Enable stereo mixing in your sound card
    # to make you sound output an input
    # Use list_devices() to list all your input devices
    device = 2

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    # input_device_index=device,
                    frames_per_buffer=chunk,
                )

    print "Starting, use Ctrl+C to stop"
    try:
        while True:
            data = stream.read(chunk, exception_on_overflow=False)

            '''
           # Old RMS code, will only show the volume

           rms   = audioop.rms(data, 2)

           level = min(rms / (2.0 ** 16) * scale, 1.0)
           level = level**exponent
           level = int(level * 255)

           print level
           ser.write(chr(level))
           '''

            # Do FFT
            levels = calculate_levels(data, chunk, samplerate)
            print levels[2]
            if (levels[2] > 0):
                led_strip.fill(50, 0xff00ff)
            else:
                led_strip.fill(0, 0xff00ff)
            # Make it look better and send to serial
            for level in levels:
                level = max(min(level / scale, 1.0), 0.0)
                level = level ** exponent
                level = int(level * 255)
    except KeyboardInterrupt:
        pass
    finally:
        print "\nStopping"
        stream.close()
        p.terminate()


def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency
    global MAX

    # Convert raw sound data to Numpy array
    fmt = "%dH" % (len(data) / 2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier) / 2]) / 1000
    ffty1 = ffty[:len(ffty) / 2]
    ffty2 = ffty[len(ffty) / 2::] + 2
    ffty2 = ffty2[::-1]
    ffty = ffty1 + ffty2
    ffty = numpy.log(ffty) - 2

    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier) / 2]

    size = len(fourier)

    # Add up for 6 lights
    levels = [sum(fourier[i:(i + size / 6)]) for i in xrange(0, size, size / 6)][:6]

    return levels


if __name__ == '__main__':
    # list_devices()
    arduino_soundlight()