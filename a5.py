"""
Name: Vaibhav Shrivathsa
UTEID: vrs782

On my honor, Vaibhav Shrivathsa, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

1. What is the purpose of your program?

    My program is a two-player game in which 
    each player has two controls: turn and shoot.
    Players control ships and must destroy the other 
    player's ship by shooting them to win. 
    Many matches can be played, and matches can be paused.
    
    As mentioned in the instructions menu:
    Player 1 turns and shoots with A and D
    Player 2 turns and shoots with the left and right arrow keys
 
2. List the major features of your program:
    Astro-Party Like Gameplay
    Matches Can Be Paused
    Physics For Collision Detection and Acceleration Implemented
    Dynamic Camera System that follows Players and Performs Screen Shake
        when objects are destroyed
    Main Menu With Clickable Buttons

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)
    
pygame is the only 3rd party module that needs to be installed.
    
4. List the things your learned while doing this program. Python features, 
techniques, third party modules, etc. 

I learned alot about the math library 
pygame offers, and about pygame itself. This project also gave me a lot of 
experience working with classes in Python. I also learned a little bit about 
basic collision detection by implementing it.

5. What was the most difficult thing you had to overcome or learn to get 
this program to work? 

It was a bit of a struggle to structure my code, 
since I haven't coded a game so ground-up before. The game is essentially 
like multiple programs stitched together (the menus vs gameplay), 
so I learned how to manage building programs like this with a state machine. 
The main method in a5 selects between different functions based on the 
current "phase" of the program. After appropriately splitting my code up 
into different files and implementing the state machine, it became much 
easier to work on developing the program.
   
6. What features would you add next? 

I would improve the graphics with maybe 
stars in the background with parallax and better sprites. More stages and 
powerups would be good additions.
"""""
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
