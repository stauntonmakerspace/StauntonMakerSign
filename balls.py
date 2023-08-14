from math import pi
import random
import pygame
import PyParticles

from makersign import LedSign

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = screen.get_size()

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")

universe = PyParticles.Environment(window_size)
universe.colour = (0,0,0)
universe.addFunctions(['move', 'bounce', 'collide', 'drag', 'accelerate'])
max_size = 20
universe.assignMaxBallSize(max_size)
colors = [(255,0,0),(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255)]
p = 25
for i in range(p):
    universe.addParticles(mass=max_size, size=max_size, speed=5, elasticity=1, colour=colors[i%len(colors)])

selected_particle = None
paused = False
running = True
a = 0
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    a+= 1
    
    # if a > 10000: running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_particle = universe.findParticle(*pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
    
    if selected_particle:
        selected_particle.mouseMove(pygame.mouse.get_pos())
    if not paused:
        universe.update()
        
    screen.fill(universe.colour)
    
    for p in universe.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, 0)

    for s in universe.springs:
        pygame.draw.aaline(screen, (0,0,0), (int(s.p1.x), int(s.p1.y)), (int(s.p2.x), int(s.p2.y)))
    sign.sample_surface(screen)
    sign.draw(screen)

    pygame.display.flip()
