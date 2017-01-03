from LEDStrip import *
import time
strip = LEDStrip(60)
strip.dark()
strip.dark()
# strip.showColors(list(getSteep()))

# music pulse
# count = [60, 30, 24, 8, 51, 60, 12, 0, 9, 15, 46, 44 ,22, 18, 35, 36, 34, 12, 22, 0]
# speed = [240, 200, 250, 300, 180, 320, 180, 240, 100, 240,240, 200, 250, 300, 180, 320, 180, 240, 100, 240  ]
# last = 0
# for i in range(count.__len__()):
#     strip.fill_smooth(count[i],last, speed[i], 0xFFFF0000)
#     last = count[i]
#     time.sleep(1.0 / 12)

# music pulse 2
count = [60, 30, 24, 8, 51, 60, 12, 0, 9, 15, 46, 44, 22, 18, 35, 36, 34, 12, 22, 0]
speed = [240, 200, 250, 300, 180, 320, 180, 240, 100, 240, 240, 200, 250, 300, 180, 320, 180, 240, 100, 240]
last = 0
for i in range(count.__len__()):
    strip.fill_smooth(count[i], 0, speed[i], 0xFFFF0000)
    while (strip.get_brightness(0) > 0xE0):
        strip.dim(count[i]-1)
        time.sleep(1.0 / 64)
    time.sleep(1.0 / 12)

# for c in count:
#     strip.fill(c, 0xE1ff00ff)
#     time.sleep(1.0 / 5)
# while count <= 60:
#     count += 1
#     strip.fill(count, 0xE1ff0000)
#     time.sleep(1.0 / 2)

# while True:
#     strip.start_rotate()
#     time.sleep(1)
#     strip.stop_rotate()
#     time.sleep(1)

# breath effect:
# strip.show_colors(list(getColors()))
# down = True
# while True:
#     if down:
#         strip.dim()
#     else:
#         strip.brighten()
#     brightness = strip.getColor(0) >> 24
#     if brightness == 0xE0:
#         down = False
#     if brightness == 0xFF:
#         down = True
#     time.sleep(1.0 / 20)