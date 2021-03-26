import serial
import pygame
import pickle


class LedStrip():
    def __init__(self, led_cnt):
        self.startpoint = pygame.math.Vector2(led_cnt, led_cnt)
        self.endpoint = pygame.math.Vector2(led_cnt * 10, led_cnt * 10)
        self.initialized = False
        self.start_set = False
        self.led_cnt = led_cnt
        # Store the last record values in order to prevent sending duplicates unnecessrily
        self.last_samples = [(0, 0, 0), ] * led_cnt
        self.scale = 1

    def set_endpoint(self, endpoint):
        self.endpoint = self.startpoint - \
            ((self.startpoint - endpoint).normalize() * self.led_cnt * self.scale)

    def set_startpoint(self, startpoint):
        self.startpoint = self.endpoint - \
            ((self.endpoint - startpoint).normalize() * self.led_cnt * self.scale)

    def sample_screen(self, screen):
        unit_vector = (
            (self.startpoint - self.endpoint).normalize() * self.scale)
        samples = []
        for i in range(self.led_cnt):
            sample_point = self.startpoint - (unit_vector * i)
            # pygame.draw.circle(screen, (0,255,0), (sample_point.x, sample_point.y+1), 1)
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

    def setup(self, vector):
        if not self.start_set:
            self.startpoint = vector

            self.start_set = True
        else:
            self.set_endpoint(vector)
            self.initialized = True

    def draw(self, screen):
        pygame.draw.line(screen, (255, 0, 0),
                         self.startpoint, self.endpoint, 6)


class LedSymbol():
    def __init__(self, strip_lengths):
        self.strips = []
        for length in strip_lengths:
            self.strips.append(LedStrip(length))
        self.initialized = False

    def setup(self, vector):
        strip = next(filter(lambda x: x.initialized ==
                            False, self.strips), None)
        if strip != None:
            strip.setup(vector)
        else:
            # all([strip.initialized for strip in self.strips])
            self.initialized = True

    def update(self, screen, events):
        rgb_cmds = []
        for strip in self.strips:
            rgb_cmds += strip.sample_screen(screen)
        return rgb_cmds

    def draw(self, screen):
        for strip_num in range(len(self.strips) - 1):
            self.strips[strip_num].draw(screen)
            pygame.draw.line(
                screen, (0, 0, 255), self.strips[strip_num].endpoint, self.strips[strip_num + 1].startpoint, 1)
        self.strips[-1].draw(screen)

    # (dist: float, strip number: int, Is start point: bool)
    def closest_control(self, vector):
        closest = 10e10
        out = None
        for i, strip in enumerate(self.strips):
            d1 = strip.startpoint.distance_to(vector)
            if d1 < closest:
                closest = d1
                out = (d1, i, 1)
            d2 = strip.endpoint.distance_to(vector)
            if d2 < closest:
                closest = d2
                out = (d2, i, 0)
        return out


class LedSign():
    def __init__(self, led_cnts, ser):
        self.symbols = []
        for cnts in led_cnts:
            self.symbols.append(LedSymbol(cnts))
        self.ser = ser

        self.active_control = None
        self.initialized = False

        self.adjustable = True
        self.showing = True

    def setup(self, vector):
        symbol = next(filter(lambda x: x.initialized ==
                             False, self.symbols), None)
        if symbol != None:
            symbol.setup(vector)
        else:
            self.initialized = True

    # (symbol number: int, strip number: int, Is start point: bool)
    def closest_control(self, vector):
        closest = 10e10
        out = None
        for i, symbol in enumerate(self.symbols):
            best = symbol.closest_control(vector)
            if best != None:
                dist, strip, is_start = best
                if dist < closest and dist < 40:
                    out = (i, strip, is_start)
        return out

    def draw(self, screen):
        for symbol in self.symbols:
            symbol.draw(screen)

    def __send_cmd(self, device_num, led_num, R, G, B):
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

    def update(self, screen, events):
        if self.adjustable:
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
                            self.symbols[self.active_control[0]].strips[self.active_control[1]].set_startpoint(
                                point)
                        else:
                            self.symbols[self.active_control[0]].strips[self.active_control[1]].set_endpoint(
                                point)

        for i in range(len(self.symbols) - 1, -1, -1):
            cmds = self.symbols[i].update(screen, events)
            led_num = 0
            changed = False
            for cmd in cmds:
                if cmd[0] != -1:
                    changed = True
                    self.__send_cmd(i, led_num, cmd[0], cmd[1], cmd[2])
                led_num += 1
            if changed:
                self.__send_cmd(i, 255, 0, 0, 0)
        if self.showing:
            self.draw(screen)
