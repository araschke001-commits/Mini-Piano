from machine import Pin, I2C, PWM
from Modules.rotary_irq_rp2 import RotaryIRQ
from neopixel import NeoPixel
import time


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

# Switch debouncing variables
leftSwTime = 0
modeSwTime = 0
rightSwTime = 0
SW_DEBOUNCE_MS = 50

# Used to change the mode, modes range from 1 to 3

# Mode 1 = play normally, stopping when no key is pressed
# Mode 2 = play like the pedal is pressed, making notes last for longer but not merging them
# Mode 3 = play the average hertz of all of the keys that are currently pressed

mode = 1

# Used to detect rotary encoder rotation and button press
volume = 25 # Used for the volume from 0% - 100%, starts at 25% and is changed by the rotary encoder's rotation
muted = False # Volume is muted / unmuted when rotary encoder's switch is pressed



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
modeButton = Pin(1, Pin.IN, Pin.PULL_UP)
rightButton = Pin(2, Pin.IN, Pin.PULL_UP)


### Set up rotary encoder ###
encoder = RotaryIRQ(
    pin_num_clk=17,
    pin_num_dt=18,
    min_val=10000,
    max_val=10000,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_UNBOUNDED,
    half_step=True # CRITICAL for 36 detent / 18 pulse encoders
)

# Initialize push button (Internal pull-up since encoder switch connects to GND)
button = Pin(19, Pin.IN, Pin.PULL_UP)

# Track the encoder baseline
lastRotation = encoder.value()

# Rotary encoder button debounce variables
rotEncSwTime = 0
ROT_ENC_DEBOUNCE_MS = 200

def buttonCallback(pin):
    global rotEncSwTime, muted
    currentTime = time.ticks_ms() # MS since board startup

    # Check if enough itme has passed to clear switch bounce
    if time.ticks_diff(currentTime, rotEncSwTime) > ROT_ENC_DEBOUNCE_MS:
        # Check if the button is pressed
        if pin.value() == 0:
            muted = not muted
        rotEncSwTime = currentTime

# Attach an interrupt to the button pin
button.irq(handler=buttonCallback, trigger=Pin.IRQ_FALLING)


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
        setLedValue(i, ledValues[i][0], ledValues[i][1], ledValues[i][2])
    leds.write()

while True:
    ### Read cts input ###
    anyKeyTouched = False
    for key in range(12):
        # If this is the first "frame" in which the key has been pressed for, it is the most recently pressed and gets added to keysPressed
        if isTouched(key):
            anyKeyTouched = True
            if key not in keysPressed:
                lastKeyPressed = key
                keysPressed.append(key)
        else:
            # Remove that key from keysPressed (if it is in keysPressed) to show that it isn't pressed anymore
            for i in range(len(keysPressed)):
                if keysPressed[i] == key:
                    del keysPressed[i]

    # Handle if 2+ keys are pressed and the last key is released before the others
    if lastKeyPressed not in keysPressed and len(keysPressed) > 0:
        # Last key in the list is the most recently added, so it should be the next last key
        lastKeyPressed = keysPressed[-1]

    # If no keys are pressed, reset lastKeyPressed to -1 to signify that no keys are pressed
    if anyKeyTouched == False:
        lastKeyPressed = -1


    ### Read switch input ###
    currentTime = time.ticks_ms()

    # If button pressed and time since last press passes debounce time
    if leftButton.value() == 0 and time.ticks_diff(currentTime, leftSwTime) > SW_DEBOUNCE_MS:
        octave -= 1
        leftSwTime = currentTime

        # Lowest octave is 1, don't allow beneath that
        if octave < 1:
            octave = 1

    if modeButton.value() == 0 and time.ticks_diff(currentTime, modeSwTime) > SW_DEBOUNCE_MS:
        mode += 1
        modeSwTime = currentTime

        # Wrap around mode number
        if mode > 3: # Number is the number of modes there are
            mode = 1

    if rightButton.value() == 0 and time.ticks_diff(currentTime, rightSwTime) > SW_DEBOUNCE_MS:
        octave += 1
        rightSwTime = currentTime

        # Highest octave is 7, don't allow above that
        if octave > 7:
            octave = 7


    ### Read rotary encoder rotation ###
    currentRotation = encoder.value()

    # Change the volume by 2 each time the rotary encoder rotates 1 detent
    if currentRotation != lastRotation: # Value changed, so it is rotating
        # Calculate how many rotations happened & direction of them
        volume += (currentRotation - lastRotation) * 2 # Volume goes by 2 in the direction of the rotary encoder's rotation: clockwise = up 2, counter = down 2

        # Clamp volume between 0 and 100, inclusive
        if volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
    
    lastRotation = currentRotation

    # Rotary encoder switch is already handled by buttonCallback in setup


    ### Set speaker output ###

    # Mode 1 = play normally, stopping when no key is pressed
    # Mode 2 = play like the pedal is pressed, making notes last for longer but not merging them
    # Mode 3 = play the average hertz of all of the keys that are currently pressed
    
    if not muted:
        if lastKeyPressed == -1: # No key pressed
            if mode == 1 or mode == 3:
                stopNote()
            else: # mode == 2
                startNote(speaker.freq(), max(0, round(speaker.duty_u16() - ((volume/100) * 65535 * (1/400))))) # Make the volume go continuously down for 2 seconds
        else:
            # Used to index the keys of notesHz to find which note should be played from the pad number
            notesList = list(notesHz.keys())

            if mode == 1 or mode == 2:
                # Index the keys of notesHz to find which note should be played from the pad number
                note = notesList[lastKeyPressed]

                # Plays the hertz of the note most recently and currently pressed, multiplied by (2 ^ the octave minus the default of 4) for shifting octaves, at the volume from 0 - 65535 (speaker's max) based off of the volume percentage
                startNote(round(notesHz[note] * (2 ** (octave - 4))), round((volume/100) * 65535))
            else: # mode == 3
                # Retrieve the average hertz from the list of keys currently pressed
                notes = [notesList[key] for key in keysPressed]
                playedNotesHz = [notesHz[note] for note in notes]
                avgHz = sum(playedNotesHz) / len(playedNotesHz)

                # Plays the average hertz of all the notes currently pressed, multiplied by (2 ^ the octave minus the default of 4) for shifting octaves, at the volume from 0 - 65535 (speaker's max) based off of the volume percentage
                startNote(round(avgHz * (2 ** (octave - 4))), round((volume/100) * 65535))
    else:
        # If muted == True, don't play anything
        stopNote()


    ### Set leds output ###
    modeLEDs = (255 * (mode == 1), 255 * (mode == 2), 255 * (mode == 3))
    volumeLEDs = (255 * round(volume / 100) * (not muted), 255 * round(volume / 100) * (not muted), 255 * round(volume / 100) * (not muted))
    setLeds([(100, 100, 100), modeLEDs, volumeLEDs])


    time.sleep_ms(5)