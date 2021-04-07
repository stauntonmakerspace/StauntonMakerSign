import numpy
import pygame
import scipy
import scipy.ndimage
from led_sign import LedSign
import cv2

pygame.init()

window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

window_size = window.get_size()
scale = 4
sim_size = (window_size[0]//scale,window_size[1]//scale)
dampening = 0.9

current = numpy.zeros(sim_size, numpy.float32)
previous = numpy.zeros(sim_size, numpy.float32)
kernel = numpy.array([[0.0, .5, 0], 
                      [.5, 0, .5],
                     [0, .5, 0]])
sign = LedSign.load("sign.txt","/dev/cu.usbserial-1410")

run = True
while run:
    clock.tick(24)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break
        
    if any(pygame.mouse.get_pressed()):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (mouse_pos[0]//scale,mouse_pos[1]//scale)
        previous[mouse_pos] = 10000

    if numpy.random.randint(10) > 8:
        y = numpy.random.randint(0, sim_size[0])
        x = numpy.random.randint(0, sim_size[1])
        previous[(y,x)] = 10000
    current = (scipy.ndimage.convolve(previous, kernel) - current) * dampening

    array =  numpy.around(numpy.clip(current, 0, 255))

    dim = numpy.ones_like(array)
    array = numpy.stack((array, dim * 255, numpy.clip(array * dim * 125, 0, 255)), axis=2).astype('uint8')

    array = cv2.blur(array, (5,5))
    array = cv2.cvtColor(array, cv2.COLOR_HSV2RGB)

    
    array = cv2.resize(array, dsize=window_size[::-1], interpolation=cv2.INTER_CUBIC)
    pygame.surfarray.blit_array(window, array)
    sign.update(window, events)
    sign.draw(window)
    pygame.display.flip()

    previous, current = current, previous

pygame.quit()
exit()    