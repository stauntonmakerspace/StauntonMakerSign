
import serial
import pygame

class LedStrip():
    def __init__(self, led_cnt):
        self.startpoint = pygame.math.Vector2(0, 0)
        self.endpoint = pygame.math.Vector2(led_cnt, led_cnt)
        self.led_cnt = led_cnt
        self.last_samples = [(0,0,0),] * led_cnt

    def set_endpoint(self, endpoint):
        self.endpoint = self.startpoint - ((self.startpoint - endpoint).normalize() * self.led_cnt * 10 )

    def set_startpoint(self, startpoint):
        self.startpoint = self.endpoint - ((self.endpoint - startpoint).normalize() * self.led_cnt * 10 )

    def sample_screen(self, screen_cap):
        unit_vector = (self.startpoint - self.endpoint) / self.led_cnt
        samples = []
        for i in range(self.led_cnt):
            sample_point = self.startpoint + (unit_vector * i)
            sample = (0,0,0) # Do Code
            if sample == self.last_samples[i]:
                sample = (-1,-1,-1)
            else:
                self.last_samples[i] = sample
            samples.append(sample)
        return samples

    def draw(self, screen):
        pygame.draw.line(screen, (255, 0, 0),
                         self.startpoint, self.endpoint, 2)

class LedSymbol():
    def __init__(self, strip_lengths):
        self.strips = []
        for length in strip_lengths:
            self.strips.append(LedStrip(length))

    def update_with(self, screen_cap):
        rgb_cmds = []
        for strip in self.strips:
            rgb_cmds += strip.sample_screen(screen_cap)
        return rgb_cmds

    def draw(self, screen):
        for strip_num in range(len(self.strips) - 1):
            self.strips[strip_num].draw(screen)
            pygame.draw.line(
                screen, (0, 0, 255), self.strips[strip_num].endpoint, self.strips[strip_num + 1].startpoint, 2)
        self.strips[-1].draw(screen)

    def closest_control(self, vector):
        return 0,0,0


class LedSign():
    def __init__(self, led_cnts, ser):
        self.symbols = []
        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
        self.ser = ser
        self.active_control = None # (symbol number: int, strip number: int, Is start point: bool)

    def closest_control(self, vector):
        closest = 10e10
        out = None
        for i in range(len(self.symbols)):
            dist, strip, is_start = self.symbols[i].closest_control(vector)
            if dist < closest and dist < 15:
                out = (i, strip, is_start)
        return out

    def draw(self, screen):
        for symbol in self.symbols:
            symbol.draw(screen)

    def update(self, screen, events):
        """ cmd_bytearray
        0: Singifies the start of a cmd
        1: How many more times should the cmd be echod before it is executed.py
        2: Which LED should the color values be assigned to. Set to 255 in order to display all set colors
        3: Red color values 0 - 255
        4: Green color values 0 - 255
        6: Blue color values 0 - 255
        """
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.active_control = self.closest_control(None)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.active_control = None

            elif event.type == pygame.MOUSEMOTION:
                if self.active_control != None:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.active_control[2]:
                        self.symbols[self.active_control[0]].strips[self.active_control[1]].set_startpoint(point)
                    else:
                        self.symbols[self.active_control[0]].strips[self.active_control[1]].set_endpoint(point)

        screen_cap = pygame.surfarray.array2d(screen)
        for i in range(len(self.symbols) - 1, -1, -1):
            cmds = self.symbols[i].update_with(screen_cap)
            led_num = 0
            for cmd in cmds:
                if cmd[0] != -1:
                    values = bytearray([ord('#'), i, led_num, cmd[0], cmd[1], cmd[2]])
                    # self.ser.write(values)
                led_num += 1
            # self.ser.write(bytearray(['#', i, 255, 0, 0, 0]))

FPS = 30
pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Drawing System")

clock = pygame.time.Clock()

running = True

led_cnts = [[10, 20],
            [4, 20],
            [5, 20],
            [10, 20],
            [6, 20],
            [10, 20],
            [10, 20],
            [10, 20],
            [10, 20],
            [10, 20],
          ]

ser = None # serial.Serial('/dev/ttyACM0', 500000, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
sign = LedSign(led_cnts, ser)

while running:
    events = pygame.event.get()
    running = not any([event.type == pygame.QUIT for event in events])

    sign.update(screen, events)

    screen.fill((0, 0, 0))
    sign.draw(screen)
    pygame.display.flip()
    # - constant game speed / FPS -
    clock.tick(FPS)