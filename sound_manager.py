import pygame


class SoundManager:
    def __init__(self, game):
        self.game = game
        self.path = 'assets/sounds/'
        self.sounds = {
            'player_shoot': pygame.mixer.Sound(f'{self.path}Weapon 1.wav')
        }

    def play_sound(self, sound):
        pygame.mixer.Sound.play(sound)
