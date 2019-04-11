import pygame
from bot import Bot
from block import Block
from spike import Spike
import sys
import copy
from random import randint

# INITAL SET UP  --------------------------------------------------------------
def createBots(screen, settings, Bots):
    for i in range(settings.botMax):
        newBot = Bot(screen, settings)
        newBot.id = i + 1
        newBot.x += newBot.id * .5
        Bots.append(newBot)



# INPUTS BY USER (Events) ----------------------------------------------------------
def checkEvents(gameStats):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            checkDown(event, gameStats)
        elif event.type == pygame.KEYUP:
            checkUp(event, gameStats)

def checkDown(event, gameStats):
    if event.key == pygame.K_LEFT:
        gameStats.screen_roll_back = True
    elif event.key == pygame.K_RIGHT:
        gameStats.screen_roll = True
    elif event.key == pygame.K_SPACE:
        pass

def checkUp(event, gameStats):
    if event.key == pygame.K_LEFT:
        gameStats.screen_roll_back = False
    elif event.key == pygame.K_RIGHT:
        gameStats.screen_roll = False
    elif event.key == pygame.K_SPACE:
        if gameStats.pause == False:
            gameStats.pause = True
        else:
            gameStats.pause = False

# COLLISIONS -------------------------------------------------------------------
def checkCollide(bot, blocks, spikes):
    dead = False
    ground = False  # This is here to see if it's touching the ground, else it floats when walking off edge
    if objectsCollide(bot, spikes):
        botDead(bot)
        dead = True

    for block in blocks:
        if reduceCollisionCheck(bot, block):    # Returns True if objects are near bot
            if objectsCollide(bot, blocks):     # True if collision detected
                if checkDirection(bot, block):  # checks if any of the blocks that touch are below player
                    ground = True

    if bot.y + bot.rect.height > bot.settings.screenHeight:
        botDead(bot)
        bot.dead = True

    resetCollides(bot)
    if ground == False:
        bot.collideBottom = False

    return dead

def checkDirection(bot, block):
    below = False
    left = False
    right = False

    # This checks to see if the block is to the left or right
    if bot.rect.centerx <= block.rect.centerx:
        left = True
    elif bot.rect.centerx > block.rect.centerx:
        right = True
    if bot.rect.bottom - 5 <= block.rect.y:  # Checks to see if the block is below
        below = True

    if left and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit RIGHT")
        bot.collideRight = True
    if right and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit LEFT")
        bot.collideLeft = True
    if below:  # if any block is below then it counts as standing on something
        bot.collideBottom = True
        return True
    return False

def resetCollides(bot):  # If left or right collision is detected then it pushes player back and stops the collision
    if bot.collideRight:
        bot.x -= 1.5
        bot.score -= 2
        bot.collideRight = False
    elif bot.collideLeft:
        bot.x += 1.5
        bot.score -= 2
        bot.collideLeft = False

def objectsCollide(bot, objects): # works even when individual object
    for object in objects:
        if reduceCollisionCheck(bot, object):
            if pygame.sprite.collide_rect(bot, object):
                return True
    return False

def enemyBlockCollide(enemies, map):
    for block in map:
        for enemy in enemies:
            if pygame.sprite.collide_rect(enemy, block):
                if round(block.rect.bottom) >= round(enemy.rect.bottom):
                    if enemy.direction == 1:
                        enemy.direction = 0
                    else:
                        enemy.direction = 1

def enemyPlayerCollide(player, enemies):
        if pygame.sprite.spritecollide(player, enemies, False):
            player.reset()

def checkOnScreen(object): # if out of screen return False
    if object.rect.right < 0 or object.rect.left > object.settings.screenWidth:
        return False
    return True

def reduceCollisionCheck(bot, object):
    if object.rect.right > bot.rect.left - 55 and object.rect.left < bot.rect.right + 55:
        return True
    return False

# BOT FUNCTIONS ----------------------------------------------------------
def scanFront(bot, blocks, spikes):
    item = -1       # No item hit
    data = 450
    exit = False

    for dis in range(13):  # Can Mix the the and might save more time
        for block in blocks:
            if scanObject(block, bot, dis):
                if block.rect.x - bot.rect.x < data:
                    data = block.rect.x - bot.rect.right
                    item = 0
                    exit = True
                    break
        for spike in spikes:
            if scanObject(spike, bot, dis):
                if spike.rect.x - bot.rect.x < data:
                    data = spike.rect.x - bot.rect.right
                    item = 1
                    exit = True
                    break
        if exit:
            break

    return (data, item)

def scanObject(object, player, dis):
    if dis <= 10:
        scanHit = (player.rect.right + (dis * 21) + 15, player.y + player.rect.height / 2)
    else:
        scanHit = (player.x + player.rect.width + ((dis-10) * 35) + 225, player.y + player.rect.height / 2)

    if object.rect.collidepoint(scanHit):
        return True

    return False

def splitBots(Bots): # Gets all scores, orders them then gets rid of the worst bots based on those scores
    listScore = []
    if len(Bots) % 2 == 1:
        odd = 1
    else:
        odd = 0

    for i in range(int(len(Bots))): # Puts all the scores and indexes in a list
        if Bots[i].dead:
            Bots[i].score -= int(Bots[i].score/4)
        else:
            Bots[i].score -= 5
        listScore.append((Bots[i].score, i))

    listScore.sort(reverse=True) # sorts based on the second variable (score, highest to lowest)
    highScore, spot = listScore[0]

    for i in range(int(len(listScore)/2)): # Pops the first half of the best scores (floor value)
       listScore.pop(0)

    listScore.sort(key=lambda x: x[1], reverse=True)

    for obj in listScore:  # Pops the worst bots
        score, num = obj
        Bots.pop(num)

    for i in range(len(Bots) + odd): # Creates new bots to replace the deleted ones
        Bots[i].reset()
        newBot = Bot(Bots[i].screen, Bots[i].settings)
        newBot.brain = copy.deepcopy(Bots[i].brain)
        newBot.resetLife()
        newBot.evolve()
        Bots.append(newBot)

    return highScore

def botDead(bot): # Sets dead bots to the top of the screen till next gen starts
    bot.dead = True
    bot.x, bot.y = 160 + (bot.id *15), 5
    bot.rect.x, bot.rect.y = bot.x, bot.y
    bot.colorRect.x, bot.colorRect.y = bot.x + 5, bot.y + 15

def deadBotBox(botLen, screen):
    rect1 = pygame.Rect(170, 3, 15*botLen+15, 41)
    pygame.draw.rect(screen, (10, 10, 10), rect1, 3)

def roundTimer(gameStats): # Timer* when timer is over roundTimer it means that time is up.
    if gameStats.timer >= int(200 + (gameStats.gen * 2) + (gameStats.timerAdd * 1.4)):
        gameStats.nextGen()
        return True
    else:
        gameStats.timer += 1
        return False

# DISPLAY FUNCTIONS -----------------------------------------------------------------
def printInfo(bots, death, settings):
    if settings.printBotInfo == True:
        for bot in bots:
            if bot.dead == False or settings.printDeadBots == True:
                print("ID: " + str(bot.id), end='')
                if bot.dead == True:
                    tempText = "Dead"
                else:
                    tempText = "Alive"
                print(" | " + tempText, end='')
                print(" | (" + str(int(bot.x)) + ", " + str(int(bot.y)) + ")")

                bot.printBrain()
                print("---------------------------")

def screenRoll(gameStats, blocks, spikes, bots):
    if (gameStats.screen_roll or gameStats.screen_bot_roll) and gameStats.xShift < 400:
        gameStats.xShift += 2
        shift = 2
        for spike in spikes:
            spike.rect.x -= shift
        for block in blocks:
            block.rect.x -= shift
        for bot in bots:
            bot.x -= shift

    if gameStats.screen_roll_back and gameStats.xShift > 0:
        gameStats.xShift -= 2
        shift = 2
        for spike in spikes:
            spike.rect.x += shift
        for block in blocks:
            block.rect.x += shift
        for bot in bots:
            bot.x += shift


def resetScreen(gameStats, blocks, spikes, bots):
    for spike in spikes:
        spike.rect.x += gameStats.xShift
    for block in blocks:
        block.rect.x += gameStats.xShift
    for bot in bots:
        bot.x += gameStats.xShift

    gameStats.xShift = 0

def printText(allText, gameStats):
    allText[0].prep("Generation: " + str(gameStats.gen), 10, 10)
    for i in range(len(allText)):
        allText[i].blit()

def drawGrid(settings, screen, gameStats):
    for x in range(int(settings.screenHeight/50)):
        for i in range(int(settings.screenWidth/50) + 1):
            pygame.draw.line(screen, (150, 150, 150), (0, 50*x), (settings.screenWidth, x*50))
            pygame.draw.line(screen, (150, 150, 150), (i*50 - gameStats.xShift %50, 0), (i*50 - gameStats.xShift %50, settings.screenHeight))

# MAP GENERATION ----------------------------------------------------------
def makeMap(map, spikes, screen, settings):  # Simple loops to set the floor

    for i in range(5):
        x = randint(settings.screenWidth, settings.screenWidth * 2)
        y = randint(0, settings.screenHeight - 300)

    for i in range(32):  # for 4 long strips of dirt blocks
        newBlock = Block(settings, screen, 1, 1, 1)
        newBlock.rect.x = 50 * i
        newBlock.rect.y = (settings.screenHeight - 50)
        map.add(newBlock)

    # for i in range(4): # for 4 long strips of dirt blocks
    #     newBlock = Block(settings, screen, 8, 1)
    #     newBlock.rect.x = 400 * i
    #     newBlock.rect.y = (settings.screenHeight - 50)
    #     map.add(newBlock)

    # newBlock = Block(settings, screen, 1, 1)
    # newBlock.rect.x = 100
    # newBlock.rect.y = (settings.screenHeight - 100)
    # map.add(newBlock)

    newBlock = Block(settings, screen, 1, 1)
    newBlock.rect.x = 350
    newBlock.rect.y = (settings.screenHeight - 100)
    map.add(newBlock)

    newBlock = Block(settings, screen, 1, 2)
    newBlock.rect.x = 400
    newBlock.rect.y = (settings.screenHeight - 150)
    map.add(newBlock)

    newBlock = Block(settings, screen, 1, 3)
    newBlock.rect.x = 450
    newBlock.rect.y = (settings.screenHeight - 200)
    map.add(newBlock)

    newBlock = Block(settings, screen, 2, 1)
    newBlock.rect.x = 1000
    newBlock.rect.y = (settings.screenHeight - 100)
    map.add(newBlock)

    newBlock = Block(settings, screen, 2, 6)
    newBlock.rect.x = 1500
    newBlock.rect.y = (settings.screenHeight - 250)
    map.add(newBlock)

    # newBlock = Block(settings, screen, 2, 1)
    # newBlock.rect.x = 800
    # newBlock.rect.y = (settings.screenHeight - 100)
    # map.add(newBlock)

    newSpike= Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 130, settings.screenHeight -110
    spikes.add(newSpike)

    newSpike= Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 200, settings.screenHeight -50
    spikes.add(newSpike)

    for i in range(2):
        newSpike = Spike(settings, screen)
        newSpike.rect.x, newSpike.rect.bottom = 630 +(i * 95), settings.screenHeight - 50
        spikes.add(newSpike)

    for i in range(3):
        newSpike = Spike(settings, screen)
        newSpike.rect.x, newSpike.rect.bottom = 830 +(i * 45), settings.screenHeight - 100
        spikes.add(newSpike)

    newSpike= Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 1150, settings.screenHeight -100
    spikes.add(newSpike)

def blitMap(map):
    for block in map:
        if (checkOnScreen(block)):
            block.blit()

