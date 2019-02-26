
# AI Project
I (Kaine Rubalcava) started this as a personal project where later on it was adapted into a AI course. Once the AI course was completed, I then wanted to take it a bit further. To do this I plan on making the game run faster and more efficiently.
Also adding some extra options would be the next major addition, these options would be: groups (how many groups would be in one generation), amount of bots in the groups, simple level editor, settings (screen width, height, frame rate cap), testing grounds (allows for testing to see how many bots on screen would start to make the program lag).

#Specs
I'm currently using Python(3) to create this program. The IDE I use is Pycharm with the Pygame library. My laptop is
currently using windows 10 and is fairly new, while I have tried running this program on other computers using various
operating systems there has been no testing to see if they preform as well as the specs I have now.

#### Image sizes (pixels):
```
blocks are 50, 50
player is 20, 35
enemy 40, 30
```

If you want to quickly switch pictures change NAME in ("Images/NAME.png") to whatever the new picture name is. Also in main gf is `gameFunctions`, but it's shorten to make it easier to use.

### Pygame Tips:

All objects that are being displayed have a "rect".

You can use this to get several things:
```python
object.rect.x = (left pixel value)  #*can also use object.rect.left*
object.rect.right = (right pixel value)
object.rect.y = (top pixel value)   #*can also use object.rect.top*
object.rect.bottom = (bottom pixel value)
object.rect.width = (width of rect)
EXAMPLE1: block.rect.x = 50 (moves the block 50 pixels from the left of the screen)
EXAMPLE2: currentLocation = player.rect.y
```

You can change the location of objects by doing:
```python
objects.rect.y, objects.rect.x = 50, 100
    #*same as doing object.rect.y = 50
    #*              object.rect.x = 50
```

The objects that are included are: player, blocks (inside map)

The player is a bit different, if you want to move him, then you have to move `player.x` instead of `player.rect.x`.

"map" is a group of "blocks". For creating new blocks in map, it's easier to use a loop. You could also just code everyone individually:
```python
    newblock = Map(settings, screen) # Creates object
    newBlock.rect.x, newBlock.rect.y = 50, 50 # moved block to coordinate (50, 50)
    map.add(newBlock)  # Adds new block into the group for collide testing
```