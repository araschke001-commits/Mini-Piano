from machine import Pin, PWM
import time

speaker = PWM(Pin(15))

def startNote(hertz, volume):
    speaker.freq(hertz)
    speaker.duty_u16(volume)

def stopNote():
    speaker.duty_u16(0)

def playNote(hertz, volume, duration):
    startNote(hertz, volume)
    time.sleep_ms(duration)
    stopNote()

playNote(262, 10000, 500) # C4

playNote(294, 20000, 250) # D4

playNote(330, 10000, 1000) # E4

speaker.deinit()