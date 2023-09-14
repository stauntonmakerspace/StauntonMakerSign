import pygame
from makersign import LedSign
import random

pygame.display.set_caption('Quick Start')
pygame.font.init()
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
r = 4
g = 7
b = 88
while clearRunning:
    clock.tick(60)
    x += 3
    rect=(x, 160, 30, 200)
    screen.fill("black")
    pygame.draw.rect(screen, pygame.Color(r,g,b), rect)
    font = pygame.font.SysFont("arial", size=100)
    text = font.render("{}".format("Clearing Sign"), True, "Blue")
    screen.blit(text, (300, 500))
    text = font.render("{}".format("Enter a word or phrase for someone to guess!"), True, "Blue")
    screen.blit(text, (300, 650))
    text = font.render("{}".format("No capital letters.  Press esc to confirm your entry"), True, "Blue")
    screen.blit(text, (300, 800))
    if x % 5 ==0:
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)

    sign.sample_surface(screen)
    sign.draw(screen)
    pygame.display.flip()
    if x > 1360:
        clearRunning = False
