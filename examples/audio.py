# Print out realtime audio volume as ascii bars

import sounddevice as sd
import numpy as np
from led_sign import LedSign
import pygame
from colour import Color
FPS = 24
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
data = 0
red = Color("green")
colors = list(red.range_to(Color("red"),bars))
MAX = 1

viz = [pygame.rect.Rect(i * (width // bars), 0, width // bars, height) for i in range(bars)]

def print_sound(indata, frames, time, status):
    global data
    volume_norm = np.linalg.norm(indata)
    data += volume_norm
    data /= 2

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

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
        cut_off = int(data * bars)
        for i, rect in enumerate(viz[:cut_off]):
            pygame.draw.rect(screen, (int(colors[i].red * 255), int(colors[i].green* 255), int(colors[i].blue* 255)), rect)

        sign.update(screen, events)
        sign.draw(screen)
        pygame.display.update()


   
