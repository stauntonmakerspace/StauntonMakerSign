import pygame
import pygame_gui
import cv2
import os
from makersign import LedSign

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((1400, 900))
window_size = window_surface.get_size()

background = pygame.Surface((1400, 900))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((1400, 900))

prev_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 475), (100, 50)),
                                            text='Prev',
                                            manager=manager)

next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((550, 475), (100, 50)),
                                            text='Next',
                                            manager=manager)

exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 475), (100, 50)),
                                            text='Exit',
                                            manager=manager)
sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")

video_dir = "videos"
video_index = 0 
video_files = [os.path.join(video_dir, i) for i in os.listdir(video_dir) if ".mp4" in i]
video_handle = cv2.VideoCapture(video_files[video_index])
loaded = True

clock = pygame.time.Clock()
is_running = True

while is_running:  
    time_delta = clock.tick(24)/1000.0
    events = list(pygame.event.get())
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == next_button:
                    video_index += 1
                    video_index %= len(video_files)
                    loaded = False
                elif event.ui_element == prev_button:
                    video_index -= 1
                    video_index %= len(video_files)
                    loaded = False
                elif event.ui_element == exit_button:
                    exit()

        manager.process_events(event)
    
    ret, frame = video_handle.read() 
    if ret and loaded:
        frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.resize(frame, dsize=window_size[::-1], interpolation=cv2.INTER_NEAREST)
        # frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        # TODO: Delegate color space limiting to the LedSign object it makes more sense and limits unnecessary computation
        # frame -= frame % 100 # Reduce Collor Space and limit serial communication

        pygame.surfarray.blit_array(window_surface, frame)
        sign.update(window_surface, events)
        sign.draw(window_surface)
    else:
        video_handle = cv2.VideoCapture(video_files[video_index])
        loaded = True

    manager.update(time_delta)
    manager.draw_ui(window_surface)

    pygame.display.update()