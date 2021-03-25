from sign_code import LedSign
import serial
import pygame

FPS = 20
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True

led_cnts = [[10, 20,10,20],# M
            [4, 20, 20], # a
            [5, 20], # k
            [10, 20],# e
            [6, 20], # r
            [10, 20],# S
            [10, 20],# p
            [10, 20],# a
            [10, 20],# c
            [10, 20],# e
          ]

ser = serial.Serial('/dev/cu.usbserial-1430', 500000)
sign = LedSign(led_cnts, ser)
sign.adjustable = True
sign.showing = True

rect = pygame.rect.Rect(0, 0, 640, 300)
v = [0, 4]
while running:
    events = pygame.event.get()
    running = not any([event.type == pygame.QUIT for event in events])
    
    rect.move_ip(v)

    if rect.left < 0:
        v[0] *= -1
    if rect.right > 640:
        v[0] *= -1
    if rect.top < 0:
        v[1] *= -1
    if rect.bottom > 480:
        v[1] *= -1
   
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,0,255), rect)

    sign.update(screen, events)
    pygame.display.flip()
    # - constant game speed / FPS -
    clock.tick(FPS)