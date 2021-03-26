"""
A simple Kinect game using PyGame.
"""

import pygame
import pygame.color
from pykinect import nui, JointId

KINECTEVENT = pygame.USEREVENT
WINDOW_SIZE = 640, 480

def post_frame(frame):
    """Get skeleton events from the Kinect device and post them into the PyGame
    event queue."""
    try:
        pygame.event.post(
            pygame.event.Event(KINECTEVENT, skeletons=frame.SkeletonData)
        )
    except:
        # event queue full
        pass

def main():
    """Initialize and run the game."""
    pygame.init()

    # Initialize PyGame
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 16)
    pygame.display.set_caption('Python Kinect Game')
    screen.fill(pygame.color.THECOLORS["black"])

    with nui.Runtime() as kinect:
        kinect.skeleton_engine.enabled = True
        kinect.skeleton_frame_ready += post_frame

        # Main game loop
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                break
            elif event.type == KINECTEVENT:
                skeletons = event.skeletons 
                     
                for index, data in enumerate(skeletons): # index for users
                    # get head position 
                    head_positions = data.SkeletonPositions[JointId.Head] 
                    # handle limbs - left arm 
                    LEFT_ARM = (JointId.ShoulderCenter, 
                    JointId.ShoulderLeft, 
                    JointId.ElbowLeft, JointId.WristLeft, JointId.HandLeft)
                    left_arm_positions = [data.SkeletonPositions[x] for x in LEFT_ARM]
                    print(left_arm_positions)
                pass

if __name__ == '__main__':
    main()