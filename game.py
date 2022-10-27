import pygame
import sys
from settings import *
from entities.player import Player
pygame.init()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = pygame.Surface((WIDTH, HEIGHT)).convert()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.running = True

    def refresh(self):
        self.__init__()
        self.run()

    def update_groups(self):
        self.player.update()

    def draw_groups(self):
        self.player.draw(self.screen)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.player.input()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            self.refresh()

    def run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.update_groups()
            self.draw_groups()
            self.input()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

