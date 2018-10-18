import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    def __init__(self, settings, screen):
        super(Block, self).__init__() # Needed to make Groups()
        self.image = pygame.image.load("Images/block1.png")  # Loads the image
        self.rect = self.image.get_rect()  # pygame function to return the width and height of the picture
        self.rect.x, self.rect.y = 50, 50  # Sets the default position of block at (50, 50)
        self.settings = settings
        self.screen = screen

    def blit(self):
        self.screen.blit(self.image, self.rect)