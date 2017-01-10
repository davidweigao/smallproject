import pyaudio
import sys
import time
import numpy
import signal
from LEDStrip import LEDStrip

p = pyaudio.PyAudio()
num_pixel = 30
led_strip = LEDStrip(num_pixel)
max_volumn = 40.0
sample_rate = 44100 #Hz
sample_per_buffer = 512
volumn_per_pixel = float(max_volumn) / num_pixel


frequency_per_sample = sample_rate / sample_per_buffer
def frequencyToIndex(frequency):
    return int(frequency / frequency_per_sample)

def adjust_value(x):
    return abs(x) / 1000.0

def avg(list):
    return sum(list) / float(len(list))

def getVolumn(fft):
    from_index = frequencyToIndex(7200)
    until_index = frequencyToIndex(8200) + 1
    return max(fft[from_index:until_index])

def volumnToPixel(volumn):
    volumn = min(max_volumn, volumn)
    return int(volumn / volumn_per_pixel)

def callback(in_data, frame_count, time_info, status):
    samples = numpy.fromstring(in_data, dtype=numpy.int16)
    fft = numpy.fft.fft(samples)
    fft = map(adjust_value, fft.tolist())
    volumn = getVolumn(fft)
    led_pixel = volumnToPixel(volumn)
    print "volumn: {}, Pixel: {}".format(volumn, led_pixel)
    if led_pixel > 10:
         led_strip.fill(led_pixel,0xff00ff)
    else:
        led_strip.fill(0, 0xff00ff)
    time.sleep(0.1)
    return (None, pyaudio.paContinue)

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                input=True,
                output=False,
                input_device_index = 2,
                frames_per_buffer=sample_per_buffer,
                stream_callback=callback)

# This is to release mic when the program  exit
def interrupt_callback(signum, frame):
    print "interrupted manually"
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit()

signal.signal(signal.SIGTSTP, interrupt_callback)
signal.signal(signal.SIGINT, interrupt_callback)

stream.start_stream()
while True:
    time.sleep(0.1)
