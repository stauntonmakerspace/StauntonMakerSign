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
a = 0
x = 10
y = 160
d = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(40):
        if a % 5 == 0:
            pygame.draw.rect(screen, "blue", rect=(x, 160, 30, 200))
            if d == True:
                pygame.draw.rect(screen, "black", rect=(x - 20, 160, 10, 200))
                x += 1
                if a % 30 == 0:
                    y += 1
            elif not d:
                pygame.draw.rect(screen, "black", rect=(x + 35, 160, 10, 200))
                x -= 1
                if a % 30 == 0:
                    y -= 1
            if x > 1350:
                d = False
                x = 1350
            elif x < 15:
                d = True
                x = 15

    sign.sample_surface(screen)
    sign.draw(screen)

    pygame.display.flip()
