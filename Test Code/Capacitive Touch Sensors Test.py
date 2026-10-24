from machine import Pin, I2C
import time

# I2C0: SDA = GP20, SCL = GP21
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

while True:
    for key in range(12):
        if isTouched(key):
            print(f"Key {key} is touched")
    time.sleep_ms(50)