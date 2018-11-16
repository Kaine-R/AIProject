import pygame


class Text():
    def __init__(self, screen, settings, msg, size, x, y):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.SysFont(None, size, False, False)

        self.prep(msg, x, y)

    def prep(self, msg, x, y):
        self.image = self.font.render(msg, True, (250, 250, 250))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def blit(self):
        self.screen.blit(self.image, self.rect)