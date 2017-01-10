from SoundSampler import SoundSampler
from LEDStrip import LEDStrip
import time

sound_sampler = SoundSampler()
led_strip = LEDStrip(60)

while True:
    try:
        voice = sound_sampler.read(4096)[50]
        voice = min(30000, voice)
        print voice
        x = 30000 / 60
        led_pixel = int(voice / x)
        led_strip.fill(led_pixel, 0xff0000)
        time.sleep(1.0 / 20)
    except:
        pass