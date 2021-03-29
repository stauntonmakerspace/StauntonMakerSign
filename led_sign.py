import serial
import pygame
import pickle


class SerialMock():
    def __init__(self):
        print("WARNING: Running with mock serial. No commands will actually be sent to connected devices")

    def write(self, bytes):
        pass


class LedStrip():
    def __init__(self, led_cnt):
        self.initialized = False 
        self.start_set = False
        self.led_cnt = led_cnt
        self.adjusting = False
        # Store the last record values in order to prevent sending duplicates unnecessrily
        self.last_samples = [(0, 0, 0), ] * led_cnt
        self.scale = 5

        self.start_control = pygame.math.Vector2(led_cnt, led_cnt)
        self.end_control = pygame.math.Vector2(
            led_cnt * self.scale, led_cnt * self.scale)
    
    def setup(self, vector):
        if not self.start_set:
            self.start_control = vector
            self.start_set = True
        else:
            self.set_end_control(vector)
            self.initialized = True

    def draw(self, screen):
        pygame.draw.line(screen, (255, 0, 0),
                         self.start_control, self.end_control, 6)
        pygame.draw.circle(screen, (0, 255, 255),
                           (self.start_control.x,  self.start_control.y), 4)
        pygame.draw.circle(screen, (0, 255, 255),
                           (self.end_control.x,  self.end_control.y), 4)

    def adjust_controls(self, screen, events):
        return False
        # for event in events:
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if event.button == 1:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             self.active_control = self.closest_control(point)

        #     elif event.type == pygame.MOUSEBUTTONUP:
        #         if event.button == 1:
        #             self.active_control = None

        #     elif event.type == pygame.MOUSEMOTION:
        #         if self.active_control != None:
        #             mouse_x, mouse_y = event.pos
        #             point = pygame.math.Vector2(mouse_x, mouse_y)
        #             if self.active_control[2] == 1:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].set_start_control(
        #                     point)
        #             else:
        #                 self.symbols[self.active_control[0]].strips[self.active_control[1]].set_end_control(
        #                     point)

    def update(self, screen, events):
        unit_vector = (
            (self.start_control - self.end_control).normalize() * self.scale)
        samples = []
        for i in range(self.led_cnt):
            sample_point = self.start_control - (unit_vector * i)
            # pygame.draw.circle(screen, (0,255,0), (sample_point.x, sample_point.y), 1)
            try:
                sample = screen.get_at(
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
            pass

    def save(self):
        return (int(self.start_control.x),int(self.start_control.y), int(self.end_control.x),int(self.end_control.y), self.led_cnt)

    def set_end_control(self, end_control):
        self.end_control = self.start_control - \
            ((self.start_control - end_control).normalize()
             * self.led_cnt * self.scale)

    def set_start_control(self, start_control):
        self.start_control = self.end_control - \
            ((self.end_control - start_control).normalize()
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
        for strip_num in range(len(self.strips) - 1):
            self.strips[strip_num].draw(screen)
            pygame.draw.line(
                screen, (0, 0, 255), self.strips[strip_num].end_control, self.strips[strip_num + 1].start_control, 1)
        self.strips[-1].draw(screen)
        pygame.draw.circle(screen, (255, 255, 255),
                           (self.strips[0].start_control.x - 15,  self.strips[0].start_control.y - 15), 4)

    def adjust_controls(self, screen, events):
        for strip in self.strips:
            adjusted = strip.adjust_controls(screen, events)
            if adjusted:
                break
        return False

    def update(self, screen, events):
        rgb_cmds = []
        for strip in self.strips:
            rgb_cmds += strip.update(screen, events)
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


class LedSign():
    def __init__(self, led_cnts, ser=None):
        self.symbols = []
        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
        self.ser = ser

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

    def draw(self, screen):
        for symbol in self.symbols:
            symbol.draw(screen)

    def adjust_controls(self, screen, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if not self.initialized:
                        self.setup(point)
                    else:
                        self.active_control = self.closest_control(point)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.active_control = None

            elif event.type == pygame.MOUSEMOTION:
                if self.active_control != None:
                    mouse_x, mouse_y = event.pos
                    point = pygame.math.Vector2(mouse_x, mouse_y)
                    if self.active_control[2] == 1:
                        self.symbols[self.active_control[0]].strips[self.active_control[1]].set_start_control(
                            point)
                    else:
                        self.symbols[self.active_control[0]].strips[self.active_control[1]].set_end_control(
                            point)
        return False

    def update(self, screen, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.save("sign.txt")
        if self.adjustable:
            if not self.adjust_controls(screen, events):
                for symbol in self.symbols:
                    adjusted = symbol.adjust_controls(screen, events)
                    if adjusted:
                        break
        for i in range(len(self.symbols) - 1, -1, -1):
            cmds = self.symbols[i].update(screen, events)
            led_num = 0
            changed = False
            for cmd in cmds:
                if cmd[0] != -1:
                    changed = True
                    self.send_cmd(i, led_num, cmd[0], cmd[1], cmd[2])
                led_num += 1
            if changed:
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
                    led_cnts[-1].append(int(led_cnt))
                    cntrl_vectors.append(pygame.math.Vector2(int(x1), int(y1)))
                    cntrl_vectors.append(pygame.math.Vector2(int(x2), int(y2)))
        temp = LedSign(led_cnts)
        for vector in cntrl_vectors:
            temp.setup(vector)

        return temp

    def save(self, filename):
        with open(filename, 'w') as filehandle:
            for symbol in self.symbols:
                filehandle.write('#\n')
                for strip in symbol.save():
                    for cntrl in strip:
                        filehandle.write('%s ' % cntrl)
                    filehandle.write('\n')
                    
                

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

    def attach(self, ser):
        self.ser = ser

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
            print("WARNING No serial object is attached")
