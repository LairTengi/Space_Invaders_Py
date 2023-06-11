import unittest
from unittest.mock import MagicMock

import pygame

from Space_Invanders import SpaceInvaders
from Stats.GameStatistics import GameStats
from Stats.ScoreTable import ScoreTable
from model import fire_bomb, change_mystery_ship_direction, change_armada_direction
from models.Invader import Invader
from models.Mystery_ship import MysteryShip


class TestSpaceInvaders(unittest.TestCase):
    # Инициализация
    def setUp(self):
        self.space_invaders = SpaceInvaders()
        self.space_invaders.stats = GameStats(self.space_invaders)
        self.space_invaders.score_table = ScoreTable(self.space_invaders)
        self.space_invaders.invaders = pygame.sprite.Group()
        self.create_test_invaders()
        self.space_invaders.mystery_ship = MysteryShip(self.space_invaders)

    def create_test_invaders(self):
        invader1 = Invader(self.space_invaders)
        invader2 = Invader(self.space_invaders)
        invader3 = Invader(self.space_invaders)
        self.space_invaders.invaders.add(invader1, invader2, invader3)

    # Отрабатывание fire_bomb, когда бомбы есть
    def test_fire_bomb_with_bombs_left(self):
        self.space_invaders.stats.bombs_left = 3
        self.space_invaders.bomb.add = MagicMock()

        fire_bomb(self.space_invaders)

        self.assertEqual(self.space_invaders.stats.bombs_left, 2)
        self.assertTrue(self.space_invaders.bomb.add.called)

    # Отрабатывание fire_bomb, когда бомб нет
    def test_fire_bomb_with_no_bombs_left(self):
        self.space_invaders.stats.bombs_left = 0
        self.space_invaders.bomb.add = MagicMock()

        result = fire_bomb(self.space_invaders)

        self.assertEqual(self.space_invaders.stats.bombs_left, 0)
        self.assertIsNone(result)
        self.assertFalse(self.space_invaders.bomb.add.called)

    # Изменение направления мистического корабля
    def test_change_mystery_ship_direction(self):
        original_y = self.space_invaders.mystery_ship.rect.y
        original_direction = self.space_invaders.settings.armada_direction

        change_mystery_ship_direction(self.space_invaders)

        expected_y = original_y + self.space_invaders.settings.armada_drop_speed
        expected_direction = original_direction * -1

        self.assertEqual(self.space_invaders.mystery_ship.rect.y, expected_y)
        self.assertEqual(self.space_invaders.settings.armada_direction, expected_direction)

    # Изменение направления армады
    def test_change_armada_direction(self):
        original_direction = self.space_invaders.settings.armada_direction
        original_y_values = [invader.rect.y for invader in self.space_invaders.invaders.sprites()]

        change_armada_direction(self.space_invaders)

        expected_direction = original_direction * -1
        expected_y_values = [y + self.space_invaders.settings.armada_drop_speed for y in original_y_values]

        self.assertEqual(self.space_invaders.settings.armada_direction, expected_direction)

        for invader, expected_y in zip(self.space_invaders.invaders.sprites(), expected_y_values):
            self.assertEqual(invader.rect.y, expected_y)


