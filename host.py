from sign_code import LedSign
import serial
import pygame

FPS = 20
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True
# led_counts = { 0: 151, 1: 57, 2: 10, 3: 10, 4: 10, 5: 10, 6: 10, 7: 10, 8: 10, 9: 10 },
led_cnts = [[10, 10],# M 
            [10, 10], # a
            [10, 10], # k
            [10, 10],# e
            [10, 10], # r
            [10, 10],# S
            [10, 10],# p
            [10, 10],# a
            [10, 10],# c
            [10, 10],# e
          ]
try:
    ser = serial.Serial('/dev/cu.usbserial-1420', 500000)
except:
    class SerialMock():
        def __init__(self):
            pass
        def write(self, bytes):
            pass
    ser = SerialMock()
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