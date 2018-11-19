from brain import Brain
import pygame


class Bot:
    def __init__(self, screen, settings):
        self.brain = Brain()
        self.brain.setBrain()
        self.id = 1
        self.score = 0
        self.dead = False

        self.color = (250, 150, 10)

        self.screen = screen
        self.settings = settings

        self.movementRight = True

        self.jump = False
        self.jumpNum = 0
        self.allowJump = True
        self.timer = 0 # this if to give the jump a bit of a buffer
        self.baseJump = settings.screenHeight

        self.collideLeft = False
        self.collideRight = False
        self.collideBottom = False

        self.image = pygame.image.load("Images/player.png")
        self.rect = self.image.get_rect()
        self.x, self.y = 50, self.settings.screenHeight - self.rect.bottom - 50
        self.rect.x, self.rect.y = self.x, self.y

        self.colorRect = pygame.Rect(self.x, self.y, 13, 17)


    def evolve(self):
        self.brain.evolve()

    def chooseInput(self, data, item):
        nodeNum = 0
        weight = 0
        chooseNode = 0

        if len(self.brain.nodes) > 0:
            tempwWeight = 0
            tempMult =1
            for node in self.brain.nodes:
                tempDis, tempItem, tempInput = node

                if tempItem == item:
                    tempMult += .3

                if tempDis == data:
                    tempMult += .2

                if item == -1:
                    tempWeight = 300
                else:
                    tempWeight = tempDis - data
                    if tempWeight < 0:
                        tempWeight = tempWeight * -1

                tempWeight = tempWeight * tempMult

                if tempWeight > weight:
                    weight = tempWeight
                    chooseNode = nodeNum
                nodeNum += 1

        idealDis, idealItem, botInput = self.brain.nodes[chooseNode]
        if botInput == 0:
            print("Walk")
        elif botInput == 1:
            self.jump = True
            print("Jump")
        elif botInput == 2:
            self.movementRight = False
            print("Stop")
        elif botInput == 3:
            self.movementRight = False
            self.jump = True
            print("Stop and Jump")

        print("ID: " + str(self.id))
        print("Node: " + str(chooseNode) + "/" + str(len(self.brain.nodes)))
        print("-----------")

    def update(self):
        if self.rect.x > self.score:
            self.score = self.rect.x

        if self.jump and self.collideBottom:
            self.y -= 10
            self.jump = False
            self.jumpNum = 1

        if self.jumpNum != 0:
            yShift = 5
            self.jumpNum += 1
            if self.jumpNum > 20:
                yShift -= 2.5
            if self.jumpNum > 25:
                yShift -= 1
            if self.jumpNum >= 43:
                self.jumpNum = 0
            self.y -= yShift

        if self.collideBottom == False:
            self.y += 1.5
        if self.movementRight == True:
            self.x += .75

        self.jump = False
        self.movementRight = True

        self.rect.x, self.rect.y = self.x, self.y
        self.colorRect.x, self.colorRect.y = self.x + 5, self.y + 15

    def blit(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, self.color, self.colorRect)

    def reset(self):
        self.dead = False
        self.score = 0
        self.x, self.y = 50, self.settings.screenHeight - 90
        self.rect.x, self.rect.y = self.x, self.y


    def colorChange(self):
        if self.id % 10 == 0:
            color = 250
        else:
            color = (int(((self.id % 10) * 25)))

        if self.id <= 10:
            self.color = (color, 50, 50)
        elif self.id <= 20:
            self.color = (50, color, 50)
        elif self.id <= 30:
            self.color = (50, 50, color)
