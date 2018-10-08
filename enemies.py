import pygame
from pygame.sprite import Sprite

class Baddie(Sprite):
    def __init__(self):
        super(Baddie, self).__init__()
        self.image = pygame.image.load("Images/Enemy1.png")
        