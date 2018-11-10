from brain import Brain
import pygame


class Bot:
    def __init__(self, screen, settings):
        self.brain = Brain()
        self.brain.setBrain()
        self.id = 10

        self.screen = screen
        self.settings = settings

        self.movementRight = True

        self.jump = False
        self.allowJump = True
        self.timer = 0 # this if to give the jump a bit of a buffer
        self.baseJump = settings.screenHeight

        self.collideRight = False
        self.collideBottom = False

        self.image = pygame.image.load("Images/player.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 50, self.settings.screenHeight - self.rect.bottom - 50
        self.rect.x, self.rect.y = self.x, self.y

    def evolve(self):
        self.brain.evolve()

    def chooseInput(self, data, item):
        nodeNum = 0
        weight = 0
        chooseNode = 0
        if len(self.brain.nodes) > 0:
            for node in self.brain.nodes:
                tempDis, tempItem, tempInput = node
                if data != "none":
                    point1 = tempDis - data
                    if point1 < 0:
                        point1 * -1
                    tempWeight = 350 - point1
                    if tempItem == item:
                        tempWeight *1.5
                    if tempWeight > weight:
                        weight = tempWeight
                        chooseNode = nodeNum
                else:
                    tempWeight = 100
                    chooseNode = nodeNum
                    if tempWeight > weight:
                        weight = tempWeight
                        chooseNode = nodeNum
                nodeNum += 1
        idealDis, idealItem, botInput = self.brain.nodes[chooseNode]
        if botInput == 0:
            pass
        elif botInput == 1:
            print("jump")
        print("Node: " + str(chooseNode))

    def update(self):
        if self.movementRight == True:
            self.x += .5

        self.rect.x = self.x

    def blit(self):
        self.screen.blit(self.image, self.rect)