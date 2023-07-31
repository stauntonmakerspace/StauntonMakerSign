import pygame
from makersign import LedSign

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = screen.get_size()
screen.fill("blue")
screen.fill("black")

window_width = screen.get_width()
window_height = screen.get_height()

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")

running = True
color = "green"
a = 0
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if a % 30 == 0:
        if color == "green":
            color = "blue"
        elif color == "blue":
            color = "green"
        screen.fill(color, rect=(0, 0, 1536, 960 / 3 + 50))
    sign.sample_surface(screen)
    sign.draw(screen)

    pygame.display.flip()