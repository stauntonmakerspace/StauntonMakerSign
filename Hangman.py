
import pygame
from makersign import LedSign
import ClearSign

pygame.display.set_caption('Quick Start')
pygame.font.init()
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
word_set = False

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
        if i < 20:
            x = (window_width / len(w) + (150 * i))
            y = window_height - 200
        elif i >= 20:
            x = (window_width / len(w) + (150 * (i - 20)))
            y = window_height - 80

        if w[i] != " ":
            color = "white"
        elif w[i] == " ":
            color = "black"

        line = pygame.draw.line(screen, color, (x, y), ((x + 100), y))
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
                                if line == s and word[s] == ev.unicode:
                                    font = pygame.font.SysFont("arial", size=150)
                                    text = font.render("{}".format(word[s]), True, "Purple")
                                    screen.blit(text, (lines[line].centerx-30, lines[line].y - 150))
                    elif not gc:
                        lives -= 1
            return str(guess_list)

def word_search():
    global guesses
    guesses = read_guesses()
    pygame.draw.rect(screen, color=fc, rect=(40, 160, 1350 - (135 * lives), 200))


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


def loss():
    for line in range(len(lines)):
        for s in range(len(word)):
            if line == s:
                font = pygame.font.SysFont("arial", size=100)
                text = font.render("{}".format(word[s]), True, "Blue")
                screen.blit(text, (lines[line].centerx-30, lines[line].y - 150))

                font = pygame.font.SysFont("arial", size=100)
                text = font.render("{}".format(f"You ran out of lives!"), True, "RED")
                screen.blit(text, (1536 / 2, 960 / 2))


def win():
    global d
    global x
    global y
    global a
    ClearSign
    '''
    pygame.draw.rect(screen, "blue", rect=(x, 160, 30, 200))
    pygame.draw.rect(screen, "hotPink", rect=(40, y, 1350, 30))
    if d:
        pygame.draw.rect(screen, "black", rect=(x - 20, 160, 10, 200))
        pygame.draw.rect(screen, "black", rect=(40, y - 20, 1350, 10))
        x += 10
        if a % 30 == 0:
            y += 10
    elif not d:
        pygame.draw.rect(screen, "black", rect=(x + 35, 160, 10, 200))
        pygame.draw.rect(screen, "black", rect=(40, y + 30, 1350, 10))
        x -= 10
        if a % 30 == 0:
            y -= 10
    if x > 1350:
        d = False
        x = 1350
    elif x < 15:
        d = True
        x = 15
'''
running = True
a = 0
clock = pygame.time.Clock()
clearCount = 1
while running:
    if clearCount == 1:
        ClearSign
        clearCount = 0
    clock.tick(60)
    a += 1
    sign.sample_surface(screen)
    sign.draw(screen)
    if not word_set:
        word = set_word()
        if len(word) > 40:
            word = set_word()
        draw_word(word)
        word_set = True
        font = pygame.font.SysFont("arial", size=100)
        text = font.render("{}".format("Someone set a word for you! Guess a letter!"), True, "Blue")
        screen.blit(text, (300, 500))
        text = font.render("{}".format("If you see any blanks, press space."), True, "Blue")
        screen.blit(text, (300, 650))
    else:
        if check_win():
            win()
        else:
            word_search()
    if lives == 0:
        loss()


    pygame.display.flip()
