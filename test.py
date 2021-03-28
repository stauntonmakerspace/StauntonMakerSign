import thread
import pygame
import cv2 
from pykinect import nui
from led_sign import LedSign, SerialMock
# pip  install opencv-python==4.2.0.32
DEPTH_WINSIZE = (320,240)

screen_lock = thread.allocate()
screen = None

tmp_s = pygame.Surface(DEPTH_WINSIZE, 0, 16)
backSub = cv2.bgsegm.createBackgroundSubtractorGSOC()

def depth_frame_ready(frame):
    with screen_lock:
        frame.image.copy_bits(tmp_s._pixels_address)
        arr2d = (pygame.surfarray.pixels2d(tmp_s) >> 7) & 255
        arr2d = arr2d.astype('float32')
        backtorgb = cv2.cvtColor(arr2d,cv2.COLOR_GRAY2RGB)
        fg = backSub.apply(backtorgb).astype("int32")
        pygame.surfarray.blit_array(screen, fg)
        pygame.display.update()


def main():
    """Initialize and run the game."""
    pygame.init()

    # Initialize PyGame
    global screen
    screen = pygame.display.set_mode(DEPTH_WINSIZE)
    pygame.display.set_caption('PyKinect Depth Map Example')

    with nui.Runtime() as kinect:
        kinect.depth_frame_ready += depth_frame_ready   
        kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

        # Main game loop
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                break

if __name__ == '__main__':
    main()