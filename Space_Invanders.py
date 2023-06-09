import pygame

from models.Mystery_ship import MysteryShip
from Stats.Settings import Settings
from models.Ship import Ship
from Stats.GameStatistics import GameStats
from Stats.ScoreTable import ScoreTable
from Buttons.Button import Button
from controller import check_events
from serialization import load_stats
from view import update_invaders, update_bullets, update_bomb, update_screen, create_armada, update_mystery_ship


class SpaceInvaders:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders")
        self.background_image = pygame.image.load('images/background.jpg')

        self.ship = Ship(self)
        self.mystery_ship = MysteryShip(self)

        # Группа для управления спрайтами
        self.bullets = pygame.sprite.Group()
        self.invaders = pygame.sprite.Group()
        self.bomb = pygame.sprite.Group()

        create_armada(self)

        # Игровая статистика
        self.stats = GameStats(self)
        self.score_table = ScoreTable(self)

        # Кнопка Play
        self.play_button = Button(self, "Play")

        self.FIRST_GAME = True
        self.MYSTERY = False
        # Три хита у mystery_ship
        self.coll_mystery_ship = 3

    def run_game(self):
        load_stats(self)  # Загрузка сериализованных объектов
        while True:
            check_events(self)
            if self.stats.game_active:
                self.ship.update()
                update_bullets(self)
                if self.MYSTERY == True:
                    update_mystery_ship(self)
                else:
                    update_invaders(self)
                update_bomb(self)

            update_screen(self)


if __name__ == "__main__":
    ai = SpaceInvaders()
    ai.run_game()
