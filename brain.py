import random

class Brain():
    def __init__(self):
        self.nodes = []
        self.nodeLimit =6
        self.info = ()

    def setBrain(self):
        idealDistance = random.randint(0, 250)  # Ideal distance for particular input
        idealItem = random.randint(0, 1)        # Ideal Item that makes a input more likely to take
        botInput = random.randint(0, 2)         # Input can be walk, jump or stop
        self.info = (idealDistance, idealItem, botInput)
        self.nodes.append((370, -1, 0))  # chooses an action when nothing is detected
        self.nodes.append(self.info)                        # chooses an action when anything is detected

    def print(self):
        for i in range(len(self.nodes)):
            Dis, Item, Input = self.nodes[i]
            print("# " + str(i) + ": ", end='')
            print("(Dis: " + str(Dis) + ", ", end='')
            if Item == 0:
                tempText = "Box"
            elif Item == 1:
                tempText = "Spike"
            else:
                tempText = "Nothing"
            print("Item: " + tempText + ", ", end='')
            if Input == 0:
                tempText = "Walk"
            elif Input == 1:
                tempText = "Jump"
            elif Input == 2:
                tempText = "Stop"
            else:
                tempText = "Other #" + str(Input)
            print("Input: " + tempText + ")   ")

    def evolve(self):
        choices = 3
        choose = random.randint(0, (choices * 10))

        if len(self.nodes) < 3: # If node (brain) is less than 3 then make more nodes
            choose = 5
        elif len(self.nodes) > self.nodeLimit: # If node (brain) is at hit the max then delete a random node
            choose = 10

        if choose <= 5: # add node ==============================================================
            if len(self.nodes) < self.nodeLimit:

                idealDistance = random.randint(0, 250)
                idealItem = random.randint(0, 1)
                botInput = random.randint(0, 2)
                self.info = (idealDistance, idealItem, botInput)
                self.nodes.append(self.info)

        elif choose <= 10: # remove a Node ===========================================================
            if len(self.nodes) > 2:
                self.nodes.pop(random.randint(1, len(self.nodes) -1))

        elif choose <= 25: # evolve a node (change a few values) ============================================
            if len(self.nodes) > 0:
                chooseNode = random.randint(0, len(self.nodes) -1)
                idealDistance, idealItem, idealInput = self.nodes[chooseNode]
                randint = random.randint(0, 11)

                if randint < 6:
                    if random.randint(0, 1) == 0:
                        idealDistance -= random.randint(0, 50)
                        if idealDistance < 0:
                            idealDistance = 0
                    else:
                        idealDistance += random.randint(0, 50)
                        if idealDistance > 250:
                            idealDistance = 250
                elif randint < 8:
                    if idealItem != -1:
                        idealItem = random.randint(0, 1)
                else:
                    idealInput = random.randint(0, 2)

                self.nodes[chooseNode] = (idealDistance, idealItem, idealInput)


        else: # ================================================================================
            pass
