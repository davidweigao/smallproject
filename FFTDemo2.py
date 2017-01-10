# import matplotlib.pyplot as plt
# import wave
# import numpy
#
# data = wave.open('output.wav', 'rb')
# a = data # this is a two channel soundtrack, I get the first track
# b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
# c = numpy.fft.fft(b) # calculate fourier transform (complex numbers list)
# d = len(c)/2  # you only need half of the fft list (real signal symmetry)
# plt.plot(abs(c[:(d-1)]),'r')
# plt.show()

import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


spf = wave.open('hello.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

#If Stereo
# if spf.getnchannels() == 2:
#     print 'Just mono files'
#     sys.exit(0)


Time=np.linspace(0, len(signal)/fs, num=len(signal))

# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(Time,signal)
# plt.show()

# max_frequency = 5000
# min_frequency = 300
# frequency_range = max_frequency - min_frequency
# fft = np.fft.fft(signal)
# # only care about below 5000 Hz
# fft = fft.tolist()
# fft = map(abs, fft)
# size = fft.__len__()
# fft = fft[size-max_frequency:size - min_frequency] + fft[min_frequency:max_frequency]
# # fft = fft.reverse() + fft
# # the max frequency is in the middle, FFT basic knowledge
# k = np.arange(-frequency_range, frequency_range)
# T = len(signal)/fs  # total time of the wav file in seconds
# frqLabel = k/T # the frequency is N/T, FFT knowledge
# plt.plot(frqLabel, fft)
# plt.show()



fft = np.fft.fft(signal)
# only care about below 5000 Hz
fft = fft.tolist()
fft = map(abs, fft)
size = fft.__len__()
# fft = fft.reverse() + fft
# the max frequency is in the middle, FFT basic knowledge
k = np.arange(0, len(signal))
T = len(signal)/fs  # total time of the wav file in seconds
frqLabel = k/T # the frequency is N/T, FFT know# ledge
deltaFrequency = float(fs) / len(signal)
print len(signal)
print deltaFrequency
NMaxFrequency = fs / 2 / deltaFrequency
print NMaxFrequency
plt.plot(frqLabel, fft)
plt.show()