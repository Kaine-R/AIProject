import pygame
from pygame.sprite import Sprite

class Baddie(Sprite):
    def __init__(self, screen, settings):
        super(Baddie, self).__init__()
        self.screen, self.settings = screen, settings

        self.image = pygame.image.load("Images/Enemy1.png")
        self.rect = self.image.get_rect()

        self.direction = 0

    def update(self):
        if self.direction == 0:
            self.rect.x += self.settings.enemySpeed
        else:
            self.rect.x -= self.settings.enemySpeed

    def blit(self):
        self.screen.blit(self.image, self.rect)