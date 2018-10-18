import pygame
from pygame.sprite import Group
from settings import Settings
from block import Block
from player import Player
from spike import Spike
import gameFunctions as gf


def runGame():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("AI Game")
    player = Player(screen, settings)
    map = Group() # Group of all Blocks

    # testing spikes
    spikes = Group()
    newSpike, newSpike2 = Spike(settings, screen), Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 250, settings.screenHeight -50
    newSpike2.rect.x, newSpike2.rect.bottom = 600, settings.screenHeight -50
    spikes.add(newSpike, newSpike2)
    # creates a lone block above the rest for testing
    newBlock = Block(settings, screen)
    newBlock.rect.x, newBlock.rect.y = 300, settings.screenHeight - 100
    map.add(newBlock)
    gf.makeMap(map, screen, settings) # makes the bottom layer right now

    while True:
        screen.fill(settings.bgColor)    # Fills background with solid color, can add clouds or something later
        gf.blitMap(map)                  # Draws the map on screen
        gf.drawGrid(settings, screen)    # Draw the Grid, helps for coding can be removed

        gf.checkEvents(player)           # Checks Button Presses
        gf.checkCollide(player, map, spikes)     # Checks to see if player is hitting the world around him
        player.updatePlayer(map)         # Movement of the player
        player.drawPlayer()              # Draws the player
        gf.checkJump(player)             # Checks to see if top of jump is reached

        spikes.draw(screen)

        pygame.display.flip()            # Makes the display work (Don't Touch, Make sure this stay near the bottom)


runGame()