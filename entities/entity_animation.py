import pygame
from settings import *


class EntityAnimation:
    def __init__(self, entity):
        self.entity = entity
        self.direction = self.entity.direction
        self.animation_frame = 0  # The current frame of the animation
        self.states = ['idle', 'run']  # List of possible states
        self.frames_dict = self.load_frames_dict() # Loads the animation images for the entity

    def load_frames_dict(self):
        # Returns a dictionary of every image frame for different states
        frames_dict = {"IDLE": [], "RUN": []}
        for state in self.states:
            for i in range(4):
                frame = pygame.image.load(f'{self.entity.path}_{state}_anim_f{i}.png').convert_alpha()
                frame = pygame.transform.scale(frame, (TILE_SIZE, PLAYER_HEIGHT))
                frames_dict[state.upper()].append(frame)
        return frames_dict

    def update_animation_frame(self):
        # Cycles through the animation frames
        self.animation_frame += 0.1
        if self.animation_frame >= 4:
            self.animation_frame = 0

    def animation(self, state):
        self.update_animation_frame()
        # Sets the animation frame to the correct image based on the state and direction
        # If the entity was moving left, the image is flipped
        if self.entity.direction == 'right':
            self.entity.image = self.frames_dict[state][int(self.animation_frame)]
        elif self.entity.direction == 'left':
            self.entity.image = pygame.transform.flip(self.frames_dict[state][int(self.animation_frame)], True, False)

    def update(self):
        # Checks what state the entity is in and plays the correct animation
        if self.entity.velocity == [0, 0]:
            self.animation('IDLE')
        elif self.entity.velocity != [0, 0]:
            self.animation('RUN')

