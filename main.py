import pygame
from pygame.sprite import Group
from settings import Settings
from gameStats import GameStats
from enemies import Baddie
from textBox import Text
import gameFunctions as gf


def runGame():
    pygame.init()

    # Basic init (clock for fps, settings for easy number changes, gamestats for game variables, screen/display for window)
    clock = pygame.time.Clock()
    settings = Settings()
    gameStats = GameStats()
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("AI Game")

    text = Text(screen, settings, "Generation # Text", 30, 10, 10)
    allText = [text]

    spikes = Group() # group of all spikes
    map = Group() # Group of all Blocks
    gf.makeMap(map, spikes, screen, settings) # assigns blocks and spikes to groups

    enemies = Group() # testing enemy
    # newEnemy = Baddie(screen, settings)
    # newEnemy.rect.x, newEnemy.rect.y = 550, settings.screenHeight - 85
    # enemies.add(newEnemy)

    Bots = []
    gf.createBots(screen, settings, Bots) # For loop to create and append bots

    while True:
        screen.fill(settings.bgColor)    # Fills background with solid color, can add clouds or something later
        gf.blitMap(map)                  # Draws the map on screen
        gf.drawGrid(settings, screen, gameStats)    # Draw the Grid, helps for coding can be removed


        gf.checkEvents(gameStats)           # Checks Button Presses
        #gf.checkCollide(player, map, spikes)     # Checks to see if player is hitting the world around him
        gf.enemyBlockCollide(enemies, map)
        #gf.enemyPlayerCollide(player, enemies)
        gf.screenRoll(gameStats, map, spikes, Bots)

        if gameStats.pause == False:

            for bot in Bots:
                if gf.checkCollide(bot, map, spikes):
                    gameStats.death += 1
                if bot.dead == False:
                    if bot.rect.x > 19 * (bot.settings.screenWidth/24): # screen roll, Make optional or only scan once
                        gameStats.screen_bot_roll = True
                    data, item = gf.scanFront(bot, map, spikes)
                    bot.chooseInput(data, item)

            if gf.roundTimer(gameStats) or gameStats.death >= len(Bots): ## Things that are done to prepare for next gen ** Alll this into a function
                gameStats.screen_bot_roll = False ## This needs to be a function check to turn off
                gf.resetScreen(gameStats, map, spikes, Bots)

                tempTimerAdd = gf.splitBots(Bots) # Deletes the worst half and return the highest score
                gameStats.addTimer(tempTimerAdd)
                ## TIMER MIGHT BE MESS UP RIGHT NOW MUST CHECK LATER *******************************************

                for i in range(len(Bots)):
                    Bots[i].id = i + 1
                    Bots[i].increaseLife()

            gf.printInfo(Bots, gameStats.death, settings)
            for i in range(int(len(Bots))):
                if Bots[i].dead == False:
                    Bots[i].update()
                Bots[i].blit()
        else: # When pause is True
            for i in range(int(len(Bots))):
                Bots[i].blit()

        for enemy in enemies: # not affected by pause since it's being tested
            enemy.update()
            enemy.blit()

        gf.printText(allText, gameStats)

        gf.deadBotBox(len(Bots), screen)
        spikes.draw(screen)

        pygame.display.flip()            # Makes the display work (Don't Touch, Make sure this stay near the bottom)
        clock.tick(75)

runGame()


