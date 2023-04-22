import pygame

from UITools import UI

class GameInfo:
    """
    Class for an object that holds important data for the entire game
    """
    def __init__(self):
        self.screen = pygame.display.set_mode(UI.WINDOW_SIZE)
        pygame.display.set_caption("Astro Wars")
        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.INTRO_MENU

class GamePhase:
    """
    Class of constants that represents the current functionality
    of the program
    """
    INTRO_MENU = 0
    IN_MATCH = 1
    GAME_EXITED = 2
    CREDITS_MENU = 3
    INFO_MENU = 4
    GAME_PAUSED = 5
    GAME_ENDED = 6
