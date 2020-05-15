import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class Cube(object):
    # global rows, width
    rows = 20
    width = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        global size_between
        my_row = self.pos[0]
        my_column = self.pos[1]

        pygame.draw.rect(surface, self.color, (my_row * size_between + 1, my_column * size_between + 1, size_between - 2, size_between - 2))

        if eyes:
            centre = size_between // 2
            radius = 3
            # Not sure about circle_middle_1 and 2 maths
            # Have to look at it again in the future
            circle_middle_1 = (my_row * size_between + centre - radius, my_column * size_between + 8)
            circle_middle_2 = (my_row * size_between + size_between - radius * 2, my_column * size_between + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_1, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle_2, radius)


class Snake(object):
    body = []
    turn = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            # Set direction to move in
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turn[self.head.pos[:]] = [self.dirnx, self.dirny]

        for index, cube in enumerate(self.body):
            position = cube.pos[:]

            if position in self.turn:
                turn = self.turn[position]
                cube.move(turn[0], turn[1])

                if index == len(self.body)-1:
                    self.turn.pop(position)

            else:
                # If + elif to check if we move through the edge of the screen
                # Else to just move like normal
                if cube.dirnx == -1 and cube.pos[0] <= 0:
                    cube.pos = (cube.rows - 1, cube.pos[1])
                elif cube.dirnx == 1 and cube.pos[0] >= cube.rows - 1:
                    cube.pos = (0, cube.pos[1])
                elif cube.dirny == 1 and cube.pos[1] >= cube.rows - 1:
                    cube.pos = (cube.pos[0], 0)
                elif cube.dirny == -1 and cube.pos[1] <= 0:
                    cube.pos = (cube.pos[0], cube.rows - 1)
                else:
                    cube.move(cube.dirnx, cube.dirny)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turn = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy, = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.draw(surface, True)
            else:
                cube.draw(surface)


def draw_grid(w, rows, surface):
    global size_between

    x = 0
    y = 0
    for line in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global width, rows, my_snake, snack
    surface.fill((0, 0, 0))
    my_snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, my_snake):
    current_positions = my_snake.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        if len(list(filter(lambda z: z.pos == (x, y), current_positions))) > 0:
            continue
        else:
            break

    return x, y

# Should look up tkinter docs for the following part
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, my_snake, size_between, snack
    width = 500
    rows = 20
    size_between = width // rows

    win = pygame.display.set_mode((width, width))
    my_snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, my_snake), color=(0, 255, 0))

    clock = pygame.time.Clock()

    flag = True
    while flag:
        # Not sure about this part
        # Would it not be easier to just wait x ticks?
        pygame.time.delay(50)
        clock.tick(10)

        my_snake.move()
        if my_snake.body[0].pos == snack.pos:
            my_snake.add_cube()
            snack = Cube(random_snack(rows, my_snake), color=(0, 255, 0))

        for x in range(len(my_snake.body)):
            if my_snake.body[x].pos in list(map(lambda z:z.pos, my_snake.body[x+1:])):
                print("Score: ", len(my_snake.body))
                message_box("You Lost!", "Play again...")
                my_snake.reset((10, 10))
                break

        redraw_window(win)


main()
