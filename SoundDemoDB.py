import pyaudio
import sys
import numpy
from LEDStrip import LEDStrip

p = pyaudio.PyAudio()
num_pixel = 60
led_strip = LEDStrip(num_pixel)
max_db = 50.0
sample_rate = 44100 #Hz
sample_per_buffer = 2**11
db_per_pixel = float(max_db) / num_pixel

frequency_per_sample = sample_rate / sample_per_buffer
def frequencyToIndex(frequency):
    return int(frequency / frequency_per_sample)

def normalize(x):
    return 20 * numpy.log10(numpy.abs(x)) - 50

def avg(list):
    return sum(list) / float(len(list))

def getDb(fft, start, end):
    from_index = frequencyToIndex(start)
    until_index = frequencyToIndex(end) + 1
    return max(fft[from_index:until_index])

def dbToPixel(db):
    db = min(max_db, db)
    pixel = int(db / db_per_pixel)
    pixel = min(max(0, pixel), num_pixel-1)
    return pixel

def dbToColor(db):
    db = min(max(0, db), max_db)
    brightness = long(db / max_db * 31) + 0xe0
    color = 0xff00ffL
    color = (brightness << 24) + color
    return color

def print_spectrum(fft):
    out_str = ''
    for i in range(0, len(fft), 50):
        db = getDb(fft, i, i + 50)
        out_str += "{0:g}\t ".format(db)
    print out_str

def handleData(in_data):
    samples = numpy.fromstring(in_data, dtype=numpy.int16)
    fft = numpy.fft.fft(samples)
    fft = normalize(fft)
    db = getDb(fft, 7300, 7400)
    led_pixel = dbToPixel(db)
    color = dbToColor(db)
    print "db: {}, Pixel: {}, color: {}".format(db, led_pixel, hex(color))
    # led_strip.dark()
    # led_strip.set_color(led_pixel, 0xff00ff)
    # led_strip.show()
    led_strip.fill(led_pixel, color)
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
                    # input_device_index=2,
                    output=False)
    stream.start_stream()
    while True:
        stream.start_stream()
        in_data = stream.read(sample_per_buffer, exception_on_overflow=False)
        stream.stop_stream()
        handleData(in_data)
        # time.sleep(0.1)
except Exception as e:
    print e
finally:
    interrupt_callback()

