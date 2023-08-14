
import pygame
from makersign import LedSign
import ClearSign

pygame.display.set_caption('Quick Start')
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_size = screen.get_size()
screen.fill("blue")
screen.fill("black")

window_width = screen.get_width()
window_height = screen.get_height()
print(window_width)
print(window_height)
keys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u,
        pygame.K_i, pygame.K_o, pygame.K_p, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
        pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_z, pygame.K_x,
        pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_PERIOD, pygame.K_QUESTION,
        pygame.K_EXCLAIM, pygame.K_SPACE]
lines = []
correct = ""
LetterList = ""
lives = 10
deathColor = "red"
sStart = False
x = 10
x1 = 10
y = 160
d = True
fc = "red"

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")


def set_word():
    global LetterList
    string = ""
    pygame.font.init()
    done = False
    while not done:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                for i in keys:
                    if ev.key == i:
                        string += str(ev.unicode)
                if ev.key == pygame.K_ESCAPE:
                    done = True
    for i in string:
        if i not in LetterList:
            LetterList += i
    return string


def draw_word(w):
    for i in range(len(w)):
        if i < 14:
            x = (window_width / len(w) + (100 * i))
            y = window_height - 200
        elif i >= 14:
            x = (window_width / len(w) + (100 * (i - 14)))
            y = window_height - 100

        if w[i] != " ":
            line = pygame.draw.line(screen, "white", (x, y), ((x + 50), y))
            line.y = y
            lines.append(line)
        elif w[i] == " ":
            line = pygame.draw.line(screen, "black", (x, y), ((x + 50), y))
            line.y = y
            lines.append(line)


def read_guesses():
    global lives
    global correct
    guess_list = ""
    while lives != 0:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key in keys:
                    guess_list += str(ev.unicode)
                    gc = guess_correct(ev.unicode)
                    if gc != False:
                        for line in range(len(lines)):
                            for s in range(len(word)):
                                if (line == s and word[s] == ev.unicode):
                                    font = pygame.font.SysFont("arial", size=50)
                                    text = font.render("{}".format(word[s]), True, "RED")
                                    screen.blit(text, (lines[line].centerx, lines[line].y - 50))
                    elif not gc:
                        lives -= 1
            return str(guess_list)


def guess_correct(guess):
    global correct
    if guess in word:
        correct += str(guess)
    else:
        return False


def check_win():
    global LetterList
    global correct
    if len(LetterList) == len(correct):
        return True
    else:
        return False


running = True
word_set = False
a = 0
clock = pygame.time.Clock()
clearCount = 1
while running:
    ClearSign.clearScreen(clearCount)
    clearCount = 0
    clock.tick(60)
    a += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not word_set:
        word = set_word()
        if len(word) > 28:
            word = set_word()
        draw_word(word)
        word_set = True
    elif word_set:
        if check_win():
            for i in range(40):
                if a % 5 == 0:
                    pygame.draw.rect(screen, "blue", rect=(x, 160, 30, 200))
                    pygame.draw.rect(screen, "hotPink", rect=(40, y, 1350, 30))
                    pygame.draw.rect(screen, "purple", rect=(x, y, 80, 80))
                    if d:
                        pygame.draw.rect(screen, "black", rect=(x - 20, 160, 10, 200))
                        pygame.draw.rect(screen, "black", rect=(40, y - 20, 1350, 10))
                        pygame.draw.rect(screen, "black", rect=(x - 20, y - 20, 10, 10))
                        x += 1
                        if a % 30 == 0:
                            y += 1
                    elif not d:
                        pygame.draw.rect(screen, "black", rect=(x + 35, 160, 10, 200))
                        pygame.draw.rect(screen, "black", rect=(40, y + 30, 1350, 10))
                        pygame.draw.rect(screen, "black", rect=(x + 60, y + 5, 84, 84))
                        x -= 1
                        if a % 30 == 0:
                            y -= 1
                    if x > 1350:
                        d = False
                        x = 1350
                    elif x < 15:
                        d = True
                        x = 15

        else:
            guesses = read_guesses()
            deathBar = pygame.draw.rect(screen, color=fc, rect=(40, 160, 1350 - (135 * lives), 200))
    if lives == 0:
        for line in range(len(lines)):
            for s in range(len(word)):
                if line == s:
                    font = pygame.font.SysFont("arial", size=50)
                    text = font.render("{}".format(word[s]), True, "RED")
                    screen.blit(text, (lines[line].centerx, lines[line].y - 50))

        font = pygame.font.SysFont("arial", size=50)
        text = font.render("{}".format(f"You ran out of lives!"), True, "RED")
        screen.blit(text, (1536/3, 960/2))
    sign.sample_surface(screen)
    sign.draw(screen)

    pygame.display.flip()
