import pygame
from pygame.math import Vector2


class UI:
    WINDOW_SIZE = Vector2(700, 700)
    WINDOW_CENTER = WINDOW_SIZE / 2
    WINDOW_MIN_COORD_SIZE = min(WINDOW_SIZE[0], WINDOW_SIZE[1])
    pygame.font.init()
    TEXT_FONT = pygame.font.SysFont('Lucida Console', 100)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Text:
    def __init__(self, text, color, pos, size):
        self.surface = UI.TEXT_FONT.render(text, False, color)
        text_width = self.surface.get_size()[0]

        new_text_size = Vector2(self.surface.get_size()) * \
                            (UI.WINDOW_SIZE[0] * size) / text_width
        self.surface = pygame.transform.scale(self.surface, new_text_size)

        pos = pos.elementwise() * UI.WINDOW_SIZE
        new_text_size = Vector2(self.surface.get_size())
        self.surface_top_left = pos - new_text_size / 2

    def render(self, game):
        game.screen.blit(self.surface, self.surface_top_left)


class Button:
    OUTER_BOX_SCALE = 3 / 2
    OUTER_BOX_THICKNESS = 2

    def __init__(self, text, color, hover_color, pos, size, phase_on_press):
        self.color = color
        self.text = Text(text, color, pos, size / Button.OUTER_BOX_SCALE)
        self.hover_text = Text(text, hover_color, pos, size / Button.OUTER_BOX_SCALE)

        pos = pos.elementwise() * UI.WINDOW_SIZE
        text_size = Vector2(self.text.surface.get_size())

        outer_box_size = text_size * Button.OUTER_BOX_SCALE
        outer_box_top_left = pos - outer_box_size / 2
        self.outer_box = pygame.Rect(outer_box_top_left, outer_box_size)

        self.phase_on_press = phase_on_press

    def render(self, game):
        if self.outer_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(game.screen, self.color, self.outer_box)
            self.hover_text.render(game)
            if pygame.mouse.get_pressed()[0]:
                game.game_phase = self.phase_on_press
        else:
            pygame.draw.rect(game.screen, self.color, self.outer_box, Button.OUTER_BOX_THICKNESS)
            self.text.render(game)
