import time
from picamera2 import Picamera2
from PIL import Image
import numpy as np
from gpiozero import OutputDevice
 

RELAY_GPIO = 17
BIT_S = 0.25
FRAME_W = 8
FRAME_H = 8
THRESHOLD = 128


relay = OutputDevice(RELAY_GPIO, active_high=True, initial_value=False)

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (320, 240)})
picam2.configure(config)
picam2.start()
time.sleep(2)

def laser_on():
    relay.on()

def laser_off():
    relay.off()

def send_bit(bit_value):
    if bit_value:
        laser_on()
    else:
        laser_off()
    time.sleep(BIT_S)

def send_byte(value):
    for i in range(8):
        bit_value = (value >> i) & 1
        send_bit(bit_value)

def send_sync():
    send_byte(0xAA)
    send_byte(0x55)

def capture_frame_bytes():
    arr = picam2.capture_array()
    img = Image.fromarray(arr)

    img = img.convert("L")

    img = img.resize((FRAME_W, FRAME_H))

    img = img.point(lambda p: 255 if p > THRESHOLD else 0)

    pixels = np.array(img)
    frame_bytes = []

    for y in range(FRAME_H):
        value = 0
        for x in range(FRAME_W):
            bit = 1 if pixels[y, x] > 0 else 0
            value |= (bit << x)
        frame_bytes.append(value)

    return frame_bytes, img

def print_frame(frame_bytes):
    print("FRAME:")
    for b in frame_bytes:
        row = ""
        for x in range(FRAME_W):
            row += "#" if ((b >> x) & 1) else "."
        print(row)
    print()

try:
    while True:
        frame_bytes, img = capture_frame_bytes()
        print_frame(frame_bytes)

        send_sync()
        for b in frame_bytes:
            send_byte(b)

        laser_off()
        time.sleep(1)

except KeyboardInterrupt:
    laser_off()
    picam2.close()
