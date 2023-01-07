import pygame
import sys
from settings import *
from button import PlayButton, QuitButton


class Menu:
    def __init__(self, game):
        self.game = game
        self.running = True
        self.title = pygame.font.Font(FONT, 140).render("Roguelike NEA", True, WHITE)
        # Creates the buttons
        self.play_button = PlayButton(self, 10.5 * TILE_SIZE, 4 * TILE_SIZE)
        self.quit_button = QuitButton(self, 10.5 * TILE_SIZE, 8 * TILE_SIZE)

    def input(self):
        # Checks for user inputs in the menu screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw(self):
        # Draws the menu screen
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title, (6.5 * TILE_SIZE, 50))
        self.play_button.draw()
        self.quit_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.play_button.update()
        self.quit_button.update()

    def show(self):
        # Main menu loop that is called every frame
        while self.running:
            self.input()
            self.draw()
            self.update()
            self.game.clock.tick(FPS)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()

