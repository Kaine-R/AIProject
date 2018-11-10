import pygame
from pygame.sprite import Sprite


class Spike(Sprite):
    def __init__(self, settings, screen):
        super(Spike, self).__init__()
        self.image = pygame.image.load("Images/spike.png")
        self.rect = self.image.get_rect()
        self.id = 1
        
        self.settings = settings
        self.screen = screen