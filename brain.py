import random

class Brain():
    def __init__(self):
        self.nodes = []
        self.nodeLimit = 5
        self.info = ()


    def setBrain(self):
        idealDistance = random.randint(0, 350)
        rand = random.randint(-1, 1)
        idealItem = [rand]
        if random.randint(0, 4) == 0:
            tempRand = random.randint(-1, 1)
            if rand != tempRand:
                idealItem.append(tempRand)
        if random.randint(0, 1) == 0:
            botInput = 0
        else:
            botInput = 1
        self.info = (idealDistance, idealItem, botInput)
        self.nodes.append(self.info)

    def evolve(self):
        choices = 2
        choose = random.randint(0, choices-1)
        if choose == 0: # add node
            if len(self.nodes) < self.nodeLimit:
                idealDistance = random.randint(0, 350)
                rand = random.randint(-1, 1)
                idealItem = [rand]
                if random.randint(0, 4) == 0:
                    tempRand = random.randint(-1,1)
                    if rand != tempRand:
                        idealItem.append(tempRand)
                if random.randint(0, 1) == 0:
                    botInput = 0
                else:
                    botInput = 1
                self.info = (idealDistance, idealItem, botInput)
                self.nodes.append(self.info)
        elif choose == 1: # evolve a node (change a few values)
            if len(self.nodes) > 0:
                chooseNode = random.randint(0, len(self.nodes))
                idealDistance, idealItem = self.nodes[chooseNode]
                if random.randint(0, 1):
                    if random.randint(0, 1) == 0:
                        idealDistance -= random.randint(0, 50)
                        if idealDistance < 0:
                            idealDistance = 0
                    else:
                        idealDistance += random.randint(0, 50)
                        if idealDistance > 350:
                            idealDistance = 350
                else:
                    if len(idealItem) == 0:
                        idealItem[0] = random.randint(-1, 1)
                    elif len(idealItem) == 1:
                        if random.randint(0, 3) == 0:
                            rand = random.randint(-1, 1)
                            if rand != idealItem[0]:
                                idealItem.append(rand)
                        else:
                            idealItem[0] = random.randint(-1, 1)
                    else:
                        if random.randint(0, 3) != 0:
                            idealItem.pop(random.randint(0, len(idealItem)))
                        else:
                            print("EVO: idealItems >=2 no funtion")

    def printNodes(self):
        for node in self.nodes:
            print(node)