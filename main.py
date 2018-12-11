import pygame
from fileAndData import File
from pygame.sprite import Group
from settings import Settings
from gameStats import GameStats
from enemies import Baddie
from player import Player
from textBox import Text
from bot import Bot
import gameFunctions as gf


def runGame():
    pygame.init()

    timer = 0
    timerAdd = 0
    clock = pygame.time.Clock()
    settings = Settings()
    gameStats = GameStats()
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("AI Game")
    #player = Player(screen, settings)
    gen = 0
    death = 0

    text = Text(screen, settings, "Testing asdasd", 30, 10, 10)

    allText = []
    allText.append(text)


    map = Group() # Group of all Blocks
    spikes = Group() # testing spikes
    sky = Group()
    enemies = Group() # testing enemy

    Bots = []
    for i in range(30):
        newBot = Bot(screen, settings)
        newBot.id = i + 1
        newBot.x += newBot.id * .5
        newBot.colorChange()
        Bots.append(newBot)

    # newEnemy = Baddie(screen, settings)
    # newEnemy.rect.x, newEnemy.rect.y = 550, settings.screenHeight - 85
    # enemies.add(newEnemy)



    gf.makeMap(map, spikes, sky, screen, settings) # makes the bottom layer right now

    while True:
        screen.fill(settings.bgColor)    # Fills background with solid color, can add clouds or something later
        gf.blitMap(map)                  # Draws the map on screen
        gf.blitMap(sky)
        gf.drawGrid(settings, screen, gameStats)    # Draw the Grid, helps for coding can be removed


        gf.checkEvents(gameStats)           # Checks Button Presses
        #gf.checkCollide(player, map, spikes)     # Checks to see if player is hitting the world around him
        gf.enemyBlockCollide(enemies, map)
        #gf.enemyPlayerCollide(player, enemies)
        #player.updatePlayer(map)         # Movement of the player
        gf.screenRoll(gameStats, map, spikes, Bots)

        for bot in Bots:
            if gf.checkCollide(bot, map, spikes):
                death += 1
            if bot.dead == False:
                if bot.rect.x > 19* (bot.settings.screenWidth/24):
                    gameStats.screen_bot_roll = True
                data, item = gf.scanFront(bot, map, spikes)
                bot.chooseInput(data, item)



        timer += 1
        if gf.roundTimer(timer, int(200 + (gen * 2) + (timerAdd * 1.4))) or death >= len(Bots):
            death = 0
            gen += 1
            timer = 0
            timerAdd = 0
            gameStats.screen_bot_roll = False
            gf.resetScreen(gameStats, map, spikes, Bots)
            for i in range(len(Bots)-1):

                if Bots[i].score > timerAdd:
                    timerAdd = int(Bots[i].score)
            gf.split(gf.bestBots(Bots), Bots)
            for i in range(int(len(Bots) -15)):
                Bots[i+15].brain.evolve()
                Bots[i+15].reset()
            for i in range(len(Bots)-1):
                Bots[i].id = i + 1
                Bots[i].colorChange()

        #gf.printInfo(Bots, death)
        for i in range(int(len(Bots))):
            if Bots[i].dead == False:
                Bots[i].update()
            Bots[i].blit()

        for enemy in enemies:
            enemy.update()
            enemy.blit()

        for text in allText:
            text.prep("Generation: " + str(gen), 10, 10)
            text.blit()

        spikes.draw(screen)

        pygame.display.flip()            # Makes the display work (Don't Touch, Make sure this stay near the bottom)
        clock.tick(1200)

runGame()