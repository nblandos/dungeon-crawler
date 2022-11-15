import pygame
from settings import *


class EntityAnimation:
    def __init__(self, entity):
        self.entity = entity
        self.direction = self.entity.direction
        self.animation_frame = 0
        self.states = ['idle', 'run']
        self.frames_dict = self.load_frames_dict()

    def load_frames_dict(self):
        frames_dict = {"IDLE": [], "RUN": []}
        for state in self.states:
            for i in range(4):
                frame = pygame.image.load(f'{self.entity.path}_{state}_anim_f{i}.png').convert_alpha()
                frame = pygame.transform.scale(frame, (TILE_SIZE, PLAYER_HEIGHT))
                frames_dict[state.upper()].append(frame)
        return frames_dict

    def update_animation_frame(self):
        self.animation_frame += 0.1
        if self.animation_frame >= 4:
            self.animation_frame = 0

    def player_animation(self, state):
        self.update_animation_frame()
        if self.entity.direction == 'right':
            self.entity.image = self.frames_dict[state][int(self.animation_frame)]
        elif self.entity.direction == 'left':
            self.entity.image = pygame.transform.flip(self.frames_dict[state][int(self.animation_frame)], True, False)

    def animation(self):
        if self.entity.velocity == [0, 0]:
            self.player_animation('IDLE')
        elif self.entity.velocity != [0, 0]:
            self.player_animation('RUN')

    def update(self):
        self.animation()
