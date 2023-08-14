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



def clearScreen():
    global x
    global a
    for i in range(20):
        if a % 5 == 0:
            if x < 1360:
                pygame.draw.rect(screen, "blue", rect=(x, 160, 30, 200))
                #pygame.draw.rect(screen, "black", rect=(x - 20, 160, 10, 200))
                x += 1
            else:
                return False
    return True


clearRunning = True
a = 0
x = 10
d = True
clock = pygame.time.Clock()
clearCount = 1
while clearRunning:
    clock.tick(60)
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            clearRunning = False
    clearRunning = clearScreen()
    clearCount = 0


    sign.sample_surface(screen)
    sign.draw(screen)

    pygame.display.flip()
