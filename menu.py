import pygame
import sys
from settings import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('assets/fonts/main_font.ttf', 140)
        self.running = True
        self.title = self.font.render("Roguelike NEA", True, WHITE)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:  # skip menu for testing purposes
            self.running = False

    def draw(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title, (6.5 * TILE_SIZE, 50))

    def show(self):
        while self.running:
            self.input()
            self.draw()
            self.game.clock.tick(FPS)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()

class Button:
    def __init__(self, menu, name, x, y):
        self.menu = menu
        self.name = name
        self.image = pygame.image.load(f'assets/buttons/{self.name}.png')
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        self.clicked = False

    def draw(self):
        self.menu.game.screen.blit(self.image, self.rect)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
            else:
                self.clicked = False


class PlayButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'play', x, y)


class SettingsButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'settings', x, y)


class QuitButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'quit', x, y)



