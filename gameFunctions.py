import pygame
from bot import Bot
from block import Block
import sys
import copy


# INPUTS BY USER ----------------------------------------------------------
def checkEvents(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            checkDown(event, player)
        elif event.type == pygame.KEYUP:
            checkUp(event, player)

def checkDown(event, player):
    if event.key == pygame.K_LEFT:
        player.movementLeft = True
    elif event.key == pygame.K_RIGHT:
        player.movementRight = True
    elif event.key == pygame.K_SPACE:
        jump(player)

def checkUp(event, player):
    if event.key == pygame.K_LEFT:
        player.movementLeft = False
    elif event.key == pygame.K_RIGHT:
        player.movementRight = False
    elif event.key == pygame.K_SPACE:
        pass

# PLAYER SKILLS ---------------------------------------------------------------

def jump(player):
    if player.jump == False and player.allowJump == True:
        player.jump = True
        player.allowJump = False
        player.baseJump = player.rect.bottom
        player.timer = 0

def checkJump(player, num = 0):
    if player.jump == True:
        if player.baseJump - player.rect.bottom > player.settings.jumpLimit or num == 1:
            player.jump = False
    if num == 1 or player.baseJump == round(player.rect.bottom):
            player.allowJump = True

# COLLISIONS -------------------------------------------------------------------

def checkCollide(player, map, spikes):
    dead = False
    ground = False  # This is here to see if it's touching the ground, else it floats when walking off edge
    if spikeCollide(player, spikes):
        if player.id != 0:
            botDead(player)
            dead = True

    if player.x < 0:
        player.collideLeft = True
    elif player.x + player.rect.width > player.settings.screenWidth:
        player.collideRight = True
    elif player.y + player.rect.height > player.settings.screenHeight:
        player.reset()

    for block in map:
        if pygame.sprite.collide_rect(player, block):
            if checkDirection(player, block): # checks if any of the blocks that touch are below player
                ground = True
                if player.timer > 15:
                    checkJump(player, 1)

    resetCollides(player)
    if ground == False:
        player.collideBottom = False

    return dead


def checkDirection(player, block):
    below = False
    left = False
    right = False

    # This checks to see if the block is to the left or right
    if player.rect.centerx <= block.rect.centerx:
        left = True
    elif player.rect.centerx > block.rect.centerx:
        right = True
    if player.rect.bottom - 5 <= block.rect.y:  # Checks to see if the block is below
        below = True

    if left and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit RIGHT")
        player.collideRight = True
    if right and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit LEFT")
        player.collideLeft = True
    if below:  # if any block is below then it counts as standing on something
        player.collideBottom = True
        return True
    return False

def resetCollides(player):  # If left or right collision is detected then it pushes player back and stops the collision
    if player.collideRight:
        player.x -= 1.5
        player.collideRight = False
    elif player.collideLeft:
        player.x += 1.5
        player.collideLeft = False

def spikeCollide(player, spikes):
    if pygame.sprite.spritecollideany(player, spikes):
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
def makeMap(map, screen, settings):  # Simple loops to set the floor
    newBlock = Block(settings, screen, 10, 1)
    newBlock.rect.x = 0
    newBlock.rect.y = (settings.screenHeight - 50)
    map.add(newBlock)

    newBlock = Block(settings, screen, 13, 1)
    newBlock.rect.x = 550
    newBlock.rect.y = (settings.screenHeight - 50)
    map.add(newBlock)

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

    newBlock = Block(settings, screen, 3, 3)
    newBlock.rect.x = 950
    newBlock.rect.y = (settings.screenHeight - 200)
    map.add(newBlock)

    newBlock = Block(settings, screen, 1, 1)
    newBlock.rect.x = 150
    newBlock.rect.y = (settings.screenHeight - 250)
    map.add(newBlock)


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
            bots[i].score = int(bots[i].score/4)
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
    bot.x, bot.y = (bot.id *18), 50
    bot.rect.x, bot.rect.y = bot.x, bot.y
    bot.colorRect.x, bot.colorRect.y = bot.x, bot.y

def roundTimer(timer, roundTime):
    if timer >= roundTime:
        timer = 0
        return True
    return False


# EXTRAS -----------------------------------------------------------------

def drawGrid(settings, screen):
    for x in range(int(settings.screenHeight/50)):
        for i in range(int(settings.screenWidth/50)):
            pygame.draw.line(screen, (150, 150, 150), (0, 50*x), (settings.screenWidth, x*50))
            pygame.draw.line(screen, (150, 150, 150), (i*50, 0), (i*50, settings.screenHeight))

def printInfo(bots, death):
    for bot in bots:
        print("ID " + str(bot.id) + "_" + str(bot.dead) + ": (" + str(bot.x) + ", " + str(bot.y) + ")")

        print(bot.brain.nodes)
        print("---------------------------")

   # print(str(death) + " : " + str(len(bots)))
    print("---------------------------")
