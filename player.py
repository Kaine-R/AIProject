import pygame
import math


class Player:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        self.movementLeft = False
        self.movementRight = False
        self.drop = True
        self.baseJump = 0
        self.landed = True
        
        self.collideRight = False
        self.collideLeft = False
        self.collideBottom = False

        self.image = pygame.image.load("Images/player.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 50, self.settings.screenHeight - self.rect.bottom - 50
        self.rect.x, self.rect.y = self.x, self.y

    def updatePlayer(self, map):  # Controls moving the character based on key presses
        if self.drop == False:  # This should only happen during jump fuction in gf
            self.y -= self.settings.playerSpeed * 2
            # This section is for slowing down the jump animation near the top of the arc (still a bit rough)
        elif self.drop == True and self.collideBottom == False:
            if self.baseJump - self.rect.bottom > 2 * self.settings.jumpLimit/5:
                self.y += self.settings.playerSpeed * .9
            elif self.baseJump - self.rect.bottom > 5 * self.settings.jumpLimit/6:
                self.y += self.settings.playerSpeed * .5
            else:
                self.y += self.settings.playerSpeed * 1.6
            # End of jump section
        if self.movementLeft == True and self.collideLeft == False: # If left arrow key is pressed and not touching block to the left
            self.x -= self.settings.playerSpeed
        if self.movementRight == True and self.collideRight == False:# If right arrow key is pressed and not touching block to the right
            self.x += self.settings.playerSpeed

        self.rect.x, self.rect.y = self.x, self.y
        self.currentRow = int(math.ceil((self.rect.bottom + 1)/50))


    def drawPlayer(self):
        self.screen.blit(self.image, self.rect)