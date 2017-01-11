import pyaudio
import sys
import time
import numpy
import signal
from LEDStrip import LEDStrip

p = pyaudio.PyAudio()
num_pixel = 30
led_strip = LEDStrip(num_pixel)
max_db = 60.0
sample_rate = 44100 #Hz
sample_per_buffer = 2**11
db_per_pixel = float(max_db) / num_pixel

frequency_per_sample = sample_rate / sample_per_buffer
def frequencyToIndex(frequency):
    return int(frequency / frequency_per_sample)

def adjust_value(x):
    return 20 * numpy.log10(abs(x)) - 50

def avg(list):
    return sum(list) / float(len(list))

def getDb(fft, start, end):
    from_index = frequencyToIndex(start)
    until_index = frequencyToIndex(end) + 1
    return max(fft[from_index:until_index])

def dbToPixel(db):
    db = min(max_db, db)
    pixel = int(db / db_per_pixel)
    return pixel if pixel > 5 else 0

def print_spectrum(fft):
    out_str = ''
    for i in range(0, len(fft), 50):
        db = getDb(fft, i, i + 50)
        out_str += "{0:g}\t ".format(db)
    print out_str

def callback(in_data, frame_count, time_info, status):
    samples = numpy.fromstring(in_data, dtype=numpy.int16)
    fft = numpy.fft.fft(samples)
    fft = map(adjust_value, fft.tolist())
    db = getDb(fft, 7200, 8200)
    led_pixel = dbToPixel(db)
    print "db: {}, Pixel: {}".format(db, led_pixel)
    led_strip.fill(led_pixel, 0xff00ff)
    time.sleep(0.1)
    return (None, pyaudio.paContinue)


# This is to release mic when the program  exit
def interrupt_callback():
    print "interrupted manually"
    stream.stop_stream()
    stream.close()
    p.terminate()
    sys.exit()

try:
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    output=False,
                    input_device_index = 2)
    stream.start_stream()
    while True:
        in_data = stream.read(sample_per_buffer, exception_on_overflow=False)
        callback(in_data, 0, None, None)
        time.sleep(0.05)
except Exception as e:
    print e
finally:
    interrupt_callback()

