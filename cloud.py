import pygame
from pygame.sprite import Sprite
import random

clouds = [pygame.image.load("Images/cloud1.png"), pygame.image.load("Images/cloud2.png"), pygame.image.load("Images/cloud4.png"), pygame.image.load("Images/cloud6.png"), pygame.image.load("Images/cloud7.png")] # Loads the images

class Cloud(Sprite):
    def __init__(self, settings, screen, x, y):
        super(Cloud, self).__init__()  # Needed to make Groups()
        self.settings = settings
        self.screen = screen
        self.state = 0
        self.image = clouds[self.state].copy()
        self.speed = random.randint(10, 15)/10
        alpha = random.randint(200, 255)
        self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self.id = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.original_x = x

    def blit(self):
        self.rect.x -= self.speed
        if (self.rect.x + self.rect.width < 1):
            self.rect.x = self.original_x + random.randint(-150, 150)
            self.state = 0

        if (random.randint(0, 1000) > 998):
            if (self.state < 4):
                self.state += 1
            self.image = clouds[self.state].copy()
            alpha = 255 - self.state * 48
            self.image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        self.rect.y += random.randint(-1, 1)
        self.screen.blit(self.image, self.rect)
