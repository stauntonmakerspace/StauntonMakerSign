import pygame
import cv2 
from makersign import LedSign

pygame.init()

# Initialize PyGame
global screen
global FULL_WINSIZE
global fg_frame

screen = pygame.display.set_mode((1400, 900))
clock = pygame.time.Clock()
FULL_WINSIZE = pygame.display.get_surface().get_size()
OP_WINSIZE = (350, 225)

pygame.display.set_caption('LED Sign Depth Code')

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")

cam = cv2.VideoCapture(0)
backSub = cv2.bgsegm.createBackgroundSubtractorGSOC()
    
# Main game loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cam.release()
                running = False
                break
    ret, frame = cam.read() 
    if ret:
        frame = cv2.resize(frame, dsize=OP_WINSIZE, interpolation=cv2.INTER_NEAREST)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        ksize = (7, 7)
        blur_frame = cv2.blur(frame, ksize)
        mask_frame = backSub.apply(blur_frame)

        frame = cv2.resize(frame, dsize=FULL_WINSIZE, interpolation=cv2.INTER_NEAREST)
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        mask_frame = cv2.resize(mask_frame, dsize=FULL_WINSIZE, interpolation=cv2.INTER_NEAREST)
        mask_frame = cv2.rotate(mask_frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        pygame.surfarray.blit_array(screen, mask_frame.astype("int32"))    
        sign.update(screen, events)
        and_frame = cv2.bitwise_and(frame, frame, mask=mask_frame)
        pygame.surfarray.blit_array(screen, and_frame.astype("int32"))    
        sign.draw(screen)
        pygame.display.update()
        clock.tick(30)


