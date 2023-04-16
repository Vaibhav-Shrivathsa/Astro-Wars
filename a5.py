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

import UITools
from UITools import UI

pygame.init()

class GameGraphics:
    ship_image_size = Vector2(100, 100)
    BLUE_SHIP_SURFACE = pygame.image.load("blue-ship.png")

class GameInfo:
    def __init__(self):
        self.screen = pygame.display.set_mode(UI.WINDOW_SIZE)
        pygame.display.set_caption("Astro Party Clone")
        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.INTRO_MENU

class GameMatchState:
    HUMAN_START_POS = Vector2(8, -8)
    HUMAN_START_VEL = Vector2(0, 0)
    HUMAN_START_ANG = 90
    CAMERA_START_POS = Vector2(0, 0)
    CAMERA_INIT_VIEW_SIZE = 10

    def __init__(self, game):
        self.human = PlayerShip(GameMatchState.HUMAN_START_POS,
                                GameMatchState.HUMAN_START_VEL,
                                GameMatchState.HUMAN_START_ANG)

        #self.ai = PlayerShip()

        self.camera = Camera(game,
                             GameMatchState.CAMERA_START_POS,
                             GameMatchState.CAMERA_INIT_VIEW_SIZE)

class GamePhase:
    INTRO_MENU = 0
    IN_MATCH = 1
    GAME_EXITED = 2


def main():
    game = GameInfo()
    while game.game_phase != GamePhase.GAME_EXITED:
        game.clock.tick(120)
        if game.game_phase == GamePhase.INTRO_MENU:
            intro_menu_phase(game)
        elif game.game_phase == GamePhase.IN_MATCH:
            game_match_phase(game)
        pygame.display.flip()


def intro_menu_phase(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.game_phase = GamePhase.GAME_EXITED

    game.screen.fill(UI.BLACK)
    intro_menu_phase.play_button.render(game)
    intro_menu_phase.title_text.render(game)


intro_menu_phase.play_button = UITools.Button("PLAY", UI.WHITE, UI.BLACK,
                                              Vector2(0.5, 0.5), 1 / 7,
                                              GamePhase.IN_MATCH)
intro_menu_phase.title_text = UITools.Text("ASTRO WARS", UI.WHITE,
                                           Vector2(0.5, 0.5 - 1 / 7), 3 / 7)

def game_match_phase(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.game_phase = GamePhase.GAME_EXITED

    if not game_match_phase.match_started:
        game_match_phase.match_started = True
        game_match_phase.match_state = GameMatchState(game)
    match_state = game_match_phase.match_state

    game.screen.fill(UI.BLACK)
    dt = game.clock.get_time() / 1000
    match_state.human.take_in_player_input(dt)
    match_state.human.pos_update(dt)
    match_state.camera.render_player_ship(match_state.human, GameGraphics.BLUE_SHIP_SURFACE)


game_match_phase.match_started = False
game_match_phase.match_state = None

class PlayerShip:
    MAX_SPEED = 8
    SHIP_ACCEL_MAGNITUDE = 10
    TURNING_ANGULAR_VEL = 170

    MAX_SHOTS = 3
    SHOT_ANIM_ANGULAR_VEL = 5

    SHIP_SIZE = Vector2(1, 1)

    def __init__(self, pos, vel, angle):
        self.pos = pos
        self.vel = vel
        self.accel = 0
        self.angle = angle
        self.shots_left = PlayerShip.MAX_SHOTS
        self.shot_rotate_anim_angle = 0

    def pos_update(self, dt):
        self.accel = Vector2.from_polar((PlayerShip.SHIP_ACCEL_MAGNITUDE, self.angle + 90))
        self.vel = self.vel + (self.accel * dt)
        self.vel.clamp_magnitude_ip(PlayerShip.MAX_SPEED)
        self.pos = self.pos + (self.vel * dt)

    def take_in_player_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle -= PlayerShip.TURNING_ANGULAR_VEL * dt


class Camera:
    def __init__(self, game, center, size_of_view):
        self.center = center
        self.size_of_view = size_of_view
        self.game: GameInfo = game

    def render_player_ship(self, ship: PlayerShip, ship_image):
        ship_camera_disp = ship.pos - self.center
        coord_to_pixel_factor = UI.WINDOW_MIN_COORD_SIZE/(2 * self.size_of_view)
        ship_pixel_disp = ship_camera_disp * coord_to_pixel_factor
        ship_pixel_disp.update(ship_pixel_disp[0], -ship_pixel_disp[1])
        ship_pixel_pos = ship_pixel_disp + UI.WINDOW_SIZE / 2

        ship_render_image = pygame.transform.scale(ship_image, PlayerShip.SHIP_SIZE * coord_to_pixel_factor)
        ship_render_image = pygame.transform.rotate(ship_render_image, ship.angle)

        # Pygame Renders Images With Top Left Corner Of Image At Given Position
        offset = Vector2(ship_render_image.get_size()) / 2

        self.game.screen.blit(ship_render_image, ship_pixel_pos - offset)


if __name__ == '__main__':
    main()
