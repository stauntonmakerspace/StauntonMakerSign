import pygame
from makersign import LedSign

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = screen.get_size()


window_width = screen.get_width()
window_height = screen.get_height()

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")
screen.fill("blue")
screen.fill("black")


clearRunning = True
a = 0
x = 10
d = True
clock = pygame.time.Clock()
clearCount = 1
rect = None
while clearRunning:
    clock.tick(60)
    x += 5
    rect=(x, 160, 30, 200)
    screen.fill("black")
    pygame.draw.rect(screen, "blue", rect)

    sign.sample_surface(screen)
    sign.draw(screen)
    pygame.display.flip()
    if x > 1360:
        clearRunning = False
