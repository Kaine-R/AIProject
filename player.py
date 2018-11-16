import pygame
import math


class Player:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.id = 0

        self.movementLeft = False
        self.movementRight = False

        self.jump = False
        self.allowJump = True
        self.timer = 0 # this if to give the jump a bit of a buffer
        self.baseJump = settings.screenHeight

        self.collideRight = False
        self.collideLeft = False
        self.collideBottom = False

        self.image = pygame.image.load("Images/player.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 50, self.settings.screenHeight - self.rect.bottom - 50
        self.rect.x, self.rect.y = self.x, self.y

    def updatePlayer(self, map):  # Controls moving the character based on key presses
        if self.jump:  # This should only happen during jump function in gf
            self.y -= self.settings.playerSpeed * 2 - ((self.baseJump-55 - self.rect.y) / (self.settings.jumpLimit +0))*2 # jump formula don't touch (slows jump speed near top of arc)
        elif self.collideBottom == False:
            self.y += self.settings.playerSpeed * 2
        if self.movementLeft == True and self.collideLeft == False: # If left arrow key is pressed and not touching block to the left
            self.x -= self.settings.playerSpeed
        if self.movementRight == True and self.collideRight == False:# If right arrow key is pressed and not touching block to the right
            self.x += self.settings.playerSpeed

        self.rect.x, self.rect.y = self.x, self.y


    def drawPlayer(self):
        self.screen.blit(self.image, self.rect)

    def reset(self):
        self.x = 50
        self.y = self.settings.screenHeight - 100
