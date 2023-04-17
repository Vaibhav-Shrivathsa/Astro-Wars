import pygame
from pygame.math import Vector2

import UITools
from UITools import UI
from GameInfo import *


def intro_menu_phase(game):
    game.screen.fill(UI.BLACK)
    intro_menu_phase.play_button.render(game)
    intro_menu_phase.credits_button.render(game)
    intro_menu_phase.info_button.render(game)
    intro_menu_phase.title_text.render(game)


intro_menu_phase.play_button = UITools.Button("PLAY", UI.WHITE, UI.BLACK,
                                              Vector2(0.5 - 1 / 13, 0.5 + 1 / 13), 1 / 7,
                                              GamePhase.IN_MATCH)
intro_menu_phase.info_button = UITools.Button("INFO", UI.WHITE, UI.BLACK,
                                              Vector2(0.5 + 1 / 13, 0.5 + 1 / 13), 1 / 7,
                                              GamePhase.INFO_MENU)
intro_menu_phase.credits_button = UITools.Button("CREDITS", UI.WHITE, UI.BLACK,
                                                 Vector2(0.5, 0.5), 1 / 4,
                                                 GamePhase.CREDITS_MENU)
intro_menu_phase.title_text = UITools.Text("ASTRO WARS", UI.WHITE,
                                           Vector2(0.5, 0.5 - 1 / 12), 3 / 7)


def credit_menu_phase(game):
    game.screen.fill(UI.BLACK)
    credit_menu_phase.inspired_text.render(game)
    credit_menu_phase.author_text.render(game)
    credit_menu_phase.project_text.render(game)
    credit_menu_phase.return_button.render(game)


credit_menu_phase.project_text = UITools.Text("CS 109 Final Project", UI.WHITE,
                                              Vector2(0.5, 0.5 - 2 / 7), 4 / 7)
credit_menu_phase.author_text = UITools.Text("Made By Vaibhav Shrivathsa", UI.WHITE,
                                             Vector2(0.5, 0.5 - 1 / 7), 5 / 7)
credit_menu_phase.inspired_text = UITools.Text("Inspired By Astro Party", UI.WHITE,
                                               Vector2(0.5, 0.5), 6 / 7)
credit_menu_phase.return_button = UITools.Button("RETURN", UI.WHITE, UI.BLACK,
                                                 Vector2(0.5, 0.5 + 1 / 7), 1 / 5,
                                                 GamePhase.INTRO_MENU)

def info_menu_phase(game):
    game.screen.fill(UI.BLACK)
    info_menu_phase.player_1_instructions.render(game)
    info_menu_phase.player_2_instructions.render(game)
    info_menu_phase.yellow_block_text.render(game)
    info_menu_phase.return_button.render(game)


info_menu_phase.player_1_instructions = UITools.Text("Player 1: A - Turn, D - Shoot", UI.WHITE,
                                              Vector2(0.5, 0.5 - 2 / 7), 4 / 7)
info_menu_phase.player_2_instructions = UITools.Text("Player 2: ← - Turn, → - Shoot", UI.WHITE,
                                             Vector2(0.5, 0.5 - 1 / 7), 4 / 7)
info_menu_phase.yellow_block_text = UITools.Text("Yellow Blocks Can Be Destroyed", UI.WHITE,
                                               Vector2(0.5, 0.5), 4 / 7)
info_menu_phase.return_button = UITools.Button("RETURN", UI.WHITE, UI.BLACK,
                                                 Vector2(0.5, 0.5 + 1 / 7), 1 / 5,
                                                 GamePhase.INTRO_MENU)
