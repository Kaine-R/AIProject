from brain import Brain
import pygame


class Bot:
    def __init__(self, screen, settings):
        self.brain = Brain()
        self.brain.setBrain()
        self.id = 1
        self.score = 0
        self.dead = False

        self.life = 1
        self.color =(0, 0, 0)

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

    def chooseInput(self, data, item):  #temp variables are node info, base values are whats actually seen by bot
        if item == -1:
            chooseNode = 0
        else:
            weight = 400
            for i in range(len(self.brain.nodes)):
                tempDis, tempItem, tempInput = self.brain.nodes[i]
                tempWeight = abs(tempDis - data)
                if tempItem != item:
                    tempWeight += 100
                if round(tempDis) == round(data):
                    tempWeight -= 20
                if tempWeight < weight:
                    weight = tempWeight
                    chooseNode = i


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
        print("Node: " + str(chooseNode) + "/" + str(len(self.brain.nodes)-1), end='')
        print(", Dis: " + str(data), end='')
        if item == 0:
            tempText = "Box"
        elif item == 1:
            tempText = "Spike"
        else:
            tempText = "Nothing #" + str(item)
        print("  Item: " + tempText + ", ")
        print("-----------")

    def update(self):
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

        self.rect.x, self.rect.y = self.x, self.y

        if self.collideBottom == False:
            self.y += 1.5
        if self.movementRight == True:
            self.score += 1
            self.x += .75

        self.jump = False
        self.movementRight = True

        self.rect.x, self.rect.y = self.x, self.y
        self.colorRect.x, self.colorRect.y = self.x + 5, self.y + 15

    def blit(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, self.color, self.colorRect)

    def printBrain(self):
        self.brain.print()

    def reset(self):
        self.dead = False
        self.score = 0
        self.x, self.y = 50, self.settings.screenHeight - 90
        self.rect.x, self.rect.y = self.x, self.y

    def resetLife(self):
        self.life = 0

    def increaseLife(self):
        self.life += 1
        if self.life <= 5:
            self.color = (self.life*50, self.life*50, self.life*50)
        elif self.life <= 10:
            self.color = (255, self.life%5*30, self.life%5*30)
        elif self.life <= 15:
            self.color = (self.life%5*30, self.life%5*30, 255)
        else:
            self.color = (self.life%5*20, 255, self.life%5*20)


