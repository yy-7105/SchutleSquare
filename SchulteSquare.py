import pygame
from pygame.locals import (MOUSEBUTTONUP,
                           MOUSEBUTTONDOWN,
                           KEYDOWN,
                           K_r,
                           QUIT)
import random


def init_board(size):
    assert isinstance(size, int) and 4 <= size <= 9

    lst = []
    for i in range(1, size ** 2 + 1):
        lst.append(i)
    random.shuffle(lst)

    lst2d = []
    while lst:
        temp = []
        for i in range(size):
            temp.append(lst.pop())
        lst2d.append(temp)

    return lst2d


pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)
dark_grey = (43, 45, 47)
light_grey = (80, 80, 80)
WIDTH = 724
margin = 4
title_height = 80
HEIGHT = WIDTH + title_height
screen = pygame.display.set_mode([WIDTH, HEIGHT])
screen.fill(dark_grey)
font = pygame.font.SysFont('calibri', 35)

size_to_font_size = {
    4: 50,
    5: 42,
    6: 39,
    7: 34,
    8: 30,
    9: 28
}


def gen_text_window(text, font_size, centered_pos, font_color, bg_color):
    font = pygame.font.SysFont('calibri', font_size)
    text = font.render(text, True, font_color, bg_color)
    textrect = text.get_rect()
    textrect.center = centered_pos
    screen.blit(text, textrect)


def render_board(lst, size):
    block_size = int(round((WIDTH - margin) / size))
    block_size_no_margin = block_size - margin
    for y in range(size):
        for x in range(size):
            pygame.draw.rect(screen, black,
                             pygame.Rect(margin + block_size * x,
                                         title_height + margin + block_size * y,
                                         block_size_no_margin,
                                         block_size_no_margin))

            center = (margin + block_size * x + block_size_no_margin // 2,
                      title_height + margin + block_size * y + block_size_no_margin // 2)
            gen_text_window(str(lst[y][x]), size_to_font_size[size],
                            center, white, black)


width = 400
left = int(round((WIDTH - width) // 2))
height = 60


def select_modes():
    pygame.draw.rect(screen, black, pygame.Rect(left, 100, width, height))
    gen_text_window('4 x 4', 28, (WIDTH // 2, 100 + height // 2), white, black)

    pygame.draw.rect(screen, black, pygame.Rect(left, 200, width, height))
    gen_text_window('5 x 5', 28, (WIDTH // 2, 200 + height // 2), white, black)

    pygame.draw.rect(screen, black, pygame.Rect(left, 300, width, height))
    gen_text_window('6 x 6', 28, (WIDTH // 2, 300 + height // 2), white, black)

    pygame.draw.rect(screen, black, pygame.Rect(left, 400, width, height))
    gen_text_window('7 x 7', 28, (WIDTH // 2, 400 + height // 2), white, black)

    pygame.draw.rect(screen, black, pygame.Rect(left, 500, width, height))
    gen_text_window('8 x 8', 28, (WIDTH // 2, 500 + height // 2), white, black)

    pygame.draw.rect(screen, black, pygame.Rect(left, 600, width, height))
    gen_text_window('9 x 9', 28, (WIDTH // 2, 600 + height // 2), white, black)


def get_mode(pos):
    x, y = pos[0], pos[1]
    if x < left or x > left + width:
        return None
    elif 100 <= y <= 100 + height:
        return 4
    elif 200 <= y <= 200 + height:
        return 5
    elif 300 <= y <= 300 + height:
        return 6
    elif 400 <= y <= 400 + height:
        return 7
    elif 500 <= y <= 500 + height:
        return 8
    elif 600 <= y <= 600 + height:
        return 9


def get_block(pos, size, curr, lst):
    x, y = pos[0], pos[1] - 60
    if y < height:
        return None
    block_size = int(round((WIDTH - margin) / size))
    block_size_no_margin = block_size - margin
    i, j = y // block_size, x // block_size
    print(i, j)

    if lst[i][j] == curr:
        center = (margin + block_size * j + block_size_no_margin // 2,
                  title_height + margin + block_size * i + block_size_no_margin // 2)
        gen_text_window(str(lst[i][j]), size_to_font_size[size],
                        center, light_grey, black)
        curr += 1

    return curr


running = True
size_decided = False
rendered = False
size = None
curr = None
lst = []
time_when_finished = None
t1 = 0

while running:
    while not size_decided:
        screen.fill(dark_grey)
        select_modes()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                size_get = get_mode(pos)
                if size_get:
                    size = size_get
                    size_decided = True
                    curr = 1
            elif event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    if not rendered:
        screen.fill(dark_grey)
        lst = init_board(size)
        print(lst)
        render_board(lst, size)
        rendered = True
        t1 = pygame.time.get_ticks()/1000

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            temp = get_block(pos, size, curr, lst)
            print(temp)
            if temp:
                curr = temp
                gen_text_window(f'current:', 25, (660, 25), white, dark_grey)
                gen_text_window(str(curr - 1), 25, (660, 50), white, dark_grey)
            if curr > size ** 2:
                time_when_finished = pygame.time.get_ticks()/1000 - t1
                center = (WIDTH // 2, HEIGHT // 2)
                gen_text_window('Finished!', 40, center, black, white)
        elif event.type == KEYDOWN:
            if event.key == K_r:
                print('reset')
                size_decided = False
                rendered = False
                size = None
                curr = None
                lst = []
                time_when_finished = None
                t1 = 0
        elif event.type == pygame.QUIT:
            pygame.quit()

    if time_when_finished:
        time_string = 'Timer: {:.3f}'.format(time_when_finished)
    else:
        time_string = 'Timer: {:.3f}'.format(pygame.time.get_ticks()/1000 - t1)

    gen_text_window(time_string, 32, (WIDTH // 2, title_height // 2),
                    white, dark_grey)
    gen_text_window('Press R to reset', 20, (80, 25), white, dark_grey)

    pygame.display.update()

pygame.quit()
