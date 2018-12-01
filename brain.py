import random

class Brain():
    def __init__(self):
        self.nodes = []
        self.nodeLimit =6
        self.info = ()



    def setBrain(self):
        idealDistance = random.randint(0, 350)
        idealItem = random.randint(-1, 1)
        botInput = random.randint(0, 3)
        self.info = (idealDistance, idealItem, botInput)
        self.nodes.append(self.info)

    def evolve(self):
        choices = 3
        choose = random.randint(0, choices * 10)

        if len(self.nodes) < 3:
            choose = 5
        elif len(self.nodes) > 5:
            choose = 10

        if choose <= 5: # add node ==============================================================
            if len(self.nodes) < self.nodeLimit:

                idealDistance = random.randint(0, 350)
                idealItem = random.randint(-1, 1)
                botInput = random.randint(0, 3)
                self.info = (idealDistance, idealItem, botInput)
                self.nodes.append(self.info)

        elif choose <= 10: # remove a Node ===========================================================
            if len(self.nodes) > 0:
                self.nodes.pop(random.randint(0, len(self.nodes) -1))

        elif choose <= 25: # evolve a node (change a few values) ============================================
            if len(self.nodes) > 0:
                chooseNode = random.randint(0, len(self.nodes) -1)
                idealDistance, idealItem, idealInput = self.nodes[chooseNode]
                randint = random.randint(0, 10)

                if randint < 6:
                    if random.randint(0, 1) == 0:
                        idealDistance -= random.randint(0, 50)
                        if idealDistance < 0:
                            idealDistance = 0
                    else:
                        idealDistance += random.randint(0, 50)
                        if idealDistance > 350:
                            idealDistance = 350
                elif randint < 8:
                    idealItem = random.randint(-1, 1)
                else:
                    idealInput = random.randint(0, 3)

                self.nodes[chooseNode] = (idealDistance, idealItem, idealInput)


        else: # ================================================================================
            pass

