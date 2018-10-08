import pygame
import sys
from map import Map
import sys


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
        print("↑")

# PLAYER SKILLS ---------------------------------------------------------------

def jump(player):
    if player.drop == True and player.landed:
        player.baseJump = player.rect.bottom
        player.drop = False
        player.landed = False

def checkJump(player):
    if player.baseJump - player.rect.bottom > player.settings.jumpLimit:
        player.drop = True
        player.collideBottom = False

# COLLISIONS -------------------------------------------------------------------

def checkCollide(player, map, spikes):
    ground = False  # This is here to see if it's touching the ground, else it floats when walking off edge
    spikeCollide(player, spikes)

    if player.x < 0:
        player.collideLeft = True
    elif player.x + player.rect.width > player.settings.screenWidth:
        player.collideRight = True

    for block in map:
        if pygame.sprite.collide_rect(player, block):
            ground = checkDirection(player, block)
            resetCollides(player)
        checkJump(player)

    if ground == False:
        player.collideBottom = False

def checkDirection(player, block):
    below = False
    left = False
    right = False

    # This checks to see if the block is to the left or right
    if player.rect.centerx <= block.rect.centerx:
        left = True
    elif player.rect.centerx > block.rect.centerx and player.rect.bottom - player.rect.height/2 <= block.rect.bottom -1:
        right = True
    if player.rect.bottom - player.rect.height/2 <= block.rect.y:  # Checks to see if the block is below
        below = True

    if left and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit RIGHT")
        player.collideRight = True
    if right and not below:  # Checks to see if there's a block that's not getting stepped on
        print("hit LEFT")
        player.collideLeft = True
    if below:  # if any blocck is below then it counts as standing on something
        player.landed = True
        player.collideBottom = True
        return True
    return False

def resetCollides(player):  # If left or right collision is detected then it pushes player back and stops the collision
    if player.collideRight:
        player.x -= 1
        player.collideRight = False
    elif player.collideLeft:
        player.x += 1
        player.collideLeft = False

def spikeCollide(player, spikes):
    if pygame.sprite.spritecollideany(player, spikes):
        player.x = 50
        player.y = player.settings.screenHeight - 100



# MAP CREATION ----------------------------------------------------------
def makeMap(map, screen, settings):  # Simple loops to set the floor
    for x in range(int(settings.screenWidth/50)):
        newBlock = Map(settings, screen)
        newBlock.rect.x = x * 50
        newBlock.rect.y = (settings.screenHeight - 50)
        map.add(newBlock)

def blitMap(map):
    for blocks in map:
        blocks.blit()

# EXTRAS -----------------------------------------------------------------

def drawGrid(settings, screen):
    for x in range(int(settings.screenHeight/50)):
        for i in range(int(settings.screenWidth/50)):
            pygame.draw.line(screen, (150, 150, 150), (0, 50*x), (settings.screenWidth, x*50))
            pygame.draw.line(screen, (150, 150, 150), (i*50, 0), (i*50, settings.screenHeight))
