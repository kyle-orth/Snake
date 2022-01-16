"""
Basic game: Snake. Run using PyGame.
"""
import os
import random
import pygame as pg

os.environ['SDL_VIDEO_WINDOW_POS'] = "30, 50"
windowSize = (700, 540)
tileSize = 20
cols = windowSize[0] / tileSize - 2
rows = windowSize[1] / tileSize - 2


class Apple:
    def __init__(self, color='red'):
        self.pos = (random.randint(0, cols), random.randint(0, rows))
        self.color = color

    def draw(self, window):
        rect = pg.Rect(self.pos[0], self.pos[1], tileSize, tileSize)
        pg.draw.rect(window, self.color, rect)


class Snake:
    def __init__(self, color='green'):
        self.color = color
        self.pos = (0, 0)
        self.direction = (0, 1)
        self.coords = []
        self.length = 4

    def move(self):
        new_pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        self.pos = new_pos
        self.coords.append(self.pos)
        if len(self.coords) >= self.length:
            self.coords.pop(0)

    def draw(self, window):
        for pos in self.coords:
            rect = pg.Rect(pos[0], pos[1], tileSize, tileSize)
            pg.draw.rect(window, self.color, rect)


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode(windowSize[0], windowSize[1])
        pg.display.set_caption("Snake")

        self.score = 0

        self.snake = self.setup_snake()
        self.apple = Apple()
        self.border = pg.Rect(tileSize, tileSize, cols*tileSize, rows*tileSize)

    @staticmethod
    def setup_snake():
        snake = Snake()
        snake.pos = (9, 8)
        snake.coords.append([9, 8])
        snake.coords.append([8, 8])
        snake.coords.append([7, 8])
        snake.coords.append([6, 8])
        return snake

    def apple_collision(self):
        if self.snake.pos == self.apple.pos:
            self.apple = Apple()
            self.snake.length += 1

    def snake_collision(self):
        layers = self.snake.coords.count(self.snake.pos)
        if layers != 1:
            self.end()

    def border_collision(self):
        if self.snake.pos[0] < 0 or self.snake.pos[0] > cols or self.snake.pos[1] < 0 or self.snake.pos[1] > rows:
            self.end()

    def end(self):
        pass
