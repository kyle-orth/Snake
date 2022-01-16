"""
Basic game: Snake. Run using PyGame.
https://github.com/kyle-orth/snake.git
"""
import random
import pygame as pg
from resources import Text, Input

windowSize = (540, 540)
tileSize = 30
cols = windowSize[0] / tileSize - 2
rows = windowSize[1] / tileSize - 2
running = True
speed = 6


class Apple:
    def __init__(self, snake_coords, color='red'):
        self.color = color
        self.pos = (random.randint(1, cols), random.randint(1, rows))
        while self.pos in snake_coords:
            self.pos = (random.randint(1, cols), random.randint(1, rows))

    def draw(self, window):
        rect = pg.Rect(self.pos[0]*tileSize, self.pos[1]*tileSize, tileSize, tileSize)
        pg.draw.rect(window, self.color, rect)


class Snake:
    def __init__(self, color='green'):
        self.color = color
        self.pos = (0, 0)
        self.direction = (0, 0)
        self.coords = []
        self.length = 4

    def move(self):
        if self.direction == (0, 0):
            return
        new_pos = (self.pos[0] + self.direction[0], self.pos[1] + self.direction[1])
        self.pos = new_pos
        self.coords.append(self.pos)
        if len(self.coords) > self.length:
            self.coords.pop(0)

    def draw(self, window):
        for pos in self.coords:
            rect = pg.Rect(pos[0]*tileSize, pos[1]*tileSize, tileSize, tileSize)
            pg.draw.rect(window, self.color, rect)


class Game:
    def __init__(self, pygame_window):
        self.window = pygame_window
        self.border = pg.Rect(tileSize, tileSize, cols*tileSize, rows*tileSize)
        self.done = False

        self.score = 0
        self.active = True
        self.endscreen_timer = int(speed*2)
        self.snake = self.setup_snake()
        self.apple = Apple(self.snake.coords)

    def update(self):
        if self.done:
            return
        if self.active:
            self.input()
            self.snake.move()
            self.collisions()
            self.score = self.snake.length - 4
        else:
            self.end_input()

    def draw(self):
        if self.done:
            return
        if self.active:
            self.display()
        else:
            self.end_display()
        pg.display.flip()

    def reset(self):
        self.score = 0
        self.active = True
        self.endscreen_timer = int(speed*2)
        self.snake = self.setup_snake()
        self.apple = Apple(self.snake.coords)

    @staticmethod
    def quit():
        global running
        running = False
        pg.quit()

    @staticmethod
    def setup_snake():
        snake = Snake()
        snake.pos = (9, 8)
        snake.coords.append((6, 8))
        snake.coords.append((7, 8))
        snake.coords.append((8, 8))
        snake.coords.append((9, 8))
        return snake

    def input(self):
        events = pg.event.get()
        if Input.quit(events) or Input.escape(events):
            self.done = True
            pg.quit()
        else:
            new_direction = Input.direction(events, self.snake.direction)
            self.snake.direction = new_direction

    def collisions(self):
        # Apple collision
        if self.snake.pos == self.apple.pos:
            self.apple = Apple(self.snake.coords)
            self.snake.length += 1

        # Snake collision
        if self.snake.coords.count(self.snake.pos) != 1:
            self.active = False

        # Border collision
        if self.snake.pos[0] < 1 or self.snake.pos[0] > cols or self.snake.pos[1] < 1 or self.snake.pos[1] > rows:
            self.active = False

    def end_input(self):
        events = pg.event.get()
        if Input.quit(events) or Input.escape(events):
            self.done = True
            pg.quit()
        elif Input.any_key(events):
            if self.endscreen_timer == 0:
                self.reset()

    def display(self):
        self.window.fill("black")
        self.apple.draw(self.window)
        self.snake.draw(self.window)
        pg.draw.rect(self.window, "white", self.border, 4)

        score = Text(str(self.score), color="white")
        score.rect.center = (windowSize[0] / 2, int(tileSize * 1.75))
        score.draw(self.window)

        # On the last frame of the active game, darken display
        if not self.active:
            shade = pg.Surface(windowSize)
            shade.set_alpha(160)
            self.window.blit(shade, (0, 0))

    def end_display(self):
        score = Text('Score: ' + str(self.score), size=24, color="white")
        score.rect.center = (windowSize[0] / 2, windowSize[1] / 2 - 30)
        score.draw(self.window)
        if self.endscreen_timer == 0:
            play_again = Text('(Press any key to play again)', size=18, color="white")
            play_again.rect.center = (windowSize[0] / 2, windowSize[1] / 2 + 30)
            play_again.draw(self.window)
        else:
            self.endscreen_timer -= 1


def run():
    pg.init()
    window = pg.display.set_mode((windowSize[0], windowSize[1]))
    pg.display.set_caption("Snake")
    game = Game(window)
    clock = pg.time.Clock()
    while not game.done:
        clock.tick(speed)
        game.update()
        game.draw()


if __name__ == "__main__":
    run()
