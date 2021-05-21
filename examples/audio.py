# Print out realtime audio volume as ascii bars

import sounddevice as sd
import numpy as np
from makersign import LedSign
import pygame
from colour import Color

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("MakerSign Recording System")

clock = pygame.time.Clock()

running = True

sign = LedSign.load("sign.txt")
sign.attach("COM3")

sign.adjustable = True

bars = 50
avg = 30
data = [0 for _ in range(avg)]
red = Color("green")
colors = list(red.range_to(Color("red"),bars))
MAX = 1

viz = [pygame.rect.Rect(i * (width // bars), 0, width // bars, height) for i in range(bars)]

def print_sound(indata, frames, time, status):
    global data
    volume_norm = np.linalg.norm(indata)
    data.append(volume_norm)
    data = data[1:]

with sd.InputStream(device=0, channels=1, callback=print_sound):
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        screen.fill((0, 0, 0))
        cut_off = int((sum(data)/avg) * bars)
        for i, rect in enumerate(viz[:cut_off]):
            pygame.draw.rect(screen, (int(colors[i].red * 255), int(colors[i].green* 255), int(colors[i].blue* 255)), rect)

        sign.update(screen, events)
        sign.draw(screen)
        pygame.display.update()