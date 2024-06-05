import pygame


class Button:
    def __init__(self, menu, path, name, x, y):
        self.menu = menu
        self.name = name
        self.path = path
        self.images = []
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)

    def load_images(self):
        # Load the images for the button
        self.images.append(pygame.image.load(
            f'assets/buttons/{self.path}/{self.name} Button.png'))
        self.images.append(pygame.image.load(
            f'assets/buttons/{self.path}/{self.name} col_Button.png'))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],
                                                    (self.images[i].get_width() / 1.2,
                                                     self.images[i].get_height() / 1.2))

    def action(self):
        # This method is overwritten in the subclasses
        pass

    def draw(self):
        # Draws the button
        self.menu.game.screen.blit(self.image, self.rect)

    def update(self):
        # Checks if the button is hovered over and changes the image accordingly
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[1]
            if pygame.mouse.get_pressed()[0] == 1:
                self.action()
        else:
            self.image = self.images[0]


class PlayButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Large Buttons', 'Play', x, y)

    def action(self):
        self.menu.running = False
        pygame.mixer.music.play(-1)


class HighscoreButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Large Buttons', 'Highscores', x, y)

    def action(self):
        self.menu.running = False
        self.menu.game.highscore_menu.running = True


class QuitButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Large Buttons', 'Quit', x, y)

    def action(self):
        self.menu.game.running = False
        self.menu.running = False


class ResumeButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Large Buttons', 'Resume', x, y)

    def action(self):
        pygame.mixer.music.unpause()
        self.menu.running = False


class MenuButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Large Buttons', 'Menu', x, y)

    def action(self):
        self.menu.running = False
        self.menu.game.restart()


class BackButton(Button):
    def __init__(self, menu, x, y):
        # Inherits from the Button class
        super().__init__(menu, 'Square Buttons', 'Back', x, y)

    def action(self):
        self.menu.running = False
        self.menu.game.main_menu.running = True
