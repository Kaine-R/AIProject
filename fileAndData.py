class File():
    def __init__(self): # 0 is blocks, 1 is spikes, 2 is else
        self.info = []

    def addData(self, data):
        self.info.append(data)



# SAVE / LOAD TO FILE -------------------------------------------------

    def save(self):
        self.file = open("data.txt", "w")
        if self.file.mode == "w":
            for i in range(len(self.info)):
                self.file.write(str(self.info[i]) + "\n")

        self.file.close()

    def load(self):
        self.file = open("data.txt", "r")
        temp = ""
        item = ""
        switch = False

        if self.file.mode == "r":
            lines = self.file.readlines()
            for line in lines:
                for char in line:
                    if char != "\n":
                        temp += char
                        if switch == True:
                            if char != ")":
                                char += item
                            else:
                                switch = False
                        if char == " ":
                            switch = True

                if item == "0":
                    self.dataB.append(temp)
                elif item == "1":
                    self.dataS.append(temp)
                else:
                    print("Error Reading")
