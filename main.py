import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    rows = 0
    w = 0

    def __init_(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        pass

    def move(self, dirnx, dirny):
        pass

    def draw(self, surface, eyes=False):
        pass


class Snake(object):
    def __init__(self, color, pos):
        pass

    def move(self):
        pass

    def reset(self, pos):
        pass

    def add_cube(self):
        pass

    def draw(self, surface):
        pass


def draw_grid(w, rows, surface):
    pass


def redraw_window(surface):
    pass


def random_snack(rows, items):
    pass


def message_box(subject, content):
    pass


def main():
    width = 500
    height = 500
    rows = 20

    win = pygame.display.set_mode((width, height))
    s = Snake((255, 0, 0), (10, 10))

    clock = pygame.time.Clock()

    flag = True
    while flag:
        # Not sure about this part
        # Would it not be easier to just wait x ticks?
        pygame.time.delay(50)
        clock.tick(10)

        redraw_window(win)


main()
