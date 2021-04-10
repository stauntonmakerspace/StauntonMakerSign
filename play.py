import numpy as np
import cv2
import numpy
import pygame
from led_sign import LedSign
import cv2
cap = cv2.VideoCapture('rainbow.mp4')

pygame.init()

window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

window_size = window.get_size()

sign = LedSign.load("sign.txt")
sign.attach("COM3")
run = True
while(cap.isOpened() and run):

    ret, frame = cap.read() 
    #cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    if ret:
        clock.tick(24)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
        array = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
        pygame.surfarray.blit_array(window, array)
        sign.update(window, events)
        sign.draw(window)
        pygame.display.flip()
    else:
       print('no video')
       cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


cap.release()
cv2.destroyAllWindows()