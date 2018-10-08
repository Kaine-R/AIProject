Image sizes (pixels):
blocks are 50, 50
player is 20, 35
enemy 40, 30

If you want to quickly switch pictures change NAME in ("Images/NAME.png") to whatever the new picture name is.
Also in main gf is gameFunctions, but it's shorten to make it easier to use

Pygame Tips:

All objects that are bing displayed have a "rect"

You can use this to get several things:
    object.rect.x = (left pixel value)  #*can also use object.rect.left*
    object.rect.right = (right pixel value)
    object.rect.y = (top pixel value)   #*can also use object.rect.top*
    object.rect.bottom = (bottom pixel value)
    object.rect.width = (width of rect)
    EXAMPLE1: block.rect.x = 50 (moves the block 50 pixels from the left of the screen)
    EXAMPLE2: currentLocation = player.rect.y

You can change the location of objects by doing:
    objects.rect.y, objects.rect.x = 50, 100
        #*same as doing object.rect.y = 50
        #*              object.rect.x = 50

The objects that are included are: player, blocks (inside map)
# The player is a bit different, if you want to move him, then you have to move
#   player.x instead of player.rect.x

"map" is a group of "blocks"
For creating new blocks in map, it's easier to use a loop
You could also just code everyone individually:
    newblock = Map(settings, screen) # Creates object
    newBlock.rect.x, newBlock.rect.y = 50, 50 # moved block to coordinate (50, 50)
    map.add(newBlock)  # Adds new block into the group for collide testing


*** Enemy is not yet finished and is only going to be added if the spike doesn't seem like enough of a challenge. ***
*** As for as I know, pygame doesn't use triangles, so we'lll create some kind of square killing device ***
*** If you want to mess around with the code, but dont know where to start, mess with settings.