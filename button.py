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
        self.images.append(pygame.image.load(f'assets/buttons/{self.path}/{self.name} Button.png'))
        self.images.append(pygame.image.load(f'assets/buttons/{self.path}/{self.name} col_Button.png'))
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i],
                                                    (self.images[i].get_width() / 1.4,
                                                     self.images[i].get_height() / 1.4))

    def action(self):
        pass

    def draw(self):
        self.menu.game.screen.blit(self.image, self.rect)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.images[1]
            if pygame.mouse.get_pressed()[0] == 1:
                self.action()
        else:
            self.image = self.images[0]


class PlayButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'Large Buttons', 'Play', x, y)

    def action(self):
        self.menu.running = False


class SettingsButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'Large Buttons', 'Settings', x, y)

    def action(self):
        pass


class QuitButton(Button):
    def __init__(self, menu, x, y):
        super().__init__(menu, 'Large Buttons', 'Quit', x, y)

    def action(self):
        self.menu.game.running = False
        self.menu.running = False
