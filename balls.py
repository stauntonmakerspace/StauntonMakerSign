import balls_lib
import pygame
from makersign import LedSign

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = screen.get_size()
sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")

balls_lib.show_balls(screen, sign)