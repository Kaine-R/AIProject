import pygame
from fileAndData import File
from pygame.sprite import Group
from settings import Settings
from enemies import Baddie
from player import Player
from spike import Spike
import gameFunctions as gf


def runGame():
    pygame.init()

    settings = Settings()
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("AI Game")
    player = Player(screen, settings)
    file = File()

    map = Group() # Group of all Blocks
    spikes = Group() # testing spikes
    enemies = Group() # testing enemy

    # newEnemy = Baddie(screen, settings)
    # newEnemy.rect.x, newEnemy.rect.y = 550, settings.screenHeight - 85
    # enemies.add(newEnemy)

    newSpike, newSpike2 = Spike(settings, screen), Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 250, settings.screenHeight -50
    newSpike2.rect.x, newSpike2.rect.bottom = 600, settings.screenHeight -50
    spikes.add(newSpike, newSpike2)
    gf.makeMap(map, screen, settings) # makes the bottom layer right now

    while True:
        screen.fill(settings.bgColor)    # Fills background with solid color, can add clouds or something later
        gf.blitMap(map)                  # Draws the map on screen
        gf.drawGrid(settings, screen)    # Draw the Grid, helps for coding can be removed

        gf.addInfo(file, gf.scanFront(player, map, spikes))

        gf.checkEvents(player)           # Checks Button Presses
        gf.checkCollide(player, map, spikes)     # Checks to see if player is hitting the world around him
        gf.enemyBlockCollide(enemies, map)
        gf.enemyPlayerCollide(player, enemies)
        player.updatePlayer(map)         # Movement of the player
        player.drawPlayer()              # Draws the player

        for enemy in enemies:
            enemy.update()
            enemy.blit()

        gf.checkJump(player)
        spikes.draw(screen)

        # if pygame.time.get_ticks()%1000:
        #     file.save()
        pygame.display.flip()            # Makes the display work (Don't Touch, Make sure this stay near the bottom)


runGame()