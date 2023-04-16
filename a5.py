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
pygame.init()

def add(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]
def sub(tuple1, tuple2):
    return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]
def scale(tuple, scalar):
    return tuple[0] * scalar, tuple[1] * scalar

class UI:
    WINDOW_SIZE = (700, 700)
    pygame.font.init()
    TITLE_FONT = pygame.font.SysFont('Lucida Console', 50)
    TEXT_FONT = pygame.font.SysFont('Lucida Console', 30)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class GameGraphics:
    ship_image_size = (100, 100)
    BLUE_SHIP_SURFACE = pygame.image.load("blue-ship.png")

class GameState:
    def __init__(self):
        self.screen = pygame.display.set_mode(UI.WINDOW_SIZE)
        pygame.display.set_caption("Astro Party Clone")
        self.clock = pygame.time.Clock()
        self.game_phase = GamePhase.INTRO_MENU

class GameMatchState:
    HUMAN_START_POS = (8.0, -8.0)
    HUMAN_START_VEL = (0.0, 0.0)
    HUMAN_START_ANG = 90
    CAMERA_START_POS = (0.0, 0.0)
    CAMERA_INIT_VIEW_SIZE = 10

    def __init__(self, game):
        self.human = PlayerShip()
        self.human.pos = GameMatchState.HUMAN_START_POS
        self.human.vel = GameMatchState.HUMAN_START_VEL
        self.human.angle = GameMatchState.HUMAN_START_ANG
        self.ai = PlayerShip()

        self.camera = Camera(game)
        self.camera.center = GameMatchState.CAMERA_START_POS
        self.camera.size_of_view = GameMatchState.CAMERA_INIT_VIEW_SIZE

class GamePhase:
    INTRO_MENU = 0
    IN_MATCH = 1
    GAME_EXITED = 2


WINDOW_SIZE = (700, 700)


def main():
    game = GameState()
    while game.game_phase != GamePhase.GAME_EXITED:
        game.clock.tick(60)
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

    screen_center = scale(UI.WINDOW_SIZE, 1/2)
    title = UI.TITLE_FONT.render("ASTRO WARS", False, UI.WHITE)
    title_pos = add(screen_center, (0, -100))
    game.screen.blit(title, dest=sub(title_pos, scale(title.get_size(), 1/2)))

    play_text = UI.TEXT_FONT.render("PLAY", False, UI.WHITE)
    play_text_pos = add(screen_center, (0, 0))

    play_box_size = scale(play_text.get_size(), 3/2)
    play_top_left = sub(play_text_pos, scale(play_box_size, 1/2))

    if play_top_left[0] <= pygame.mouse.get_pos()[0] <= play_top_left[0] + play_box_size[0] and \
       play_top_left[1] <= pygame.mouse.get_pos()[1] <= play_top_left[1] + play_box_size[1]:
        play_text = UI.TEXT_FONT.render("PLAY", False, UI.BLACK)
        pygame.draw.rect(game.screen, UI.WHITE,
                         pygame.Rect(play_top_left[0], play_top_left[1], play_box_size[0], play_box_size[1]))
        game.screen.blit(play_text, dest=sub(play_text_pos, scale(play_text.get_size(), 1 / 2)))
        if pygame.mouse.get_pressed()[0]:
            game.game_phase = GamePhase.IN_MATCH
    else:
        game.screen.blit(play_text, dest=sub(play_text_pos, scale(play_text.get_size(), 1 / 2)))
        pygame.draw.rect(game.screen, UI.WHITE,
                         pygame.Rect(play_top_left[0], play_top_left[1], play_box_size[0], play_box_size[1]), 2)

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
    MAX_SHOTS = 3
    SHOT_ANIM_ANGULAR_VEL = 5
    TURNING_ANGULAR_VEL = 170
    SHIP_SIZE = (1, 1)

    def __init__(self):
        self.pos = None
        self.vel = None
        self.accel = None
        self.angle = None
        self.shots_left = PlayerShip.MAX_SHOTS
        self.shot_rotate_anim_angle = 0

    def pos_update(self, dt):
        self.accel = (-math.sin(math.radians(self.angle)) * 10, math.cos(math.radians(self.angle)) * 8)
        self.vel = add(self.vel, scale(self.accel, dt))
        if self.vel[0] ** 2 + self.vel[1] ** 2 > PlayerShip.MAX_SPEED ** 2:
            self.vel = scale(self.vel, PlayerShip.MAX_SPEED/math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2))
        self.pos = add(self.pos, scale(self.vel, dt))

    def take_in_player_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle -= PlayerShip.TURNING_ANGULAR_VEL * dt


class Camera:
    def __init__(self, game):
        self.center = None
        self.size_of_view = None
        self.game: GameState = game

    def render_player_ship(self, ship: PlayerShip, ship_image):
        ship_camera_disp = sub(ship.pos, self.center)
        coord_to_pixel_factor = UI.WINDOW_SIZE[0]/(2 * self.size_of_view)
        ship_pixel_disp = scale(ship_camera_disp, coord_to_pixel_factor)
        ship_pixel_disp = (ship_pixel_disp[0], -ship_pixel_disp[1])
        ship_pixel_pos = add(scale(UI.WINDOW_SIZE, 1/2), ship_pixel_disp)

        ship_img_size = scale(PlayerShip.SHIP_SIZE, coord_to_pixel_factor)
        ship_render_image = pygame.transform.scale(ship_image, scale(PlayerShip.SHIP_SIZE, coord_to_pixel_factor))
        ship_render_image = pygame.transform.rotate(ship_render_image, ship.angle)

        render_img_size = ship_render_image.get_size()
        ship_pixel_pos_offset = scale(render_img_size, 1/2)

        self.game.screen.blit(ship_render_image, sub(ship_pixel_pos, ship_pixel_pos_offset))


if __name__ == '__main__':
    main()
