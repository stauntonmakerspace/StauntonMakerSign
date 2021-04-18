import numpy as np
import cv2
import numpy
import pygame
from led_sign import LedSign
import cv2
import time
cap = cv2.VideoCapture('rainbow.mp4')

pygame.init()

window = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
clock = pygame.time.Clock()

window_size = window.get_size()

sign = LedSign.load("sign.txt")
sign.attach("COM3")

sign.adjustable = True

run = True
ret = True
frames = [] # Resizing frames gets really expensive so it might be better off

ret, frame = cap.read() 
frame = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
frame -= frame % 100
frames.append(frame)
print("loading video")
start = False
while run and ret:
    events = pygame.event.get()
    try:
        if start:
            ret, frame = cap.read() 
            ret, frame = cap.read() 
            if ret:
                frame = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
                frame -= frame % 100
                frames.append(frame)
                pygame.surfarray.blit_array(window, frame)
            else:
                cap.release()
                break       
        else:
            pygame.surfarray.blit_array(window, frame)
        
        sign.update(window, events)
        sign.draw(window)
        pygame.display.flip()
    except Exception as e:
        print(e)
        break
    
    for event in events:
        if event.type == pygame.QUIT:   
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break
            if event.key == pygame.K_RIGHT:
                ret = False
                break
            if event.key == pygame.K_DOWN:
                sign.recording = True
                start = True
                break
print("Playing Back")
sign.recording = False
sign.adjustable = False
frame_data = zip(sign.record, frames)
while run == True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:   
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break
    for cmd_data, frame in frame_data:
        clock.tick(60)
        for cmd in cmd_data:
            sign.send_cmd(*cmd)
            # time.sleep(5e-5) # 50 MicroSeconds  
        pygame.surfarray.blit_array(window, frame)
        sign.draw(window)
        pygame.display.flip()