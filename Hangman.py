
import pygame
from makersign import LedSign
import ClearSign
import random
import balls
import os

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
deathColor = "red"
fc = "red"
word_set = False
lives = 10
won = False
lost = False
word = ""

sign = LedSign.load("sign.txt")
sign.attach("/dev/ttyUSB0")


def set_word():
    global LetterList
    string = ""
    clock = pygame.time.Clock()
    pygame.font.init()
    done = False
    letterCount = 0
    x = 200
    y = 600
    idleClock = 0
    idle = False
    while not done and not idle:
        idleClock += 1
        print(idleClock)
        clock.tick(60)
        screen.fill("black")
        font = pygame.font.SysFont("arial", size=40)
        text = font.render("{}".format("Enter a word or phrase for someone to guess!"), True, "Blue")
        screen.blit(text, (200, 450))
        text = font.render("{}".format("No capital letters.  Press esc to confirm your entry"), True, "Blue")
        screen.blit(text, (200, 550))
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                idleClock = 0
                for i in keys:
                    if ev.key == i:
                        string += str(ev.unicode)
                        letterCount += 1
                if ev.key == pygame.K_ESCAPE:
                    if len(string) > 28:
                        string = ""
                        set_word()
                    else:
                        done = True
                if ev.key == pygame.K_BACKSPACE:
                    string = string[0:len(string)-1]
                    letterCount -= 1
        font = pygame.font.SysFont("arial", size=40)
        text = font.render("{}".format(string), True, "Purple")
        screen.blit(text, (x, y))
        if done:
            for i in string:
                if i not in LetterList:
                    LetterList += i
        sign.sample_surface(screen)
        sign.draw(screen)
        pygame.display.flip()
        if idleClock > 60:
            idle = True
            return("")
    return string


def draw_word(w):
    global lines
    for i in range(len(w)):
        if i < 14:
            x = (window_width / len(w) + (150 * i))
            y = window_height - 200
        elif i >= 14:
            x = (window_width / len(w) + (150 * (i - 14)))
            y = window_height - 80

        if w[i] != " ":
            color = "white"
        elif w[i] == " ":
            color = "black"

        line = pygame.draw.line(screen, color, (x, y), ((x + 100), y))
        line.y = y
        lines.append(line)


def read_guesses(word):
    global lives
    global won
    global lost
    global lines
    guess_list = ""
    hidden = False
    clock = pygame.time.Clock()
    while lives != 0 and won is False:
        if not hidden:
            pygame.draw.rect(screen, color = "black", rect=(100,270,900,350))
            hidden = True
        clock.tick(60)
        screen.fill("black")
        draw_word(word)
        pygame.draw.rect(screen, color=fc, rect=(40, 160, 1350 - (135 * lives), 200))
        font = pygame.font.SysFont("arial", size=40)
        text = font.render("{}".format("Someone entered a word for you!"), True, "Blue")
        screen.blit(text, (200, 450))
        text = font.render("{}".format("Guess a letter!"), True, "Blue")
        screen.blit(text, (200, 550))
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key in keys:
                    if ev.unicode not in guess_list:
                        guess_list += str(ev.unicode)
                        guess_correct(ev.unicode)
        for line in range(len(lines)):
            for s in range(len(word)):
                if line == s:
                    if word[s] in correct:
                        font = pygame.font.SysFont("arial", size=100)
                        text = font.render("{}".format(word[s]), True, "Red")
                        screen.blit(text, (lines[line].centerx - 30, lines[line].y - 130))
        if check_win():
            won = True
        if lives == 0:
            lost = True
        sign.sample_surface(screen)
        sign.draw(screen)
        pygame.display.flip()


def word_search(word):
    read_guesses(word)


def guess_correct(guess):
    global correct
    global lives
    if guess in word:
        correct += str(guess)
    else:
        lives -= 1
        return False


def check_win():
    global LetterList
    global correct
    if len(LetterList) == len(correct):
        return True
    else:
        return False


def loss(word):
    runs = True
    clock = pygame.time.Clock()
    p = 0
    while runs:
        clock.tick(60)
        p += 1
        screen.fill("black")
        pygame.draw.rect(screen, color="black",rect=(200,500,1800,350))
        pygame.draw.rect(screen, color=fc, rect=(40, 160, 1350 - (135 * lives), 200))
        for line in range(len(lines)):
            for s in range(len(word)):
                if line == s:
                    font = pygame.font.SysFont("arial", size=100)
                    text = font.render("{}".format(word[s]), True, "Red")
                    screen.blit(text, (lines[line].centerx-30, lines[line].y - 150))
        draw_word(word)
        font = pygame.font.SysFont("arial", size=100)
        text = font.render("{}".format(f"You ran out of lives!"), True, "RED")
        screen.blit(text, (200, 960 / 2))
        sign.sample_surface(screen)
        sign.draw(screen)
        pygame.display.flip()
        if p >= 60:
            runs = False


def win(word):
    global won
    runs = True
    r = 4
    g = 7
    b = 88
    d = 5
    x = 15
    count = 0
    hidden = False
    clock = pygame.time.Clock()
    while runs:
        clock.tick(60)
        if not hidden:
            pygame.draw.rect(screen, color="black", rect=(150, 300, 900, 350))
            hidden = True
        if x > 1350:
            d = -abs(d)
            x = 1350
            count += 1
        elif x < 10:
            d = abs(d)
            x = 10
            count += 1
        x += d
        rect1 = (x, 160, 30, 200)
        rect2 = (x+100, 160, 30, 200)
        screen.fill("black")
        pygame.draw.rect(screen, pygame.Color(r, g, b), rect1)
        pygame.draw.rect(screen, pygame.Color(r, g, b), rect2)
        if x % 20 == 0:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
        for line in range(len(lines)):
            for s in range(len(word)):
                if line == s:
                    draw_word(word)
                    font = pygame.font.SysFont("arial", size=100)
                    text = font.render("{}".format(word[s]), True, "Blue")
                    screen.blit(text, (lines[line].centerx - 30, lines[line].y - 150))
        font = pygame.font.SysFont("arial", size=100)
        text = font.render("{}".format(f"You won!"), True, "RED")
        screen.blit(text, (1536 / 2, 960 / 2))
        sign.sample_surface(screen)
        sign.draw(screen)
        pygame.display.flip()
        if count >= 4:
            runs = False
            won = False

def game():
    global won
    global lost
    global word
    global lines
    global correct
    global LetterList
    global lives
    #os.system("python ClearSign.py")
    while not word:
        word = set_word()
        if not word:
            os.system("python balls.py")
    word_search(word)
    if won:
        win(word)
        won = False
        word = ""
        lines = []
        correct = ""
        LetterList = ""
        lives = 10
    elif lost:
        loss(word)
        lost = False
        lines = []
        correct = ""
        LetterList = ""
        lives = 10
        word = ""
    game()


game()
