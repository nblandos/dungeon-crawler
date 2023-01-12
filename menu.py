import pygame
import sys
from settings import *
from button import PlayButton, QuitButton, ResumeButton, MenuButton


class Menu:
    def __init__(self, game, title_text):
        self.game = game
        self.running = False
        self.title = pygame.font.Font(FONT, 140).render(title_text, True, WHITE)

    def draw_buttons(self):
        pass

    def input(self):
        # Checks for user inputs in the menu screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.game.pause_menu.running:
                    self.running = False

    def draw(self):
        # Draws the menu screen
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title, ((WIDTH - self.title.get_width()) / 2, 50))
        self.draw_buttons()

    def update(self):
        pass

    def show(self):
        # Main menu loop that is called every frame
        while self.running:
            self.input()
            self.draw()
            self.update()
            self.game.clock.tick(FPS)
            self.game.display.blit(self.game.screen, (0, 0))
            pygame.display.flip()


class MainMenu(Menu):
    title_text = "Roguelike NEA"

    def __init__(self, game):
        Menu.__init__(self, game, self.title_text)
        self.running = True
        # Creates the buttons
        self.play_button = PlayButton(self, WIDTH / 2, 4 * TILE_SIZE)
        self.quit_button = QuitButton(self, WIDTH / 2, 8 * TILE_SIZE)

    def draw_buttons(self):
        # Draws the menu screen
        self.play_button.draw()
        self.quit_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.play_button.update()
        self.quit_button.update()


class PauseMenu(Menu):
    title_text = "PAUSED"

    def __init__(self, game):
        Menu.__init__(self, game, self.title_text)
        # Creates the buttons
        self.resume_button = ResumeButton(self, WIDTH / 2, 4 * TILE_SIZE)
        self.menu_button = MenuButton(self, WIDTH / 2, 8 * TILE_SIZE)

    def draw_buttons(self):
        # Draws the menu screen
        self.resume_button.draw()
        self.menu_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.resume_button.update()
        self.menu_button.update()
