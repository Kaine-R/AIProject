import pygame
from fileAndData import File
from pygame.sprite import Group
from settings import Settings
from enemies import Baddie
from player import Player
from textBox import Text
from bot import Bot
from spike import Spike
import gameFunctions as gf


def runGame():
    pygame.init()

    timer = 0
    clock = pygame.time.Clock()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("AI Game")
    player = Player(screen, settings)
    file = File()
    gen = 0
    death = 0

    text = Text(screen, settings, "Testing asdasd", 30, 10, 10)

    allText = []
    allText.append(text)


    map = Group() # Group of all Blocks
    spikes = Group() # testing spikes
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

    newSpike, newSpike2 = Spike(settings, screen), Spike(settings, screen)
    newSpike3 = Spike(settings, screen)
    newSpike.rect.x, newSpike.rect.bottom = 265, settings.screenHeight -50
    newSpike2.rect.x, newSpike2.rect.bottom = 650, settings.screenHeight -50
    newSpike3.rect.x, newSpike3.rect.bottom = 120, settings.screenHeight -100
    spikes.add(newSpike, newSpike2, newSpike3)

    gf.makeMap(map, screen, settings) # makes the bottom layer right now

    while True:
        screen.fill(settings.bgColor)    # Fills background with solid color, can add clouds or something later
        gf.blitMap(map)                  # Draws the map on screen
        gf.drawGrid(settings, screen)    # Draw the Grid, helps for coding can be removed

        # gf.addInfo(file, gf.scanFront(player, map, spikes))

        gf.checkEvents(player)           # Checks Button Presses
        gf.checkCollide(player, map, spikes)     # Checks to see if player is hitting the world around him
        gf.enemyBlockCollide(enemies, map)
        gf.enemyPlayerCollide(player, enemies)
        player.updatePlayer(map)         # Movement of the player
        player.drawPlayer()              # Draws the player


        for bot in Bots:
            if gf.checkCollide(bot, map, spikes):
                death += 1
            if bot.dead == False:
                data, item = gf.scanFront(bot, map, spikes)
                bot.chooseInput(data, item)



        timer += 1
        if gf.roundTimer(timer, 280 + gen) or death >= len(Bots):
            death = 0
            gen += 1
            timer = 0
            gf.split(gf.bestBots(Bots), Bots)
            for i in range(int(len(Bots))):
                Bots[i].brain.evolve()
                Bots[i].id = i + 1
                Bots[i].reset()
                Bots[i].colorChange()

        gf.printInfo(Bots, death)
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

        gf.checkJump(player)
        spikes.draw(screen)

        pygame.display.flip()            # Makes the display work (Don't Touch, Make sure this stay near the bottom)
        clock.tick(120)

runGame()