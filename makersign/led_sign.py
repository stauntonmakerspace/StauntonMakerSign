import serial
import time
import serial.tools.list_ports
import pygame

class SerialMock():
    def __init__(self):
        print("WARNING: Running with mock serial. No commands will actually be sent to connected devices")

    def write(self, _bytes):
        print(_bytes)

class LedStrip():
    def __init__(self, led_cnt, scale=4):
        self.initialized = False
        self.scale = scale

        self.start_control = None
        self.end_control = None

        self.led_cnt = led_cnt

    def setup(self, vector):
        if self.start_control == None:
            self.start_control = vector
        else:
            self.move_end_control(vector)
            self.initialized = True

    def save(self):
        if self.initialized:
            return self.start_control, self.end_control, self.led_cnt
        else:
            return pygame.math.Vector2(0, 0), pygame.math.Vector2(1, 1), self.led_cnt

    def shift_controls(self, mouse_vector):
        mid = self.start_control - \
            ((self.start_control - self.end_control) / 2)
        diff = mouse_vector - mid
        self.start_control += diff
        self.end_control += diff

    def move_end_control(self, mouse_vector):
        self.end_control = self.start_control - \
            ((self.start_control - mouse_vector).normalize()
             * self.led_cnt * self.scale)

    def move_start_control(self, mouse_vector):
        self.start_control = self.end_control - \
            ((self.end_control - mouse_vector).normalize()
             * self.led_cnt * self.scale)

    def get_control_points(self):
        return [self.start_control, self.end_control]
    
    def process_events(self, event):
        pass 

class LedSymbol():
    def __init__(self, strip_lengths=None, position=None):
        self.position = position if position != None else pygame.math.Vector2(
            100, 100)

        self.strips = []
        for length in strip_lengths:
            self.strips.append(LedStrip(length))

        self.initialized = False

    # TODO: Somethings wrong with this set up function it doesnt work in a nice way idk what it is yet 
    def setup(self, vector):
        strip = None
        for strip in self.strips:
            if not strip.initialized:
                strip.setup(vector)
                break
        self.initialized = all([strip.initialized for strip in self.strips])

    def save(self):
        cntrls = []
        for strip in self.strips:
            cntrls.append(strip.save())
        return cntrls

    def set_position(self, position):
        self.position = position

    def get_control_points(self):
        return [strip.get_control_points() for strip in self.strips]

    def process_events(self, event):
        pass 

class LedSign():  # ! Should handle all pygame screen/event interactions
    def __init__(self, led_cnts, serial_port=None, position=None):
        self.position = position if position != None else pygame.math.Vector2(
            0, 0)
        self.frame_updates = []
        self.symbols = []
        # Store the last record values in order to prevent sending duplicates unnecessrily
        self.symbol_history = []

        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
            self.symbol_history.append([(0, 0, 0), ] * sum(cnts))

        self.attach(serial_port)

        self.hold_state = [0, 0, 0, 0]  # Dragging, Symbol_Num, Strip_Num, Is_Start

        self.adjustable = False
        self.holding = False
        self.initialized = False

    def set_position(self, position):
        self.position = position
    
    def setup(self, vector):
        symbol = None
        for symbol in self.symbols:
            if not symbol.initialized:
                symbol.setup(vector)
                break
        self.initialized = all([symbol.initialized for symbol in self.symbols])

    def sample_surface(self, screen, return_only = False):
        changes = []
        for num, symbol in reversed(list(enumerate(self.symbols))):
            led_num = 0
            updated = False
            for strip in symbol.strips:
                start, end = strip.get_control_points()
                start = start + self.position + symbol.position
                end = end + self.position + symbol.position
                unit_vector = ((end - start).normalize() * 4)
                for i in range(strip.led_cnt):
                    sample_point = start + (unit_vector * i)
                    try:
                        sample = screen.get_at(
                            (int(sample_point.x), int(sample_point.y)))[:-1]  # Remove A from RGBA
                        pygame.draw.circle(screen, (0, 255, 0), (int(
                            sample_point.x),  int(sample_point.y)), 1)
                    except:
                        sample = (0, 255, 0)
                    if sample != self.symbol_history[num][led_num]:
                        self.symbol_history[num][led_num] = sample
                        updated = True
                        changes.append([num, led_num, sample[0], sample[1], sample[2]])
                        if not return_only:
                            self.send_cmd(num, led_num, *sample)
                    led_num += 1

            if updated:
                changes.append([num, 255, 0, 0, 0])
                if not return_only:
                    self.send_cmd(num, 255, 0, 0, 0)
        return changes
    
    def draw(self, screen):
        if self.adjustable:
            pygame.draw.circle(screen, (255, 100, 0),
                            (self.position.x,  self.position.y), 10)
        for symbol in self.symbols:
            cntrl_pnts = symbol.get_control_points()
            pose = self.position + symbol.position
            if self.adjustable:
                pygame.draw.circle(screen, (255, 100, 0),
                                (pose.x,  pose.y), 10)
            for i in range(len(cntrl_pnts)):
                start, end = cntrl_pnts[i]
                start = start + self.position + symbol.position
                end = end + self.position + symbol.position
                mid = start - ((start - end) / 2)

                pygame.draw.line(screen, (255, 0, 255),
                                 start, end, 6)
                if self.adjustable:
                    pygame.draw.circle(screen, (255, 255, 255),
                                    (int(mid.x),  int(mid.y)), 4)

                    pygame.draw.circle(screen, (0, 255, 0),
                                    (start.x,  start.y), 4)

                    pygame.draw.circle(screen, (255, 0, 0),
                                    (end.x,  end.y), 4)
                if i >= 1:
                    pygame.draw.line(screen, (0, 0, 255),
                                     start, pose + cntrl_pnts[i - 1][1], 2)

    def clean(self):
        for symbol in self.symbols:
            pnts = symbol.get_control_points()
            MAX = pygame.math.Vector2(0, 0)
            MIN = pygame.math.Vector2(10e5, 10e5)
            for pair in pnts:
                for pnt in pair:
                    if pnt.x > MAX.x:
                        MAX.x = pnt.x
                    if pnt.y > MAX.y:
                        MAX.y = pnt.y
                    if pnt.x < MIN.x:
                        MIN.x = pnt.x - 20
                    if pnt.y < MIN.y:
                        MIN.y = pnt.y - 20
            for strip in symbol.strips:
                strip.end_control -= MIN
                strip.start_control -= MIN

    def adjust_controls(self, vector = None):
        if self.holding:
            if self.hold_state[0] == 1:  # Sign Control Clicked
                self.position = vector
            elif self.hold_state[1] > 0:  # Symbol Control Clicked
                if self.hold_state[2] > 0:  # Strip Control Clicked
                    if self.hold_state[3] == 1:  # Dragging Start
                        self.symbols[self.hold_state[1] - 1].strips[self.hold_state[2] - 1].move_start_control(
                            vector - self.symbols[self.hold_state[1] - 1].position - self.position)
                    elif self.hold_state[3] == 2:
                        self.symbols[self.hold_state[1] - 1].strips[self.hold_state[2] - 1].move_end_control(
                            vector - self.symbols[self.hold_state[1] - 1].position - self.position)
                    elif self.hold_state[3] == 3:
                        self.symbols[self.hold_state[1] - 1].strips[self.hold_state[2] - 1].shift_controls(
                            vector - self.symbols[self.hold_state[1] - 1].position - self.position)
                else:
                    self.symbols[self.hold_state[1] -
                                    1].set_position(vector - self.position)
                return True
        else:
            self.hold_state = [0, 0, 0, 0]
            # Determine which control to consider held
            if self.position.distance_to(vector) < 15:
                self.hold_state[0] = 1
                return True 

            for symbol_num, symbol in enumerate(self.symbols):

                if (self.position + symbol.position).distance_to(vector) < 10:
                    self.hold_state[1] = symbol_num + 1
                    return True

                for strip_num, points in enumerate(symbol.get_control_points()):

                    start, end = points[0], points[1]

                    start = start + self.position + symbol.position
                    end = end + self.position + symbol.position
                    mid = start - ((start - end) / 2)

                    if start.distance_to(vector) < 5:
                        self.hold_state[1] = symbol_num + 1
                        self.hold_state[2] = strip_num + 1
                        self.hold_state[3] = 1
                        return True

                    elif end.distance_to(vector) < 5:
                        self.hold_state[1] = symbol_num + 1
                        self.hold_state[2] = strip_num + 1
                        self.hold_state[3] = 2
                        return True

                    elif mid.distance_to(vector) < 5:
                        self.hold_state[1] = symbol_num + 1
                        self.hold_state[2] = strip_num + 1
                        self.hold_state[3] = 3
                        return True
        return False

    def process_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                point = pygame.math.Vector2(mouse_x, mouse_y)
                self.adjust_controls(point)
                self.holding = True

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            point = pygame.math.Vector2(mouse_x, mouse_y)
            self.adjust_controls(point)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.holding = False 

    @staticmethod
    def load(filename, port=None):
        cntrl_vectors = []
        led_cnts = []
        poses = [] 

        # open file and read the content in a list
        with open(filename, 'r') as filehandle:
            for line in filehandle:
                data = line.split()
                if len(data) == 5:
                    x1, y1, x2, y2, led_cnt = [int(i) for i in data]
                    if any([v == -1 for v in [x1, y1, x2, y2, led_cnt]]):
                        break
                    led_cnts[-1].append(int(led_cnt))
                    cntrl_vectors.append(pygame.math.Vector2(x1, y1))
                    cntrl_vectors.append(pygame.math.Vector2(x2, y2))
                elif len(data) == 2:
                    led_cnts.append([])
                    x, y = [int(i) for i in data]
                    poses.append(pygame.math.Vector2(x, y))
                    pass
        temp = LedSign(led_cnts)
        if port != None:
            temp.attach(port)     
        for vector in cntrl_vectors:
            temp.setup(vector)
        for pose, symbol in zip(poses, temp.symbols):
            symbol.set_position(pose)
        assert(temp.initialized == True)
        return temp

    def save(self, filename):
        with open(filename, 'w') as filehandle:
            for symbol in self.symbols:
                filehandle.write("{} {}\n".format(int(symbol.position.x),int(symbol.position.y)))
                for strip in symbol.save():
                    start, end, cnt = strip
                    filehandle.write("{} {} {} {} {}\n".format(
                        int(start.x), int(start.y), int(end.x), int(end.y), cnt))

    def attach(self, serial_port):
        try:
            if serial_port == None:
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    print(p)
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
        self.ser.write(bytearray(values))
 