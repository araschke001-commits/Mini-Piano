from machine import Pin, I2C, PWM
from neopixel import NeoPixel
import time

### Set up capacitive touch sensors ###
i2c = I2C(
    0,
    sda=Pin(20),
    scl=Pin(21),
    freq=100000
)

TOUCH_ADDRESS = 0x1C

def readRegister(register):
    # Read one register from the touch controller.
    return i2c.readfrom_mem(
        TOUCH_ADDRESS,
        register,
        1
    )[0]

def readTouches():
    # Return a 12-bit integer describing touched keys.
    low = readRegister(3)
    high = readRegister(4)

    return low | (high << 8)

def isTouched(key):
    # Return True if the specified key is touched.
    if not 0 <= key <= 11:
        raise ValueError("Key must be between 0 and 11")

    return bool(readTouches() & (1 << key))

# Check whether the controller responds
devices = i2c.scan()
print("I2C devices:", [hex(address) for address in devices])

if TOUCH_ADDRESS not in devices:
    raise RuntimeError("AT42QT2120 not found")


### Set up switches ###
leftButton = Pin(0, Pin.IN, Pin.PULL_UP)
selectButton = Pin(1, Pin.IN, Pin.PULL_UP)
rightButton = Pin(2, Pin.IN, Pin.PULL_UP)


### Set up rotary encoder ###
rotA = Pin(17, Pin.IN, Pin.PULL_UP)
rotB = Pin(18, Pin.IN, Pin.PULL_UP)
rotSW = Pin(19, Pin.IN, Pin.PULL_UP)


### Set up speaker (piezo buzzer) ###
speaker = PWM(Pin(16))
speaker.duty_u16(0) # Mute to start so it doesn't start playing instantly

def startNote(hertz, volume):
    speaker.freq(hertz)
    speaker.duty_u16(volume)

def stopNote():
    speaker.duty_u16(0)

def playNote(hertz, volume, duration):
    startNote(hertz, volume)
    time.sleep_ms(duration)
    stopNote()


### Set up leds (neopixels) ###
leds = NeoPixel(Pin(26), 3)

def setLedValue(index, r, g, b):
    leds[index] = (r, g, b)

def setLeds(ledValues):
    for i in range(len(ledValues)):
        setLedValue(i, leds[i].index(1), leds[i].index(2), leds[i].index(3))
    leds.write()

while True:
    ### Variables ###
    MIN_OCTAVE = 1
    MAX_OCTAVE = 7
    octave = 4 # Start at the same octave as middle c
    # The note hertz values for easier retrievals (also used to retrieve note from key), only using sharps, not flats
    notesHz = {
        "c": 262,
        "c#": 277,
        "d": 294,
        "d#": 311,
        "e": 330,
        "f": 349,
        "f#": 370,
        "g": 392,
        "g#": 415,
        "a": 440,
        "a#": 466,
        "b": 494
    }

    keysPressed = [] # Keeps track of which notes are already played to determine last one pressed.
    lastKeyPressed = -1 # Keeps track of which note should play, as a number for the key, from 0-12. Is -1 when no key is pressed

    # Used to detect which buttons are pressed
    leftButtonPressed = False
    selectButtonPressed = False
    rightButtonPressed = False
    

    ### Read cts input ###
    for key in range(12):
        # If this is the first "frame" in which the key has been pressed for, it is the most recently pressed and gets added to keysPressed
        if isTouched(key) and key not in keysPressed:
            lastKeyPressed = key
            keysPressed.append(key)
        else:
            # Remove that key from keysPressed (if it is in keysPressed) to show that it isn't pressed anymore
            for i in range(len(keysPressed)):
                if keysPressed[i] == key:
                    del keysPressed[i]


    ### Read switch input ###
    if leftButton.value() == 0:
        leftButtonPressed = True

    if leftButton.value() == 0:
        leftButtonPressed = True

    if leftButton.value() == 0:
        leftButtonPressed = True


    ### Read rotary encoder input ###
    if rotA.value() != lastRotA: # Value changed, so it is rotating
        if rotB.value() != rotA.value(): # Rotated clockwise
            pass
        else: # Rotated counter-clockwis
            pass
    
    lastRotA = rotA.value()

    if rotSW.value() == 0:
        pass
        time.sleep_ms(200) # Used for debouncing, MAY HAVE TO CHANGE TO ALLOW FOR OTHER INPUTS AT THE SAME TIME AS DELAY


    ### Set speaker output ###
    startNote(1000, 10000)


    ### Set leds output ###
    setLeds([])


    time.sleep_ms(5)