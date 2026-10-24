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
    ### Read cts input ###
    for key in range(12):
        if isTouched(key):
            pass


    ### Read switch input ###
    pass


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