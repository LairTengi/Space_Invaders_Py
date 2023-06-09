import sys

import pygame
from serialization import graceful_shutdown
from view import fire_bullet, prepare_game
from model import fire_bomb


def check_events(self):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(self, event)
        elif event.type == pygame.KEYUP:
            check_keyup_events(self, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            check_play_button(self, mouse_position)


def check_keydown_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = True
    elif event.key == pygame.K_ESCAPE:
        graceful_shutdown(self)    # ESC для выхода
    elif event.key == pygame.K_SPACE:
        fire_bullet(self)
    elif event.key == pygame.K_b:  # Кнопка b для бомбы
        fire_bomb(self)
    elif event.key == pygame.K_p and not self.stats.game_active:
        if self.FIRST_GAME:
            prepare_game(self)
            self.FIRST_GAME = False
            pygame.mixer.music.play()
        else:
            self.stats.game_active = True
            pygame.mixer.music.play()
    elif event.key == pygame.K_p and self.stats.game_active:
        self.stats.game_active = False
        pygame.mixer.music.pause()


def check_keyup_events(self, event):
    if event.key == pygame.K_RIGHT:
        self.ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        self.ship.moving_left = False


def check_play_button(self, mouse_pos):
    button_clicked = self.play_button.rect.collidepoint(mouse_pos)
    if button_clicked and not self.stats.game_active:
        prepare_game(self)
        pygame.mixer.music.play()

