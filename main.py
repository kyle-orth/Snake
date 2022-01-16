"""
Basic game: Snake. Run using PyGame.
https://github.com/kyle-orth/snake.git
"""
import os
import random
import pygame as pg

os.environ['SDL_VIDEO_WINDOW_POS'] = "30, 50"
windowSize = (700, 540)
tileSize = 20
cols = windowSize[0] / tileSize - 2
rows = windowSize[1] / tileSize - 2
running = True


class Apple:
    def __init__(self, color='red'):
        self.pos = (random.randint(0, cols), random.randint(0, rows))
        self.color = color

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
        if len(self.coords) >= self.length:
            self.coords.pop(0)

    def draw(self, window):
        for pos in self.coords:
            rect = pg.Rect(pos[0]*tileSize, pos[1]*tileSize, tileSize, tileSize)
            pg.draw.rect(window, self.color, rect)


class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((windowSize[0], windowSize[1]))
        pg.display.set_caption("Snake")
        self.clock = pg.time.Clock()
        self.border = pg.Rect(tileSize, tileSize, cols*tileSize, rows*tileSize)

        self.score = 0
        self.active = True
        self.done = False
        self.snake = self.setup_snake()
        self.apple = Apple()

    @staticmethod
    def setup_snake():
        snake = Snake()
        snake.pos = (9, 8)
        snake.coords.append((9, 8))
        snake.coords.append((8, 8))
        snake.coords.append((7, 8))
        snake.coords.append((6, 8))
        return snake

    def input(self):
        events = pg.event.get()
        if Input.quit(events):
            self.done = True
        else:
            new_direction = Input.direction(events, self.snake.direction)
            if type(new_direction) == tuple:
                self.snake.direction = new_direction

    def collisions(self):
        # Apple collision
        if self.snake.pos == self.apple.pos:
            self.apple = Apple()
            self.snake.length += 1

        # Snake collision
        if self.snake.coords.count(self.snake.pos) != 1:
            print(self.snake.coords)
            print(self.snake.pos)
            self.active = False

        # Border collision
        if self.snake.pos[0] < 0 or self.snake.pos[0] > cols or self.snake.pos[1] < 0 or self.snake.pos[1] > rows:
            self.active = False

    def display(self):
        self.window.fill("black")
        self.apple.draw(self.window)
        self.snake.draw(self.window)
        pg.draw.rect(self.window, "white", self.border, 4)
        if not self.active:
            self.darken_display()

    def end_input(self):
        events = pg.event.get()
        if Input.quit(events):
            self.done = True
        elif Input.any_key(events):
            self.reset()

    def darken_display(self):
        shade = pg.Surface(windowSize)
        shade.set_alpha(160)
        self.window.blit(shade, (0, 0))

    def end_display(self):
        txt1 = Text('Score: ' + str(self.score), size=24, color="white")
        txt1.rect.center = (windowSize[0] / 2, windowSize[1] / 2 - 30)
        txt1.draw(self.window)
        txt2 = Text('(Press any key to play again)', size=18, color="white")
        txt2.rect.center = (windowSize[0] / 2, windowSize[1] / 2 + 30)
        txt2.draw(self.window)

    def update(self):
        if self.done:
            self.quit()
            return
        if self.active:
            self.input()
            self.collisions()
            self.display()
        else:
            self.end_input()
            self.end_display()

        pg.display.flip()

    def reset(self):
        self.score = 0
        self.active = True
        self.snake = self.setup_snake()
        self.apple = Apple()

    @staticmethod
    def quit():
        global running
        running = False
        pg.quit()


class Input:
    def __init__(self):
        pass

    @staticmethod
    def direction(events, current_direction):
        for event in events:
            if event.type is pg.KEYDOWN:
                if event.key == pg.K_UP:
                    if current_direction[1] != 1:
                        current_direction = (0, -1)
                        break
                elif event.key == pg.K_DOWN:
                    if current_direction[1] != -1:
                        current_direction = (0, 1)
                        break
                elif event.key == pg.K_LEFT:
                    if current_direction[0] != 1 and current_direction != (0, 0):
                        current_direction = (-1, 0)
                        break
                elif event.key == pg.K_RIGHT:
                    if current_direction[0] != -1:
                        current_direction = (1, 0)
                        break
        return current_direction

    @staticmethod
    def any_key(events):
        for event in events:
            if event.type is pg.KEYDOWN:
                return True
        return False

    @staticmethod
    def quit(events):
        for event in events:
            if event.type is pg.QUIT:
                return True
            elif event.type is pg.KEYDOWN:
                key = event.key
                if key == pg.K_ESCAPE:
                    return True
        return False


class Text:
    def __init__(self, text, font='comicsansms', size=24, color='black', bold=False, italics=False, bg_color=None):
        self.text = text
        self.font = pg.font.SysFont(font, size, bold, italics)
        self.color = color
        self.bg_color = bg_color
        self.img = None
        self.rect = None

        self.prep()

    def prep(self):
        self.img = self.font.render(self.text, True, self.color, self.bg_color)
        self.rect = self.img.get_rect()
        self.rect.topleft = (0, 0)

    def draw(self, window):
        window.blit(self.img, self.rect)


def run():
    game = Game()
    clock = pg.time.Clock()
    while running:
        clock.tick(5)
        game.update()


if __name__ == "__main__":
    run()
