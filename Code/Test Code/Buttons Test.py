from machine import Pin
import time

leftButton = Pin(0, Pin.IN, Pin.PULL_UP)
selectButton = Pin(1, Pin.IN, Pin.PULL_UP)
rightButton = Pin(2, Pin.IN, Pin.PULL_UP)

while True:
    if leftButton.value() == 0:
        print("Left button pressed")
    
    if selectButton.value() == 0:
        print("Select button pressed")

    if rightButton.value() == 0:
        print("Right button pressed")
    
    time.sleep_ms(20)