from sign_code import LedSign
import serial
import pygame

FPS = 30
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True

led_cnts = [[10, 20],
            [4, 20],
            [5, 20],
            [10, 20],
            [6, 20],
            [10, 20],
            [10, 20],
            [10, 20],
            [10, 20],
            [10, 20],
          ]

ser = None # serial.Serial('/dev/ttyACM0', 500000, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
sign = LedSign(led_cnts, ser)
sign.adjustable = True
rect = pygame.rect.Rect(100, 50, 50, 50)
v = [2, 2]
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
    pygame.draw.rect(screen, (255,0,0), rect)

    sign.update(screen, events)
    sign.draw(screen)
    pygame.display.flip()
    # - constant game speed / FPS -
    clock.tick(FPS)