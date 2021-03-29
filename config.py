from led_sign import LedSign
import pygame

FPS = 24
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True

# sign = LedSign(
#     [[10, 26, 10, 30, 27, 9, 26, 12],   # M 
#     [7, 3, 3, 3, 7, 13, 3, 6, 4, 8],    # a
#     [10, 28, 8, 12, 7, 12, 7],          # k
#     [13, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], # e
#     [12, 16, 8, 6, 5],                  # r
#     [3, 6, 3, 3, 9, 3, 4, 6, 3 ],       # S
#     [7, 15, 12, 6, 7],                  # p
#     [5, 20, 18, 7, 8],                  # a
#     [3, 3, 5, 5, 5, 5, 5, 5],           # c
#     [11, 4, 6, 7, 9, 9, 7]              # e
#     ])

# sign.save("sign.txt")

sign = LedSign.load("sign.txt")
sign.attach("COM3")

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
    
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

    pygame.display.update()
    # - constant game speed / FPS -
    clock.tick(FPS)