import pygame as pg


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


class Input:
    def __init__(self):
        pass

    @staticmethod
    def direction(events, current_direction):
        for event in events:
            if event.type != pg.KEYDOWN:
                continue
            if event.key == pg.K_UP:
                if current_direction != (0, 1):
                    current_direction = (0, -1)
                    break
            elif event.key == pg.K_DOWN:
                if current_direction != (0, -1):
                    current_direction = (0, 1)
                    break
            elif event.key == pg.K_LEFT:
                if current_direction != (1, 0) and current_direction != (0, 0):
                    current_direction = (-1, 0)
                    break
            elif event.key == pg.K_RIGHT:
                if current_direction != (-1, 0):
                    current_direction = (1, 0)
                    break
        return current_direction

    @staticmethod
    def any_key(events):
        for event in events:
            if event.type == pg.KEYDOWN:
                return True
        return False

    @staticmethod
    def quit(events):
        for event in events:
            if event.type == pg.QUIT:
                return True
        return False

    @staticmethod
    def escape(events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True


class Highscore:
    def __init__(self):
        pass

    @staticmethod
    def retrieve_hs():
        try:
            with open('highscore.pickle', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    @staticmethod
    def save_hs(hs):
        with open('highscore.pickle', 'w') as file:
            file.write(str(hs))

    @staticmethod
    def reset_hs():
        with open('highscore.pickle', 'w') as file:
            file.write('0')