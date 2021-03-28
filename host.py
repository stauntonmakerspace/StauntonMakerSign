from led_sign import LedSign, SerialMock
import serial
import pygame

FPS = 24
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True

# sign = LedSign(
#     [[10, 10, 10],# M 
#     [10, 10, 10], # a
#     [10, 10, 10], # k
#     [10, 10, 10],# e
#     [10, 10, 10], # r
#     [10, 10, 10],# S
#     [10, 10, 10],# p
#     [10, 10, 10],# a
#     [10, 10, 10],# c
#     [10, 10, 10]])# e
# sign.save("sign.txt")
sign = LedSign.load("sign.txt")

try:
    ser = serial.Serial('/dev/cu.usbserial-1420', 500000)
except:
    ser = SerialMock()
sign.attach(ser)
sign.adjustable = True

rect = pygame.rect.Rect(0, 0, width//5, height)
v = [20, 0]
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sign.save("sign.txt")
        if event.type == pygame.QUIT:
            running = False
    
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