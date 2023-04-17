import math
import copy

import CollisionDetection
import Stages
import UITools
from GameInfo import *
import pygame
from pygame.math import Vector2


class GameGraphics:
    ship_image_size = Vector2(100, 100)
    BLUE_SHIP_SURFACE = pygame.image.load("assets/blue-ship.png")


class GameMatchState:
    HUMAN_START_POS = Vector2(8, -8)
    HUMAN_START_VEL = Vector2(0, 0)
    HUMAN_START_ANG = 90
    CAMERA_START_POS = Vector2(0, 0)
    CAMERA_INIT_VIEW_SIZE = 11

    def __init__(self, game):
        self.human = PlayerShip(GameMatchState.HUMAN_START_POS,
                                GameMatchState.HUMAN_START_VEL,
                                GameMatchState.HUMAN_START_ANG)

        # self.ai = PlayerShip()

        self.camera = Camera(game,
                             GameMatchState.CAMERA_START_POS,
                             GameMatchState.CAMERA_INIT_VIEW_SIZE)

        self.stage = copy.deepcopy(Stages.Stages.BASIC)
        self.outer_border = None


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

    def pos_update(self, dt, stage):
        self.accel = Vector2.from_polar((PlayerShip.SHIP_ACCEL_MAGNITUDE, self.angle + 90))
        self.vel = self.vel + (self.accel * dt)
        self.vel.clamp_magnitude_ip(PlayerShip.MAX_SPEED)
        self.pos = self.pos + (self.vel * dt)

        ship_collider = CollisionDetection.Circle(self.pos, 0.3)
        for destructable_block in stage.destructable_blocks:
            self.pos, self.vel = ship_collider.fix_collision_with_rect(destructable_block.collider, self.vel)

        for indestructable_block in stage.indestructable_blocks:
            self.pos, self.vel = ship_collider.fix_collision_with_rect(indestructable_block.collider, self.vel)

        if stage.outer_boundary is not None:
            if ship_collider.is_colliding_with_inverted_rect(stage.outer_boundary.collider):
                self.pos, self.vel = ship_collider.fix_collision_with_inverted_rect(stage.outer_boundary.collider,
                                                                                    self.vel)

    def take_in_player_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.angle -= PlayerShip.TURNING_ANGULAR_VEL * dt


class Camera:
    def __init__(self, game, center, size_of_view):
        self.center = center
        self.size_of_view = size_of_view
        self.game: GameInfo = game

    def coord_to_pixel_factor(self):
        return UI.WINDOW_MIN_COORD_SIZE / (2 * self.size_of_view)

    def game_coord_to_pixel_coord(self, game_coord):
        pixel_coord = (game_coord - self.center) * self.coord_to_pixel_factor()
        pixel_coord.update(pixel_coord[0], -pixel_coord[1])
        pixel_coord += UI.WINDOW_CENTER
        return pixel_coord

    def render_player_ship(self, ship: PlayerShip, ship_image):
        ship_render_image = pygame.transform.scale(ship_image, PlayerShip.SHIP_SIZE * self.coord_to_pixel_factor())
        ship_render_image = pygame.transform.rotate(ship_render_image, ship.angle)

        # Pygame Renders Images With Top Left Corner Of Image At Given Position
        offset = Vector2(ship_render_image.get_size()) / 2

        self.game.screen.blit(ship_render_image, self.game_coord_to_pixel_coord(ship.pos) - offset)

    def render_block(self, center, size, color, thickness):
        offset = size / 2
        offset.update(offset[0], -offset[1])
        top_left = center - offset
        top_left = self.game_coord_to_pixel_coord(top_left)

        size = size * self.coord_to_pixel_factor()
        rect_to_draw = pygame.Rect(top_left, size)

        pygame.draw.rect(self.game.screen, color,
                         rect_to_draw, round(thickness * self.coord_to_pixel_factor()))

    def render_stage(self, stage: Stages.Stage):
        if stage.outer_boundary is not None:
            self.render_block(stage.outer_boundary.center,
                              stage.outer_boundary.size,
                              Stages.OuterBoundary.COLOR,
                              Stages.OuterBoundary.THICKNESS)
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


def game_match_phase(game):
    if not game_match_phase.match_started:
        game_match_phase.match_started = True
        game_match_phase.match_state = GameMatchState(game)
    match_state = game_match_phase.match_state

    dt = game.clock.get_time() / 1000
    game.screen.fill(UI.BLACK)
    match_state.human.take_in_player_input(dt)
    match_state.human.pos_update(dt, match_state.stage)
    match_state.camera.render_stage(match_state.stage)
    match_state.camera.render_player_ship(match_state.human, GameGraphics.BLUE_SHIP_SURFACE)
    game_match_phase.pause_button.render(game)

game_match_phase.match_started = False
game_match_phase.match_state = None
game_match_phase.pause_button = UITools.Button("PAUSE", UI.WHITE, UI.BLACK,
                                               Vector2(0.93, 0.07), 1 / 12,
                                               GamePhase.GAME_PAUSED)


def game_paused_phase(game):
    game.screen.fill(UI.BLACK)
    match_state = game_match_phase.match_state
    match_state.camera.render_stage(match_state.stage)
    match_state.camera.render_player_ship(match_state.human, GameGraphics.BLUE_SHIP_SURFACE)

    pygame.draw.rect(game.screen, UI.BLACK, pygame.Rect(0.4 * UI.WINDOW_SIZE, 0.2 * UI.WINDOW_SIZE))
    game_paused_phase.resume_button.render(game)
    game_paused_phase.end_game_button.render(game)


game_paused_phase.resume_button = UITools.Button("RESUME", (0, 255, 0), UI.WHITE,
                                                 Vector2(0.5, 0.5 + 1 / 24), 1 / 7,
                                                 GamePhase.IN_MATCH)
game_paused_phase.end_game_button = UITools.Button("END GAME", (255, 0, 0), UI.WHITE,
                                                   Vector2(0.5, 0.5 - 1 / 24), 1 / 6,
                                                   GamePhase.INTRO_MENU)
