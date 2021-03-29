import serial

import serial.tools.list_ports
import pygame
import pickle


class SerialMock():
    def __init__(self):
        print("WARNING: Running with mock serial. No commands will actually be sent to connected devices")

    def write(self, bytes):
        pass
class LedStrip():
    def __init__(self, led_cnt, origin = pygame.math.Vector2(0, 0), scale = 1):
        self.origin = origin
        self.scale = scale

        self.initialized = False 
        self.led_cnt = led_cnt

        # Store the last record values in order to prevent sending duplicates unnecessrily
        self.last_samples = [(0, 0, 0), ] * led_cnt

        self.start_control = None 
        self.end_control = None
    
    def setup(self, vector):
        if self.start_control == None:
            self.start_control = vector
        else:
            self.move_end_control(vector)
            self.initialized = True

    def draw(self, screen):
        if self.initialized:
            pygame.draw.line(screen, (255, 0, 255),
                            self.start_control, self.end_control, 6)
            pygame.draw.circle(screen, (0, 0, 255),
                            (self.start_control.x,  self.start_control.y), 4)
            pygame.draw.circle(screen, (255, 0, 0),
                            (self.end_control.x,  self.end_control.y), 4)

    def adjust_controls(self, vector = None):
        if vector != None:
            pass
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             self.active_control = self.closest_control(point)

        #     elif event.type == pygame.MOUSEMOTION:
        #         if self.active_control != None:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             if self.active_control[2] == 1:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].move_start_control(
        #                     point)
        #             else:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].move_end_control(
        #                     point)
        return False

    def get_samples(self, screen_cap):
        if self.initialized:
            unit_vector = (
                (self.start_control - self.end_control).normalize() * self.scale)
            samples = []
            for i in range(self.led_cnt):
                sample_point = self.start_control - (unit_vector * i)
                try:
                    sample = screen_cap.get_at(
                        (int(sample_point.x), int(sample_point.y)))[:-1]  # Remove A from RGBA
                except:
                    sample = (-1, -1, -1)
                if sample == self.last_samples[i]:
                    samples.append((-1, -1, -1))
                else:
                    self.last_samples[i] = sample
                    samples.append(sample)
            return samples 

    def save(self):
        if self.initialized:
            return self.start_control, self.end_control, self.led_cnt
        else:
            return pygame.math.Vector2(0,0), pygame.math.Vector2(10,10), self.led_cnt

    def move_end_control(self, vector):
        self.end_control = self.start_control - \
            ((self.start_control - vector).normalize()
             * self.led_cnt * self.scale)

    def move_start_control(self, vector):
        self.start_control = self.end_control - \
            ((self.end_control - vector).normalize()
             * self.led_cnt * self.scale)

class LedSymbol():
    def __init__(self, strip_lengths):
        self.initialized = False
        self.strips = []
        for length in strip_lengths:
            self.strips.append(LedStrip(length))

    def setup(self, vector):
        strip = next(iter(filter(lambda x: x.initialized ==
                            False, self.strips)), None)
        if strip != None:
            strip.setup(vector)
        else:
            self.initialized = True

    def draw(self, screen):
        if self.initialized:
            for strip_num in range(len(self.strips) - 1):
                self.strips[strip_num].draw(screen)
                pygame.draw.line(
                    screen, (0, 0, 255), self.strips[strip_num].end_control, self.strips[strip_num + 1].start_control, 1)
            self.strips[-1].draw(screen)
            
            pygame.draw.circle(screen, (255, 255, 255),
                            (self.strips[0].start_control.x - 15,  self.strips[0].start_control.y - 15), 4)

    def adjust_controls(self, vector):
        for strip in self.strips:
            adjusted = strip.adjust_controls(vector)
            if adjusted:
                break
        return False

    def update(self, screen_cap):
        if self.initialized:
            rgb_cmds = []
            for strip in self.strips:
                rgb_cmds += strip.get_samples(screen_cap)
            return rgb_cmds

    def save(self):
        cntrls = []
        for strip in self.strips:
            cntrls.append(strip.save())
        return cntrls

    def closest_control(self, vector):
        # (dist: float, strip number: int, Is start point: bool)
        closest = 10e10
        out = None
        for i, strip in enumerate(self.strips):
            d1 = strip.start_control.distance_to(vector)
            if d1 < closest:
                closest = d1
                out = (d1, i, 1)
            d2 = strip.end_control.distance_to(vector)
            if d2 < closest:
                closest = d2
                out = (d2, i, 0)
        return out


class LedSign(): # ! Should handle all pygame screen/eventinteractions
    def __init__(self, led_cnts, serial_port = None):
        self.symbols = []
        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
        self.attach(serial_port)

        self.active_control = None
        self.initialized = False
        self.adjustable = True

    def setup(self, vector):
        symbol = next(iter(filter(lambda x: x.initialized ==
                             False, self.symbols)), None)
        if symbol != None:
            symbol.setup(vector)
        else:
            self.initialized = True

    def draw(self, screen): # ! Move symbol draw code into here
        # * TODO Draw Drag Control 
        for symbol in self.symbols:
            symbol.draw(screen)

    def adjust_controls(self, point):
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             if not self.initialized:
        #                 self.setup(point)
        #             else:
        #                 self.active_control = self.closest_control(point)

        #     elif event.type == pygame.MOUSEBUTTONUP:
        #         if event.button == 1:
        #             self.active_control = None

        #     elif event.type == pygame.MOUSEMOTION:
        #         if self.active_control != None:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             if self.active_control[2] == 1:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].move_start_control(
        #                     point)
        #             else:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].move_end_control(
        #                     point)
        return False

    def update(self, screen, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.adjustable:
                        if not self.adjust_controls(point):
                            for symbol in self.symbols: # Find first control point within adjustable range and stop 
                                adjusted = symbol.adjust_controls(point)
                                if adjusted:
                                    break
        if self.initialized:
            for i in range(len(self.symbols) - 1, -1, -1): # Update in reverse to limit downtime. Since symbols are daisychained
                cmds = self.symbols[i].update(screen, events)
                updated = False
                for led_num, cmd in enumerate(cmds):
                    if cmd[0] != -1: # Do not update LEDs that have not changed 
                        updated = True
                        self.send_cmd(i, led_num, cmd[0], cmd[1], cmd[2])
                if updated:
                    self.send_cmd(i, 255, 0, 0, 0)

    @staticmethod
    def load(filename):
        cntrl_vectors = []
        led_cnts = []

        # open file and read the content in a list
        with open(filename, 'r') as filehandle:
            for line in filehandle:
                if "#" in line:
                    led_cnts.append([])
                else:
                    x1,y1,x2,y2,led_cnt = line.split()
                    if any([v == -1 for v in [x1,y1,x2,y2,led_cnt]]): break
                    led_cnts[-1].append(int(led_cnt))
                    cntrl_vectors.append(pygame.math.Vector2(int(x1)+100, int(y1)+100))
                    cntrl_vectors.append(pygame.math.Vector2(int(x2)+150, int(y2)+150))

        temp = LedSign(led_cnts)
        for vector in cntrl_vectors:
            temp.setup(vector)
        return temp

    def save(self, filename):
        with open(filename, 'w') as filehandle:
            for symbol in self.symbols:
                filehandle.write('#\n')
                for strip in symbol.save():
                    start, end, cnt = strip
                    filehandle.write("{} {} {} {} {}\n".format(int(start.x), int(start.y), int(end.x), int(end.y), cnt))
                    
    def closest_control(self, vector):
        # (symbol number: int, strip number: int, Is start point: bool)
        closest = 10e10
        out = None
        for i, symbol in enumerate(self.symbols):
            best = symbol.closest_control(vector)
            if best != None:
                dist, strip, is_start = best
                if dist < closest and dist < 40:
                    out = (i, strip, is_start)
        return out

    def attach(self, serial_port):
        try: 
            if serial_port == None:
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if "COM" in p:
                        serial_port = p
            self.ser = serial.Serial(serial_port, 500000)
        except Exception as e:
            print(e)
            self.ser = SerialMock()
        
    def send_cmd(self, device_num, led_num, R, G, B):
        """ cmd_bytearray
        0: Singifies the start of a cmd
        1: How many more times should the cmd be echod before it is executed.py
        2: Which LED should the color values be assigned to. Set to 255 in order to display all set colors
        3: Red color values 0 - 255
        4: Green color values 0 - 255
        6: Blue color values 0 - 255
        """

        values = [ord('#'), device_num, led_num, R, G, B]
        if self.ser != None:
            self.ser.write(bytearray(values))
        else:
            print("DEBUG: Device: {0} Led: {1} R: {2} G: {3} B: {4} \n WARNING No serial object is attached".format(device_num, led_num, R, G, B))
