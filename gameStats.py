class GameStats():
    def __init__(self):

        #Timer Data
        self.timer = 0
        self.timerAdd = 0

        # Number Dead and Gen number
        self.death = 0
        self.gen = 0

        #Screen Roll Data
        self.screen_roll = False
        self.screen_bot_roll = False
        self.screen_roll_back = False
        self.xShift = 0

        #Game Pause
        self.pause = False

    def addTimer(self, extraTime):
        if extraTime > self.timerAdd:
            self.timerAdd = extraTime

    def nextGen(self):
        self.timer = 0
        self.timerAdd = 0
        self.death = 0
        self.gen += 1
