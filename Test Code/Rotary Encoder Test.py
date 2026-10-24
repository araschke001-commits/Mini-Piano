from machine import Pin
import time

rotA = Pin(17, Pin.IN, Pin.PULL_UP)
rotB = Pin(18, Pin.IN, Pin.PULL_UP)
rotButton = Pin(19, Pin.IN, Pin.PULL_UP)

lastRotA = rotA.value()

while True:

    if rotA.value() != lastRotA: # Value changed, so it is rotating
        if rotB.value() != rotA.value():
            print("Clockwise")
        else:
            print("Counter-Clockwise")

    lastRotA = rotA.value()

    if rotButton.value() == 0:
        print("Button pressed")
        time.sleep_ms(200) # Used for debouncing
    
    time.sleep_ms(1)