import pygame
from pygame.color import THECOLORS
from pygame.locals import *
import easygui

import pykinect
from pykinect import nui
from pykinect.nui import JointId

from led_sign import LedSign, SerialMock

import itertools

DEPTH_WINSIZE = (320,240)
VIDEO_WINSIZE = (640,480)


screen = None
dispInfo = None
s=None

SKELETON_COLORS = [THECOLORS["red"], 
                   THECOLORS["blue"], 
                   THECOLORS["green"], 
                   THECOLORS["orange"], 
                   THECOLORS["purple"], 
                   THECOLORS["yellow"], 
                   THECOLORS["violet"]]

LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

KINECTEVENT = pygame.USEREVENT

def draw_skeleton_data(pSkelton, index, positions, width = 4):
    global screen
    global dispInfo
    start = pSkelton.SkeletonPositions[positions[0]]
       
    for position in itertools.islice(positions, 1, None):
        next = pSkelton.SkeletonPositions[position.value]
        
        curstart = skeleton_to_depth_image(start, dispInfo.current_w, dispInfo.current_h) 
        curend = skeleton_to_depth_image(next, dispInfo.current_w, dispInfo.current_h)

        pygame.draw.line(screen, SKELETON_COLORS[index], curstart, curend, width)
        
        start = next

def draw_skeletons(skeletons):
    global screen
    global dispInfo
    for index, data in enumerate(skeletons):
        # draw the Head
        HeadPos = skeleton_to_depth_image(data.SkeletonPositions[JointId.Head], dispInfo.current_w, dispInfo.current_h) 
        draw_skeleton_data(data, index, SPINE, 10)
        pygame.draw.circle(screen, SKELETON_COLORS[index], (int(HeadPos[0]), int(HeadPos[1])), 20, 0)
    
        # drawing the limbs
        draw_skeleton_data(data, index, LEFT_ARM, 10)
        draw_skeleton_data(data, index, RIGHT_ARM, 10)
        # draw_skeleton_data(data, index, LEFT_LEG)
        # draw_skeleton_data(data, index, RIGHT_LEG)

def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

def main():
    """Initialize and run the game"""
    pygame.init()
 
    global dispInfo

    # Initialize PyGame
    global screen
    screen = pygame.display.set_mode(VIDEO_WINSIZE, 0, 32)

    pygame.display.set_caption("PyKinect Video Example")
    
    sign = LedSign.load("sign.txt")
    frame_num = 0
    with nui.Runtime() as kinect:
        kinect.skeleton_frame_ready += post_frame
        kinect.skeleton_engine.enabled = True
        # Main game loop
        while (True):
            frame_num += 1
            dispInfo = pygame.display.Info()
            events = pygame.event.get()
            for event in events:
                if (event.type == pygame.QUIT):
                    break
                elif event.type == KINECTEVENT:
                    skeletons = event.skeletons
                    screen.fill(THECOLORS["black"])
                    draw_skeletons(skeletons)
            sign.update(screen,events)
            # sign.draw(screen)
            pygame.display.flip()
if (__name__ == "__main__"):
    main()
