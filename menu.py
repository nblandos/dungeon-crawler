import pygame
import sys
import sqlite3
from settings import *
from button import PlayButton, QuitButton, ResumeButton, MenuButton, BackButton, HighscoreButton


class Menu:
    def __init__(self, game, title_text):
        self.game = game
        self.running = False
        self.title = pygame.font.Font(FONT, 140).render(title_text, True, WHITE)
        self.username_text = pygame.font.Font(FONT, 50).render("User-" + game.username, True, WHITE)

    def draw_contents(self):
        pass

    def input(self):
        # Checks for user inputs in the menu screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game.pause_menu.running:
                        self.running = False
                    elif self.game.highscore_menu.running:
                        self.running = False
                        self.game.main_menu.running = True

    def draw(self):
        # Draws the menu screen
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.title, ((WIDTH - self.title.get_width()) / 2, 50))
        self.game.screen.blit(self.username_text, (WIDTH - self.username_text.get_width() - 3, 3))
        self.draw_contents()

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
        self.play_button = PlayButton(self, WIDTH / 2, 3.5 * TILE_SIZE)
        self.highscore_button = HighscoreButton(self, WIDTH / 2, 6.5 * TILE_SIZE)
        self.quit_button = QuitButton(self, WIDTH / 2, 9.5 * TILE_SIZE)

    def draw_contents(self):
        # Draws the menu screen
        self.play_button.draw()
        self.highscore_button.draw()
        self.quit_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.play_button.update()
        self.highscore_button.update()
        self.quit_button.update()


class PauseMenu(Menu):
    title_text = "PAUSED"

    def __init__(self, game):
        Menu.__init__(self, game, self.title_text)
        # Creates the buttons
        self.resume_button = ResumeButton(self, WIDTH / 2, 4 * TILE_SIZE)
        self.menu_button = MenuButton(self, WIDTH / 2, 8 * TILE_SIZE)

    def draw_contents(self):
        # Draws the menu screen
        self.resume_button.draw()
        self.menu_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.resume_button.update()
        self.menu_button.update()


class HighscoreMenu(Menu):
    title_text = "Highscores"

    def __init__(self, game):
        Menu.__init__(self, game, self.title_text)
        # Connects to the database
        self.con = sqlite3.connect("users.db")
        self.cursor = self.con.cursor()
        # Retrieves the highscores
        self.highscores = self.retrieve_scores()
        # Creates the buttons
        self.back_button = BackButton(self, WIDTH / 10, 0.5 * TILE_SIZE)

    def retrieve_scores(self):
        self.cursor.execute("SELECT username, highscore FROM users ORDER BY highscore DESC LIMIT 5")
        return self.cursor.fetchall()

    def draw_scores(self):
        # Draws the highscores
        for i in range(len(self.highscores)):
            ranking_text = pygame.font.Font(FONT, 110).render(str(i + 1) + ".", True, WHITE)
            username_text = pygame.font.Font(FONT, 110).render(self.highscores[i][0], True, WHITE)
            score_text = pygame.font.Font(FONT, 110).render(str(self.highscores[i][1]), True, WHITE)
            self.game.screen.blit(ranking_text, (WIDTH / 6, HEIGHT / 4 + i * HEIGHT / 8))
            self.game.screen.blit(username_text, (WIDTH / 3, HEIGHT / 4 + i * HEIGHT / 8))
            self.game.screen.blit(score_text, (3 * WIDTH / 4, HEIGHT / 4 + i * HEIGHT / 8))

    def draw_contents(self):
        # Draws the menu screen
        self.draw_scores()
        self.back_button.draw()

    def update(self):
        # Updates the buttons on the menu screen (Checks if they are hovered over)
        self.back_button.update()
