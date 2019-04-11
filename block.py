import pygame
from pygame.sprite import Sprite

class Block(Sprite):
    def __init__(self, settings, screen, xnum = 1, ynum = 1, imageNum = 0): # default num is 1 if nothing is passed
        super(Block, self).__init__() # Needed to make Groups()
        self.settings = settings
        self.screen = screen
        self.id = 0
        if imageNum == 0:
            self.image = pygame.image.load("Images/block1.png")  # Loads Default image (rocks)
        else:
            self.image = pygame.image.load("Images/block0.png")  # Loads the image (dirt)

        self.makeBig(xnum, ynum) # if num 1 is passed then block is double the size

    def makeBig(self, xnum, ynum):
        self.image = pygame.transform.scale(self.image, (xnum*50, ynum*50))
        self.rect = self.image.get_rect()

    def blit(self):
        self.screen.blit(self.image, self.rect)