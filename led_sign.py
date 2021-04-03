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
    def __init__(self, led_cnt, origin = pygame.math.Vector2(0, 0), scale = 4):
        self.origin = origin
        self.scale = scale

        self.drag_start = None

        self.initialized = False 
        self.start_control = None
        self.end_control = None
        self.hold = 0

        self.led_cnt = led_cnt

        # Store the last record values in order to prevent sending duplicates unnecessrily
        self.last_samples = [(0, 0, 0), ] * led_cnt

    def setup(self, vector):
        if self.start_control == None:
            self.start_control = vector
        else:
            self.move_end_control(vector)
            self.initialized = True

    def draw(self, screen):
        if self.initialized:
            mid = self.start_control - ((self.start_control - self.end_control) / 2)
            pygame.draw.line(screen, (255, 0, 255),
                            self.start_control, self.end_control, 6)
            
            pygame.draw.circle(screen, (255, 255, 255),
                            (int(mid.x),  int(mid.y)), 4)
            pygame.draw.circle(screen, (0, 0, 255),
                            (self.start_control.x,  self.start_control.y), 4)
            pygame.draw.circle(screen, (255, 0, 0),
                            (self.end_control.x,  self.end_control.y), 4)

    def adjust_controls(self, vector):
        mid = self.start_control - ((self.start_control - self.end_control) / 2)
        if vector.x == -1:
            self.hold = 0
        if (self.start_control.distance_to(vector) < 4) or self.hold == 1:
            self.move_start_control(vector)
            self.hold = 1
            return True
        elif (self.end_control.distance_to(vector) < 4) or self.hold == 2:
            self.move_end_control(vector)
            self.hold = 2
            return True
        elif (mid.distance_to(vector) < 4) or self.hold == 3:
            if self.hold != 3:
                self.drag_start = vector
                self.start_control_old = self.start_control
                self.end_control_old = self.end_control
                self.hold = 3
            dist = self.drag_start - vector
            self.start_control = self.start_control_old - dist
            self.end_control = self.end_control_old - dist
            return True
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
        else:
            return [(-1, -1, -1), ] * self.led_cnt

    def save(self):
        if self.initialized:
            return self.start_control, self.end_control, self.led_cnt
        else:
            return pygame.math.Vector2(0,0), pygame.math.Vector2(1,1), self.led_cnt

    def move_end_control(self, vector):
        self.end_control = self.start_control - \
            ((self.start_control - vector).normalize()
             * self.led_cnt * self.scale)

    def move_start_control(self, vector):
        self.start_control = self.end_control - \
            ((self.end_control - vector).normalize()
             * self.led_cnt * self.scale)

class LedSymbol():
    def __init__(self, strip_lengths = None, origin = None):
        self.strips = []
        if origin == None:
            self.origin = pygame.math.Vector2(0, 0)
        for length in strip_lengths:
            self.strips.append(LedStrip(length))
        self.initialized = False
        self.hold = -1
        self.drag_start = None
        self.old_strips = []

    def setup(self, vector):
        strip = None
        for strip in self.strips:
            if not strip.initialized:
                strip.setup(vector)
                break
        self.initialized = all([strip.initialized for strip in self.strips])

    def draw(self, screen):
        if self.initialized:
            try:
                for strip_num in range(len(self.strips) - 1):
                    self.strips[strip_num].draw(screen)
                    pygame.draw.line(
                        screen, (0, 0, 255), self.strips[strip_num].end_control, self.strips[strip_num + 1].start_control, 1)
                self.strips[-1].draw(screen)
                
                pygame.draw.circle(screen, (255, 255, 0),
                                (self.strips[0].start_control.x - 15,  self.strips[0].start_control.y - 15), 4)
            except:
                pass

    def adjust_controls(self, vector):
        if vector.x == -1: # Not Release
            if self.hold == 0:
                self.strips = self.old_strips 
                pass
            self.hold = -1 # Release

        if self.hold != -1:
            if self.hold == 0:
                temp = self.old_strips
                diff = self.drag_start - vector
                for i in range(len(temp)):
                    temp[i].start_control -= diff
                    temp[i].end_control -= diff
                self.strips = temp

            else:
                self.strips[self.hold - 1].adjust_controls(vector)
        else:
            if self.strips[0].start_control.distance_to(vector) < 50:
                self.old_strips = self.strips
                self.drag_start = vector
                self.hold = 0
                return True
            else:
                adjusted = False
                for i, strip in enumerate(self.strips):
                    adjusted = strip.adjust_controls(vector)
                    if adjusted and vector.x != -1:
                        self.hold = i + 1
                        break
                return adjusted
        return False

    def drag(self, vector):
        
        pass

    def update(self, screen_cap):
        rgb_cmds = []
        for strip in self.strips:
            rgb_cmds += strip.get_samples(screen_cap)
        return rgb_cmds

    def save(self):
        cntrls = []
        for strip in self.strips:
            cntrls.append(strip.save())
        return cntrls


class LedSign(): # ! Should handle all pygame screen/eventinteractions
    def __init__(self, led_cnts, serial_port = None, origin = None):
        self.symbols = []
        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
        self.attach(serial_port)
        if origin == None:
            self.origin = pygame.math.Vector2(0, 0)
        
        self.hold = 0

        self.initialized = False
        self.adjustable = True

    def setup(self, vector):
        symbol = None 
        for symbol in self.symbols:
            if not symbol.initialized:
                symbol.setup(vector)
                break
        self.initialized = all([symbol.initialized for symbol in self.symbols])

    def draw(self, screen): # ! Move symbol draw code into here
        # * TODO Draw Drag Control 
        for symbol in self.symbols:
            symbol.draw(screen)

    def adjust_controls(self, vector, hold = None):
        if (self.origin.distance_to(vector) < 4):
            self.origin = vector
            return True
        return False

    def update(self, screen, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.adjustable:
                        if not self.adjust_controls(point):
                            for i, symbol in enumerate(self.symbols): # Find first control point within adjustable range and stop 
                                adjusted = symbol.adjust_controls(point)
                                if adjusted:
                                    self.hold = i
                                    break
                    
            elif event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.hold != -1:
                        self.symbols[self.hold].adjust_controls(point)
                    
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(-1, -1)
                    for symbol in self.symbols: # Find first control point within adjustable range and stop 
                        symbol.adjust_controls(point)
                    self.hold = -1
                              
    
        for i in range(len(self.symbols) - 1, -1, -1): # Update in reverse to limit downtime. Since symbols are daisychained
            cmds = self.symbols[i].update(screen)
            updated = False
            for led_num, cmd in enumerate(cmds):
                if cmd[0] != -1: # Do not update LEDs that have not changed to save bandwidth 
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
                    cntrl_vectors.append(pygame.math.Vector2(int(x1), int(y1)))
                    cntrl_vectors.append(pygame.math.Vector2(int(x2), int(y2)))
        temp = LedSign(led_cnts)
        for vector in cntrl_vectors:
            temp.setup(vector)
        assert(temp.initialized == True)
        return temp

    def save(self, filename):
        with open(filename, 'w') as filehandle:
            for symbol in self.symbols:
                filehandle.write('#\n')
                for strip in symbol.save():
                    start, end, cnt = strip
                    filehandle.write("{} {} {} {} {}\n".format(int(start.x), int(start.y), int(end.x), int(end.y), cnt))

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
            self.ser = None # SerialMock()
        
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
            pass
            print("DEBUG: Device: {0} Led: {1} R: {2} G: {3} B: {4}".format(device_num, led_num, R, G, B))
