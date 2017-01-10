import numpy
import pyaudio
import time
import matplotlib.pyplot as plt


CHUNK = 1024
class SoundSampler:
    def __init__(self):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            input = True,
            frames_per_buffer=1024)

    def read(self, num_samples):
        rawSamples = self.stream.read(num_samples)
        samples = numpy.fromstring(rawSamples, dtype=numpy.int16)
        fft = numpy.fft.fft(samples)
        return map(abs, fft.tolist())

class SoundSampler2:
    def __init__(self, handler):
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(
            format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            input_device_index = 2,
            input = True,
            output = False,
            frames_per_buffer = 1024,
            stream_callback = handler
        )

if __name__ == '__main__':
    # def callback(in_data, frame_count, time_info, status):
    #     samples = numpy.fromstring(in_data, dtype=numpy.int16)
    #     print samples
    #     return (None, pyaudio.paContinue)
    #
    # SoundSampler2(handler=callable).stream.start_stream()
    # while True:
    #     time.sleep(0.1)
    soundSampler = SoundSampler()
    samples = soundSampler.read(4096)
    k = numpy.arange(0, 4096)
    T = 4096.0 / 44100
    frqLabel = k / T
    plt.plot(frqLabel[:256], samples[:256])
    plt.show()

