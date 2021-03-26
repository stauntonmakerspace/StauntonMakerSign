from led_sign import LedSign
import serial
import pygame

FPS = 20
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True
try:
    ser = serial.Serial('/dev/cu.usbserial-1420', 500000)
except:
    class SerialMock():
        def __init__(self):
            print("WARNING: Running with mock serial. No commands will actually be sent to connected devices")
        def write(self, bytes):
            pass
    ser = SerialMock()

sign = LedSign(
    [[10, 10, 10],# M 
    [10, 10, 10], # a
    [10, 10, 10], # k
    [10, 10, 10],# e
    [10, 10, 10], # r
    [10, 10, 10],# S
    [10, 10, 10],# p
    [10, 10, 10],# a
    [10, 10, 10],# c
    [10, 10, 10]]# e
    , ser)

sign.adjustable = True

rect = pygame.rect.Rect(0, 0, width//5, height)
v = [30, 0]
while running:
    events = pygame.event.get()
    running = not any([event.type == pygame.QUIT for event in events])
    
    rect.move_ip(v)

    if rect.left < 0:
        v[0] *= -1
    if rect.right > width:
        v[0] *= -1
    if rect.top < 0:
        v[1] *= -1
    if rect.bottom > height:
        v[1] *= -1
   
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255,0,255), rect)

    sign.update(screen, events)
    sign.draw(screen)

    pygame.display.flip()
    # - constant game speed / FPS -
    clock.tick(FPS)