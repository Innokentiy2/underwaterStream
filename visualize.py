import serial
import pygame
import sys

PORT = "COM4"        
BAUD = 9600
FRAME_W = 8
FRAME_H = 8
PIXEL_SIZE = 50

ser = serial.Serial(PORT, BAUD, timeout=1)

pygame.init()
screen = pygame.display.set_mode((FRAME_W * PIXEL_SIZE, FRAME_H * PIXEL_SIZE))
pygame.display.set_caption("Laser Video Receiver")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

frame = [0] * FRAME_H

def draw_frame():
    screen.fill(WHITE)
    for y in range(FRAME_H):
        row = frame[y]
        for x in range(FRAME_W):
            bit = (row >> x) & 1
            color = BLACK if bit else WHITE
            pygame.draw.rect(
                screen,
                color,
                (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE)
            )
            pygame.draw.rect(
                screen,
                GRAY,
                (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                1
            )
    pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ser.close()
            pygame.quit()
            sys.exit()

    line = ser.readline().decode(errors="ignore").strip()

    if line.startswith("FRAME_BYTES:"):
        try:
            data = line.replace("FRAME_BYTES:", "")
            values = [int(v) for v in data.split(",")]
            if len(values) == FRAME_H:
                frame = values
                draw_frame()
        except:
            pass