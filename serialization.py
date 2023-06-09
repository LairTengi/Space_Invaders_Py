import pickle
import sys

import pygame


def graceful_shutdown(self):
    save_stats(self)
    pygame.mixer.music.stop()
    sys.exit(0)


def save_stats(self):
    serialized_data = pickle.dumps(self.stats.high_score)
    with open('data.pickle', 'wb') as file:
        file.write(serialized_data)


def load_stats(self):
    try:
        with open('data.pickle', 'rb') as file:
            loaded_data = pickle.load(file)
        self.stats.high_score = int(loaded_data)
    except:
        pass