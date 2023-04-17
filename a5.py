"""
Name: Vaibhav Shrivathsa
UTEID: vrs782
replace <NAME> with your name and delete this line.

On my honor, Vaibhav Shrivathsa, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

1. What is the purpose of your program?
 
2. List the major features of your program:

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)

4. List the things your learned while doing this program. Python features,
   techniques, third party modules, etc.

5. What was the most difficult thing you had to overcome or learn
   to get this program to work?
   
6. What features would you add next?

"""""
import math

import pygame
from pygame.math import Vector2

from GameInfo import *
import UITools
from UITools import UI

import Menus
import Gameplay

pygame.init()

def main():
    game = GameInfo()
    while game.game_phase != GamePhase.GAME_EXITED:
        game.clock.tick(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_phase = GamePhase.GAME_EXITED

        if game.game_phase == GamePhase.INTRO_MENU:
            Gameplay.game_match_phase.match_started = False
            Menus.intro_menu_phase(game)
        elif game.game_phase == GamePhase.CREDITS_MENU:
            Menus.credit_menu_phase(game)
        elif game.game_phase == GamePhase.INFO_MENU:
            Menus.info_menu_phase(game)
        elif game.game_phase == GamePhase.IN_MATCH:
            Gameplay.game_match_phase(game)
        elif game.game_phase == GamePhase.GAME_PAUSED:
            Gameplay.game_paused_phase(game)

        # dt = game.clock.get_time() / 1000
        # fps = UITools.Text(str("{:.0f}".format(1 / dt)), UI.WHITE, Vector2(0.07, 0.07), 0.04)
        # fps.render(game)

        pygame.display.flip()


if __name__ == '__main__':
    main()
