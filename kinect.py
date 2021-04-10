import thread
import pygame
import cv2 
from pykinect import nui
from led_sign import LedSign, SerialMock
# pip  install opencv-python==4.2.0.32
DEPTH_WINSIZE = (320,240)
FULL_WINSIZE = (-1,-1)
screen_lock = thread.allocate()
screen = None
fg_frame = None

tmp_s = pygame.Surface(DEPTH_WINSIZE, 0, 16)
backSub = cv2.bgsegm.createBackgroundSubtractorGSOC()

def depth_frame_ready(frame):
    global fg_frame
    with screen_lock:
        # ? Room for speed up in these operations
        frame.image.copy_bits(tmp_s._pixels_address)
        
        arr2d = (pygame.surfarray.pixels2d(tmp_s) >> 7) & 255
        arr2d = arr2d.astype('float32')
        backtorgb = cv2.cvtColor(arr2d,cv2.COLOR_GRAY2RGB)
        ksize = (5, 5)
        fg = backSub.apply(backtorgb)
        fg = cv2.blur(fg, ksize)
        fg = cv2.resize(fg, FULL_WINSIZE[::-1], interpolation=cv2.INTER_NEAREST).astype("int32")
        fg_frame = fg

def main():
    """Initialize and run the game."""
    pygame.init()

    # Initialize PyGame
    global screen
    global FULL_WINSIZE
    global fg_frame

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    FULL_WINSIZE = pygame.display.get_surface().get_size()

    pygame.display.set_caption('PyKinect LED Sign Depth Code')
    
    sign = LedSign.load("sign.txt")
    sign.attach("COM3")        

    with nui.Runtime() as kinect:
        kinect.depth_frame_ready += depth_frame_ready   
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)


        # Main game loop
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        break
            if type(fg_frame) != type(None):
                pygame.surfarray.blit_array(screen, fg_frame)
                sign.update(screen, events)
                sign.draw(screen)
            pygame.display.update()

if __name__ == '__main__':
    main()