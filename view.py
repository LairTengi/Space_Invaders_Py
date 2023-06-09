import time

import pygame

from models.Invader import Invader
from Bullets.Bullet import Bullet
from models.Mystery_ship import MysteryShip
from model import change_armada_direction, change_mystery_ship_direction


# Поведение и создание обычных пришельцев
def create_invader(self, invader_number, row_number):
    invader = Invader(self)
    invader_width, invader_height = invader.rect.size
    invader.x = invader_width + 2 * invader_width * invader_number
    invader.rect.x = invader.x
    invader.rect.y = invader.rect.height + 2 * invader.rect.height * row_number
    self.invaders.add(invader)


def create_armada(self):
    invader = Invader(self)
    invader_width, invader_height = invader.rect.size
    available_space_x = self.settings.screen_width - (2 * invader_width)
    numbers_of_invaders = available_space_x // (2 * invader_width)

    ship_height = self.ship.rect.height
    available_space_y = (self.settings.screen_height - (3 * invader_height) - ship_height)
    numbers_rows = available_space_y // (2 * invader_height)

    for row_number in range(numbers_rows):
        for invader_number in range(numbers_of_invaders):
            create_invader(self, invader_number, row_number)


def update_invaders(self):
    checks_armada_edges(self)
    self.invaders.update()
    # Если пришелец добрался до корабля - гг умер
    if pygame.sprite.spritecollideany(self.ship, self.invaders):
        ship_hit(self)
    # Если пришелец добрался до низа - гг умер
    check_invaders_bottom_collision(self)


def checks_armada_edges(self):
    for invader in self.invaders.sprites():
        if invader.check_edges():
            change_armada_direction(self)
            break


# Поведение и создание мистического корабля
def create_mystery_ship(self):
    self.mystery_ship = MysteryShip(self)


def checks_mystery_ship_edges(self):
    if self.mystery_ship.check_edges():
        change_mystery_ship_direction(self)


def check_mystery_ship_bottom_collision(self):
    screen_rect = self.screen.get_rect()
    if self.mystery_ship.rect.bottom >= screen_rect.bottom:
        ship_hit(self)


def fire_bullet(self):
    new_bullet = Bullet(self)
    self.bullets.add(new_bullet)


def update_bullets(self):  # Удаление вышедших за границы экрана пуль
    self.bullets.update()
    for bullet in self.bullets.copy():
        if bullet.rect.bottom <= 0:
            self.bullets.remove(bullet)
    if self.MYSTERY == True:
        check_mystery_ship_bullets_collision(self)
    else:
        check_bullet_invaders_collision(self)


def update_bomb(self):  # Удаление бомб за границами экрана
    self.bomb.update()
    for bomb in self.bomb.copy():
        if bomb.rect.bottom <= 0:
            self.bomb.remove(bomb)
    check_bullet_invaders_collision(self)


def check_mystery_ship_bullets_collision(self):
    collisions_m_ship = pygame.sprite.spritecollideany(self.mystery_ship, self.bullets)
    if collisions_m_ship:
        if self.coll_mystery_ship > 0:
            self.coll_mystery_ship -= 1
            collisions_m_ship.kill()
        else:
            self.mystery_ship.kill()
            self.stats.bombs_left += self.settings.bomb_limit
            self.score_table.prep_bombs()

            self.bullets.empty()
            create_armada(self)
            self.settings.increase_speed()  # Увеличение настроек игры

            self.stats.level += 1
            self.score_table.prep_level()
            self.mystery_ship.rect.x = 15
            self.mystery_ship.rect.y = 30
            self.coll_mystery_ship = 3


def check_bullet_invaders_collision(self):
    # Удаление снаряда и пришельца (коллизия между элементами)
    # Тут можно третьим аргументом передать False, чтобы снаряд не убивался об первого пришельца
    collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, True, True)
    collisions_bomb = pygame.sprite.groupcollide(self.bomb, self.invaders, False, True)

    # Тестовый залп
    # collisions = pygame.sprite.groupcollide(self.bullets, self.invaders, False, True)
    if collisions or collisions_bomb:
        self.stats.score += self.settings.invader_point
        self.score_table.prep_score()
        self.score_table.check_new_record()

    # Обновление флота при уничтожении всех пришельцев
    if not self.invaders:
        self.bullets.empty()
        create_armada(self)
        self.settings.increase_speed()  # Увеличение настроек игры

        self.stats.level += 1
        self.score_table.prep_level()


def check_invaders_bottom_collision(self):
    screen_rect = self.screen.get_rect()
    for invader in self.invaders.sprites():
        if invader.rect.bottom >= screen_rect.bottom:
            ship_hit(self)
            break


def update_screen(self):
    self.screen.blit(self.background_image, (0, 0))
    self.ship.blitMe()
    for bullet in self.bullets.sprites():
        bullet.draw_bullet()
    for bomb in self.bomb.sprites():
        bomb.draw_bomb()
    if self.stats.level % 5 == 0:
        self.MYSTERY = True
        self.mystery_ship.draw(self.screen)
    else:
        self.MYSTERY = False
        self.invaders.draw(self.screen)

    if not self.stats.game_active:
        self.play_button.draw_button()

    # Отображение статистик на экране
    self.score_table.show_life()
    self.score_table.show_score()
    pygame.display.flip()


def update_mystery_ship(self):
    checks_mystery_ship_edges(self)
    self.mystery_ship.update()

    # Если мистический корабль добрался до корабля - гг умер
    if self.mystery_ship.rect.colliderect(self.ship.rect):
        self.MYSTERY = False
        self.mystery_ship.kill()
        self.stats.level += 1
        self.score_table.prep_level()
        self.mystery_ship.rect.x = 15
        self.mystery_ship.rect.y = 30
        ship_hit(self)
    # Если мистический корабль добрался до низа - гг умер
    check_mystery_ship_bottom_collision(self)


def checks_mystery_ship_edges(self):
    if self.mystery_ship.check_edges():
        change_mystery_ship_direction(self)


def ship_hit(self):
    if self.stats.ships_left > 0:
        self.stats.ships_left -= 1
        self.score_table.prep_life()

        self.invaders.empty()
        self.bullets.empty()

        create_armada(self)
        self.ship.center_ship()

        time.sleep(0.5)
    else:
        self.stats.game_active = False
        self.FIRST_GAME = True


def prepare_game(self):
    if not self.stats.game_active:
        pygame.mixer.music.load('music/test.mp3')
        self.settings.initialize_dynamic_settings()  # Сброс игровых настроек
        self.stats.reset_stats()  # Сброс игровой статистики
        self.stats.game_active = True

        self.score_table.prep_score()
        self.score_table.prep_level()
        self.score_table.prep_life()
        self.score_table.prep_bombs()
        self.score_table.prep_high_score()

        self.invaders.empty()
        self.bullets.empty()
        create_armada(self)
        self.ship.center_ship()
