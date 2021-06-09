import numpy as np
import cv2
import numpy
import pygame
from makersign import LedSign
import cv2
import time
cap = cv2.VideoCapture('water.mp4')

pygame.init()

window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

window_size = window.get_size()

sign = LedSign.load("sign.txt")
sign.attach("COM3")

sign.adjustable = True

start = False
updates = []
run = True
record = False
frames = [] # Resizing frames gets really expensive so it might be better off


print("Loading video")

ret, frame = cap.read() 
frame = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
frame -= frame % 100
frames.append(frame)

while (run and ret) and not start:
    events = pygame.event.get()
    try:
        if record:
            for _ in range(2):
                ret, frame = cap.read()
            if ret:
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
                frame = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                frame -= frame % 100
                frames.append(frame)
                pygame.surfarray.blit_array(window, frame)
            else:
                start = True 

        if record and ret:
            updates.append(sign.update(window, events, return_changes=True))
        else:
            sign.update(window, events)
        sign.draw(window)
        pygame.display.flip()

    except Exception as e:
        print(e)
    
    for event in events:
        if event.type == pygame.QUIT:   
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                if not record:
                    record = True
                else:
                    start = True

cap.release()
print(run, record, start)
print("Playing Back")
frame_data = list(zip(updates, frames))
sign.adjustable = False
while (run and start):
    for cmd_data, frame in frame_data:
        clock.tick(15)
        for cmd in cmd_data:
            sign.send_cmd(*cmd)
            # time.sleep(5e-5) # 50 MicroSeconds  
        pygame.surfarray.blit_array(window, frame)
        sign.draw(window)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    