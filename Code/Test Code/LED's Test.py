# More iffy on whether or not it will work

import neopixel
from machine import Pin

leds = neopixel.NeoPixel(Pin(16), 3)

leds[0] = (255, 0, 0) # Red
leds[1] = (0, 255, 0) # Green
leds[2] = (0, 0, 255) # blue

leds.write()