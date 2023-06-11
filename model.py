from Bullets.Bomb import Bomb


def fire_bomb(self):
    # Проверка на 3 заряда
    if self.stats.bombs_left > 0:
        self.stats.bombs_left -= 1
        self.score_table.prep_bombs()
    elif self.stats.bombs_left == 0:
        return

    new_bomb = Bomb(self)
    self.bomb.add(new_bomb)


def change_mystery_ship_direction(self):
    self.mystery_ship.rect.y += self.settings.armada_drop_speed
    self.settings.armada_direction *= -1


def change_armada_direction(self):
    for invader in self.invaders.sprites():
        invader.rect.y += self.settings.armada_drop_speed
    self.settings.armada_direction *= -1
