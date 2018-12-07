import pygame
from bot import Bot
from block import Block
from cloud import Cloud
from spike import Spike
import sys
import copy
from random import randint

# INPUTS BY USER ----------------------------------------------------------
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
        pass

# COLLISIONS -------------------------------------------------------------------

def checkCollide(bot, map, spikes):
    dead = False
    ground = False  # This is here to see if it's touching the ground, else it floats when walking off edge
    if spikeCollide(bot, spikes):
        if bot.id != 0:
            botDead(bot)
            dead = True

    elif bot.y + bot.rect.height > bot.settings.screenHeight:
        botDead(bot)
        bot.dead = True

    for block in map:
        if pygame.sprite.collide_rect(bot, block):
            if checkDirection(bot, block): # checks if any of the blocks that touch are below player
                ground = True

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

def spikeCollide(bot, spikes):
    if pygame.sprite.spritecollideany(bot, spikes):
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

# MAP CREATION ----------------------------------------------------------
def makeMap(map, spikes, screen, settings):  # Simple loops to set the floor

    for i in range(5):
        x = randint(settings.screenWidth, settings.screenWidth * 2)
        y = randint(0, settings.screenHeight - 300)
        newCloud = Cloud(settings, screen, x, y)
        map.add(newCloud)


    for i in range(4):
        newBlock = Block(settings, screen, 8, 1)
        newBlock.rect.x = 400 * i
        newBlock.rect.y = (settings.screenHeight - 50)
        map.add(newBlock)

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


def blitMap(map):
    for blocks in map:
        blocks.blit()

# FILE FUNTIONS ----------------------------------------------------------
def scanFront(player, map, spikes):
    item = -1 # item hit
    data = 1200
    tempItem = -1
    tempData = 1300
    for block in map:
        tempData, tempItem = scanObject(block, player)
        if tempData < data:
            data = tempData
            item = tempItem

    for spike in spikes:
        tempData, tempItem = scanObject(spike, player)
        if tempData < data:
            data = tempData
            item = tempItem

    #print(data, item)

    if item != -1:
        return data, item
    else:
        return "none", -1

def addInfo(file, info):
    splitA, splitB = info

def scanObject(object, player):
    scanHit = (player.x + player.rect.width +5, player.y - player.rect.height/3)
    item = -1
    data = 1300

    for i in range(20):
        if object.rect.collidepoint(scanHit):
            temp = object.rect.x - player.rect.right
            if temp < data:
                data = temp
                item = object.id
                break
        scanHit = (player.x + player.rect.width + (i * 20), player.y + player.rect.height / 3)

    return (data, item)

def bestBots(bots):
    listScore = []
    for i in range(int(len(bots))):
        if bots[i].dead:
            bots[i].score -= int(bots[i].score/4)
        else:
            bots[i].score -=5
        listScore.append((bots[i].score, i))
    listScore.sort()
    print("Sort Bots:")
    print(listScore)

    return listScore

def split(listScore, Bots):
    listNum = []
    for i in range(int(len(listScore) /2)):
        tempScore, tempNum = listScore[i]
        listNum.append(tempNum)

    listNum.sort(reverse=True)
    for num in listNum:
        Bots.pop(num)

    size = int(len(Bots))
    for i in range(size):
        newBot = Bot(Bots[i].screen, Bots[i].settings)
        newBot.brain = copy.deepcopy(Bots[i].brain)
        Bots[i].reset()
        Bots.append(newBot)


def botDead(bot):
    bot.dead = True
    bot.x, bot.y = 160 + (bot.id *17), 5
    bot.rect.x, bot.rect.y = bot.x, bot.y
    bot.colorRect.x, bot.colorRect.y = bot.x, bot.y

def roundTimer(timer, roundTime):
    if timer >= roundTime:
        timer = 0
        return True
    return False


# EXTRAS -----------------------------------------------------------------

def drawGrid(settings, screen, gameStats):
    for x in range(int(settings.screenHeight/50)):
        for i in range(int(settings.screenWidth/50) + 1):
            pygame.draw.line(screen, (150, 150, 150), (0, 50*x), (settings.screenWidth, x*50))
            pygame.draw.line(screen, (150, 150, 150), (i*50 - gameStats.xShift %50, 0), (i*50 - gameStats.xShift %50, settings.screenHeight))

def printInfo(bots, death):
    for bot in bots:
        print("ID " + str(bot.id) + "_" + str(bot.dead) + ": (" + str(bot.x) + ", " + str(bot.y) + ")")

        print(bot.brain.nodes)
        print("---------------------------")

   # print(str(death) + " : " + str(len(bots)))
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
