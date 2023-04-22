import pygame
from pygame.math import Vector2


class UI:
    """
    Class that Contains Many Constants for UI Related Features
    """
    WINDOW_SIZE = Vector2(700, 700)
    WINDOW_CENTER = WINDOW_SIZE / 2
    WINDOW_MIN_COORD_SIZE = min(WINDOW_SIZE[0], WINDOW_SIZE[1])
    pygame.font.init()
    TEXT_FONT = pygame.font.SysFont('Lucida Console', 100)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)


class Text:
    """
    Class that Represents Displayable Text
    """

    def __init__(self, text, color, pos, size):
        """
        Initializes the Text Label
        :param text: Text to display
        :param color: Color of the Text
        :param pos: Position of the label in screen space coordinates
        (percentage of the screen to the left, percentage of the screen down)
        :param size: Size of the label in screen space coordinates
        """
        self.surface = UI.TEXT_FONT.render(text, False, color)
        text_width = self.surface.get_size()[0]

        new_text_size = Vector2(self.surface.get_size()) * (UI.WINDOW_SIZE[0] * size) / text_width
        self.surface = pygame.transform.scale(self.surface, new_text_size)

        pos = pos.elementwise() * UI.WINDOW_SIZE
        new_text_size = Vector2(self.surface.get_size())
        self.surface_top_left = pos - new_text_size / 2

    def render(self, game):
        game.screen.blit(self.surface, self.surface_top_left)


class Button:
    """
    Class That Represents a Clickable Button That Changes Color When
    Hovered Over
    """
    OUTER_BOX_SCALE = 3 / 2
    OUTER_BOX_THICKNESS = 2

    def __init__(self, text, color, hover_color, pos, size, phase_on_press):
        """
        Initializes a clickable button
        :param text: The text that the button has on it
        :param color: The color of the button when not hovered over
        :param hover_color: The color of the button when hovered over
        :param pos: The position of the button in screen space coordinates
        :param size: The size of the button in screen space coordinates
        :param phase_on_press: The phase that the program changes to
        when the button is pressed
        """
        self.color = color
        self.text = Text(text, color, pos, size / Button.OUTER_BOX_SCALE)
        self.hover_text = Text(text, hover_color, pos,
                               size / Button.OUTER_BOX_SCALE)

        pos = pos.elementwise() * UI.WINDOW_SIZE
        text_size = Vector2(self.text.surface.get_size())

        outer_box_size = text_size * Button.OUTER_BOX_SCALE
        outer_box_top_left = pos - outer_box_size / 2
        self.outer_box = pygame.Rect(outer_box_top_left, outer_box_size)

        self.phase_on_press = phase_on_press
        self.hovered_and_no_press = False

    def render(self, game):
        if self.outer_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(game.screen, self.color, self.outer_box)
            self.hover_text.render(game)
            if pygame.mouse.get_pressed()[0]:
                if self.hovered_and_no_press:
                    game.game_phase = self.phase_on_press
            else:
                self.hovered_and_no_press = True
        else:
            self.hovered_and_no_press = False
            pygame.draw.rect(game.screen, self.color,
                             self.outer_box, Button.OUTER_BOX_THICKNESS)
            self.text.render(game)
