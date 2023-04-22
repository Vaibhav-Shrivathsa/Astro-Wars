import pygame
from pygame.math import Vector2
import random
import copy
import time

import CollisionDetection
import Stages
import UITools
from GameInfo import *

random.seed(time.time())


class GameGraphics:
    ship_image_size = Vector2(100, 100)
    BLUE_SHIP_SURFACE = pygame.image.load("assets/blue-ship.png")
    RED_SHIP_SURFACE = pygame.image.load("assets/red-ship.png")


class GameKeyBindings:
    """
    Class that holds the keybindings for various player actions
    """
    PLAYER1_TURN = pygame.K_a
    PLAYER1_SHOOT = pygame.K_d

    PLAYER2_TURN = pygame.K_LEFT
    PLAYER2_SHOOT = pygame.K_RIGHT


class GameMatchState:
    """
    Class that contains important information for an ongoing match
    """
    PLAYER1_START_POS = Vector2(8, -8)
    PLAYER1_START_VEL = Vector2(0, 0)
    PLAYER1_START_ANG = 90

    PLAYER2_START_POS = Vector2(-8, 8)
    PLAYER2_START_VEL = Vector2(0, 0)
    PLAYER2_START_ANG = 270

    CAMERA_START_POS = Vector2(0, 0)
    CAMERA_INIT_VIEW_SIZE = 11

    def __init__(self, game):
        self.player1 = PlayerShip(GameMatchState.PLAYER1_START_POS,
                                  GameMatchState.PLAYER1_START_VEL,
                                  GameMatchState.PLAYER1_START_ANG)

        self.player2 = PlayerShip(GameMatchState.PLAYER2_START_POS,
                                  GameMatchState.PLAYER2_START_VEL,
                                  GameMatchState.PLAYER2_START_ANG)

        self.camera = Camera(game,
                             GameMatchState.CAMERA_START_POS,
                             GameMatchState.CAMERA_INIT_VIEW_SIZE)

        self.stage = copy.deepcopy(random.choice(Stages.PlayableStages.STAGELIST))
        self.outer_border = None
        self.bullets = set()


class PlayerShip:
    MAX_SPEED = 8
    SHIP_ACCEL_MAGNITUDE = 10
    TURNING_ANGULAR_VEL = 170

    SHIP_SIZE = Vector2(1, 1)

    SHIP_COLLIDER_RADIUS = 0.3  # Radius For The Collider That Determines If
    # The Ship Is Colliding With A Wall
    HIT_CIRCLE_RADIUS = 0.35  # Radius For The Collider That Determines Hits
    # From Bullets

    BULLET_SPAWN_DIST = 0.4

    TIME_BETWEEN_SHOTS = 0.4

    def __init__(self, pos, vel, angle):
        self.pos = pos
        self.vel = vel
        self.accel = 0
        self.angle = angle
        self.last_shot_time = 0
        self.died = False

    def ship_direction(self):
        return Vector2.from_polar((1, self.angle + 90))

    def pos_update(self, dt, stage):
        self.accel = PlayerShip.SHIP_ACCEL_MAGNITUDE * self.ship_direction()
        self.vel = self.vel + (self.accel * dt)
        self.vel.clamp_magnitude_ip(PlayerShip.MAX_SPEED)
        self.pos = self.pos + (self.vel * dt)

        ship_collider = CollisionDetection.Circle(self.pos, PlayerShip.SHIP_COLLIDER_RADIUS)
        for destructable_block in stage.destructable_blocks:
            self.pos, self.vel = ship_collider.fix_collision_with_rect(destructable_block.collider, self.vel)

        for indestructable_block in stage.indestructable_blocks:
            self.pos, self.vel = ship_collider.fix_collision_with_rect(indestructable_block.collider, self.vel)

        if stage.outer_boundary is not None:
            if ship_collider.is_colliding_with_inverted_rect(stage.outer_boundary.collider):
                self.pos, self.vel = ship_collider.fix_collision_with_inverted_rect(stage.outer_boundary.collider,
                                                                                    self.vel)

    def turn_if_player_input(self, dt, turn_key):
        keys = pygame.key.get_pressed()
        if keys[turn_key]:
            self.angle -= PlayerShip.TURNING_ANGULAR_VEL * dt


class Bullet:
    COLOR = (255, 255, 255)
    RADIUS = 0.1
    SPEED = 12

    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel
        self.destroyed = False

    def pos_update(self, dt, stage, match_state):
        self.pos += self.vel * dt

        bullet_collider = CollisionDetection.Circle(self.pos, Bullet.RADIUS)

        player1_collider = CollisionDetection.Circle(match_state.player1.pos, PlayerShip.HIT_CIRCLE_RADIUS)
        if bullet_collider.is_colliding_with_circle(player1_collider):
            self.destroyed = True
            match_state.camera.start_shaking()
            match_state.player1.died = True
            return

        player2_collider = CollisionDetection.Circle(match_state.player2.pos, PlayerShip.HIT_CIRCLE_RADIUS)
        if bullet_collider.is_colliding_with_circle(player2_collider):
            self.destroyed = True
            match_state.camera.start_shaking()
            match_state.player2.died = True
            return

        for destructable_block in stage.destructable_blocks:
            if bullet_collider.is_colliding_with_rect(destructable_block.collider):
                self.destroyed = True
                match_state.camera.start_shaking()
                stage.destructable_blocks.remove(destructable_block)
                return

        for indestructable_block in stage.indestructable_blocks:
            if bullet_collider.is_colliding_with_rect(indestructable_block.collider):
                self.destroyed = True
                return

        if stage.outer_boundary is not None:
            if bullet_collider.is_colliding_with_inverted_rect(stage.outer_boundary.collider):
                self.destroyed = True


def handle_bullets(game, match_state):
    """
    Handles the destruction of bullets when they collide with objects,
    the effects of their collision on destructable objects,
    and spawns new bullets when players shoot
    """
    keys = pygame.key.get_pressed()
    curr_time = time.time()
    if keys[GameKeyBindings.PLAYER1_SHOOT]:
        if curr_time - match_state.player1.last_shot_time >= PlayerShip.TIME_BETWEEN_SHOTS:
            match_state.player1.last_shot_time = curr_time
            ship_dir = match_state.player1.ship_direction()
            ship_pos = match_state.player1.pos
            new_bullet = Bullet(ship_pos + ship_dir * PlayerShip.BULLET_SPAWN_DIST,
                                ship_dir * Bullet.SPEED)
            match_state.bullets.add(new_bullet)

    if keys[GameKeyBindings.PLAYER2_SHOOT]:
        if curr_time - match_state.player2.last_shot_time >= PlayerShip.TIME_BETWEEN_SHOTS:
            match_state.player2.last_shot_time = curr_time
            ship_dir = match_state.player2.ship_direction()
            ship_pos = match_state.player2.pos
            new_bullet = Bullet(ship_pos + ship_dir * PlayerShip.BULLET_SPAWN_DIST,
                                ship_dir * Bullet.SPEED)
            match_state.bullets.add(new_bullet)

    # Fun Easter Egg: 0 Shakes the Screen
    if keys[pygame.K_0]:
        match_state.camera.start_shaking()

    dt = game.clock.get_time() / 1000
    for bullet in match_state.bullets:
        bullet.pos_update(dt, match_state.stage, match_state)
    match_state.bullets = set(
        filter(lambda x: not x.destroyed, match_state.bullets))


class Camera:
    """
    Class that handles converting the locations of objects into
    pixel coordinates and rendering the objects
    """
    MIN_SIZE_OF_VIEW = 17
    MAX_SIZE_OF_VIEW = 24
    VIEW_SIZE_PADDING = 6

    TOTAL_SHAKE_DURATION = 0.3
    SHAKE_OFFSET_HOLD_TIME = 0.03  # how long each camera jolt in the shake lasts
    SHAKE_MAX_MAGNITUDE = 10  # maximum displacement of the camera in pixels

    # the magnitude of the shake linearly decreases as the shake progresses

    def __init__(self, game, center, size_of_view):
        """
        Initializes the Camera
        :param game: GameInfo Object For the Game
        :param center: Initial Center of the Camera
        :param size_of_view: The in-game unit of length that should be visible
        in the window's smallest dimension (controls the zoom of the camera)
        """
        self.center = center
        self.size_of_view = size_of_view
        self.game = game

        self.is_shaking = False
        self.shake_started_time = time.time()
        self.current_offset_number = 0
        self.current_shake_offset = Vector2(0, 0)

        self.current_time = time.time()

    def coord_to_pixel_factor(self):
        """
        Gives the unit conversion factor between the game logic's location
        units and pixel screen space depending on the camera's current
        zoom level
        """
        return UI.WINDOW_MIN_COORD_SIZE / self.size_of_view

    def game_coord_to_pixel_coord(self, game_coord):
        """
        Converts a Vector2 object representing the location of an object
        in the imaginary space of the game to a pixel location on the
        screen
        """
        camera_center = self.center + self.current_shake_offset
        pixel_coord = (game_coord - camera_center) * self.coord_to_pixel_factor()
        pixel_coord.update(pixel_coord[0], -pixel_coord[1])
        pixel_coord += UI.WINDOW_CENTER
        return pixel_coord

    def dynamic_camera_zoom_update(self, player1_ship, player2_ship):
        """
        Change the zoom level of the camera and its center based on
        the location of the player ships
        """
        self.center = (player1_ship.pos + player2_ship.pos) / 2
        self.size_of_view = max(abs(player1_ship.pos[0] - player2_ship.pos[0]),
                                abs(player1_ship.pos[1] - player2_ship.pos[1]))
        self.size_of_view += Camera.VIEW_SIZE_PADDING
        self.size_of_view = max(self.size_of_view, Camera.MIN_SIZE_OF_VIEW)
        self.size_of_view = min(self.size_of_view, Camera.MAX_SIZE_OF_VIEW)

    def render_player_ship(self, ship, ship_image):
        ship_render_image = pygame.transform.scale(ship_image, PlayerShip.SHIP_SIZE * self.coord_to_pixel_factor())
        ship_render_image = pygame.transform.rotate(ship_render_image, ship.angle)

        # Pygame Renders Images With Top Left Corner Of Image At Given Position
        offset = Vector2(ship_render_image.get_size()) / 2

        self.game.screen.blit(ship_render_image,
                              self.game_coord_to_pixel_coord(ship.pos) - offset)

    def render_block(self, center, size, color, thickness):
        offset = size / 2
        offset.update(offset[0], -offset[1])
        top_left = center - offset
        top_left = self.game_coord_to_pixel_coord(top_left)

        size = size * self.coord_to_pixel_factor()
        rect_to_draw = pygame.Rect(top_left, size)

        pygame.draw.rect(self.game.screen, color,
                         rect_to_draw,
                         round(thickness * self.coord_to_pixel_factor()))

    def render_stage(self, stage):
        for destructable_block in stage.destructable_blocks:
            self.render_block(destructable_block.center,
                              destructable_block.size,
                              Stages.DestructableBlock.COLOR,
                              Stages.DestructableBlock.THICKNESS)
        for indestructable_block in stage.indestructable_blocks:
            self.render_block(indestructable_block.center,
                              indestructable_block.size,
                              Stages.IndestructableBlock.COLOR,
                              Stages.IndestructableBlock.THICKNESS)
        if stage.outer_boundary is not None:
            self.render_block(stage.outer_boundary.center,
                              stage.outer_boundary.size,
                              Stages.OuterBoundary.COLOR,
                              Stages.OuterBoundary.THICKNESS)

    def render_bullets(self, bullets):
        for bullet in bullets:
            bullet_pixel_pos = self.game_coord_to_pixel_coord(bullet.pos)
            if bullet_pixel_pos[0] >= 0:
                # pygame will render a large horizontal white line if the
                # x coordinate of the circle is off of the screen
                pygame.draw.circle(self.game.screen, Bullet.COLOR,
                                   self.game_coord_to_pixel_coord(bullet.pos),
                                   Bullet.RADIUS *
                                   self.coord_to_pixel_factor())

    def start_shaking(self):
        if not self.is_shaking:
            self.is_shaking = True
            self.shake_started_time = time.time()
            self.current_offset_number = 0
            self.current_shake_offset = \
                pygame.Vector2.from_polar((Camera.SHAKE_MAX_MAGNITUDE, random.random() * 360))
            self.current_shake_offset /= self.coord_to_pixel_factor()

    def update_internal_time(self):
        """
        Handles updating the current time of the camera and appropriately
        handles updating state related to camera shaking
        """
        self.current_time = time.time()
        if self.is_shaking:
            time_shaken = self.current_time - self.shake_started_time
            if time_shaken >= self.TOTAL_SHAKE_DURATION:
                self.is_shaking = False
                self.current_shake_offset = Vector2(0, 0)
            else:
                curr_shake_offset_number = time_shaken // Camera.SHAKE_OFFSET_HOLD_TIME

                if curr_shake_offset_number != self.current_offset_number:
                    self.current_offset_number = curr_shake_offset_number
                    perctange_shake_left = 1 - time_shaken / Camera.TOTAL_SHAKE_DURATION
                    self.current_shake_offset = \
                        pygame.Vector2.from_polar((Camera.SHAKE_MAX_MAGNITUDE * perctange_shake_left,
                                                   random.random() * 360)) / self.coord_to_pixel_factor()
        else:
            self.current_shake_offset = Vector2(0, 0)


def render_game_match(game, match_state):
    """
    Handles drawing all game objects to the screen
    """
    match_state.camera.update_internal_time()
    match_state.camera.dynamic_camera_zoom_update(match_state.player1, match_state.player2)
    match_state.camera.render_stage(match_state.stage)
    match_state.camera.render_bullets(match_state.bullets)
    if not match_state.player1.died:
        match_state.camera.render_player_ship(match_state.player1, GameGraphics.BLUE_SHIP_SURFACE)
    if not match_state.player2.died:
        match_state.camera.render_player_ship(match_state.player2, GameGraphics.RED_SHIP_SURFACE)


def game_match_phase(game):
    """
    Displays the game while a match is ongoing and actively being played
    """
    if not game_match_phase.match_started:
        game_match_phase.match_started = True
        game_match_phase.match_state = GameMatchState(game)
        game_match_phase.bullets = set()
    match_state = game_match_phase.match_state

    dt = game.clock.get_time() / 1000
    game.screen.fill(UI.BLACK)

    match_state.player1.turn_if_player_input(dt, GameKeyBindings.PLAYER1_TURN)
    match_state.player1.pos_update(dt, match_state.stage)

    match_state.player2.turn_if_player_input(dt, GameKeyBindings.PLAYER2_TURN)
    match_state.player2.pos_update(dt, match_state.stage)

    handle_bullets(game, match_state)

    render_game_match(game, match_state)
    game_match_phase.pause_button.render(game)

    if match_state.player1.died or match_state.player2.died:
        game_match_phase.time_ended = time.time()
        game.game_phase = GamePhase.GAME_ENDED


game_match_phase.match_started = False
game_match_phase.match_state = None
game_match_phase.pause_button = UITools.Button("PAUSE", UI.WHITE, UI.BLACK,
                                               Vector2(0.93, 0.07), 1 / 12,
                                               GamePhase.GAME_PAUSED)
game_match_phase.time_ended = 0


def game_paused_phase(game):
    """
    Displays the game when the pause menu is opened during a match
    """
    game.screen.fill(UI.BLACK)
    match_state = game_match_phase.match_state
    render_game_match(game, match_state)

    pygame.draw.rect(game.screen, UI.BLACK,
                     pygame.Rect(0.4 * UI.WINDOW_SIZE, 0.2 * UI.WINDOW_SIZE))
    game_paused_phase.resume_button.render(game)
    game_paused_phase.end_game_button.render(game)


game_paused_phase.resume_button = UITools.Button("RESUME", (0, 255, 0), UI.WHITE,
                                                 Vector2(0.5, 0.5 + 1 / 24), 1 / 7,
                                                 GamePhase.IN_MATCH)
game_paused_phase.end_game_button = UITools.Button("END GAME", (255, 0, 0), UI.WHITE,
                                                   Vector2(0.5, 0.5 - 1 / 24), 1 / 6,
                                                   GamePhase.INTRO_MENU)


def game_ended_phase(game):
    """
    Displays the second right after the game ends where
    the game freezes to show the last player standing
    """
    match_state = game_match_phase.match_state

    if time.time() - game_match_phase.time_ended >= \
            game_ended_phase.TIME_IN_END:
        game.game_phase = GamePhase.INTRO_MENU

    game.screen.fill(UI.BLACK)
    render_game_match(game, match_state)


game_ended_phase.TIME_IN_END = 1
