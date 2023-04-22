"""
Main Driving File For Astro Wars
Author: Vaibhav Shrivathsa
"""
from GameInfo import *

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
        elif game.game_phase == GamePhase.GAME_ENDED:
            Gameplay.game_ended_phase(game)

        # dt = game.clock.get_time() / 1000
        # fps = UITools.Text(str("{:.0f}".format(1 / dt)),
        # UI.WHITE, Vector2(0.07, 0.07), 0.04)
        # fps.render(game)

        pygame.display.flip()


if __name__ == '__main__':
    main()
