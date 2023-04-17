import pygame
from pygame.math import Vector2

import UITools
from UITools import UI

class GameInfo:
    def __init__(self):
        self.screen = pygame.display.set_mode(UI.WINDOW_SIZE)
        pygame.display.set_caption("Astro Wars")
        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.INTRO_MENU

class GamePhase:
    INTRO_MENU = 0
    IN_MATCH = 1
    GAME_EXITED = 2
    CREDITS_MENU = 3
    INFO_MENU = 4
