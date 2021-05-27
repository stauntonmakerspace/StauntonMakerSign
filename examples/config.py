from makersign import LedSign
import pygame

FPS = 24
pygame.init()

screen = pygame.display.set_mode((1400, 900))
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("MakerSign Drawing System")

clock = pygame.time.Clock()

running = True

sign = LedSign.load("sign.txt")
sign.attach("COM3")

sign.adjustable = True

rect = pygame.rect.Rect(0, 0, width//5, height)
rect2 = pygame.rect.Rect(width - (width//5), 0, width//5, height)
rect3 = pygame.rect.Rect(0, 0, width, height//4)
v = [20, 0]
v2 = [-20, 0]
v3 = [0, 20]
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                sign.save("sign.txt")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sign.clean()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break
    
    rect.move_ip(v)
    rect2.move_ip(v2)
    rect3.move_ip(v3)

    if rect.left < 0:
        v[0] *= -1
    if rect.right > width:
        v[0] *= -1
    if rect.top < 0:
        v[1] *= -1
    if rect.bottom > height:
        v[1] *= -1
    
    if rect2.left < 0:
        v2[0] *= -1
    if rect2.right > width:
        v2[0] *= -1
    if rect2.top < 0:
        v2[1] *= -1
    if rect2.bottom > height:
        v2[1] *= -1

    if rect3.left < 0:
        v3[0] *= -1
    if rect3.right > width:
        v3[0] *= -1
    if rect3.top < 0:
        v3[1] *= -1
    if rect3.bottom > height:
        v3[1] *= -1
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (0,255,0), rect3)
    pygame.draw.rect(screen, (0,0,255), rect)

    pygame.draw.rect(screen, (255,0,0), rect2)

    sign.update(screen, events)
    sign.draw(screen)

    pygame.display.update()
    # - constant game speed / FPS -
    clock.tick(FPS)
