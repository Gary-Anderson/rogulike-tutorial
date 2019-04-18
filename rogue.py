# 3rd party moduals

import pygame
import tcod as libtcod
import math
import pickle
import gzip
import random

# game files
import constants

#                           tttt                                                                            tttt
#                        ttt:::t                                                                         ttt:::t
#                        t:::::t                                                                         t:::::t
#                        t:::::t                                                                         t:::::t
#     ssssssssss   ttttttt:::::ttttttt   rrrrr   rrrrrrrrr   uuuuuu    uuuuuu      ccccccccccccccccttttttt:::::ttttttt        ssssssssss
#   ss::::::::::s  t:::::::::::::::::t   r::::rrr:::::::::r  u::::u    u::::u    cc:::::::::::::::ct:::::::::::::::::t      ss::::::::::s
# ss:::::::::::::s t:::::::::::::::::t   r:::::::::::::::::r u::::u    u::::u   c:::::::::::::::::ct:::::::::::::::::t    ss:::::::::::::s
# s::::::ssss:::::stttttt:::::::tttttt   rr::::::rrrrr::::::ru::::u    u::::u  c:::::::cccccc:::::ctttttt:::::::tttttt    s::::::ssss:::::s
#  s:::::s  ssssss       t:::::t          r:::::r     r:::::ru::::u    u::::u  c::::::c     ccccccc      t:::::t           s:::::s  ssssss
#    s::::::s            t:::::t          r:::::r     rrrrrrru::::u    u::::u  c:::::c                   t:::::t             s::::::s
#       s::::::s         t:::::t          r:::::r            u::::u    u::::u  c:::::c                   t:::::t                s::::::s
# ssssss   s:::::s       t:::::t    ttttttr:::::r            u:::::uuuu:::::u  c::::::c     ccccccc      t:::::t    ttttttssssss   s:::::s
# s:::::ssss::::::s      t::::::tttt:::::tr:::::r            u:::::::::::::::uuc:::::::cccccc:::::c      t::::::tttt:::::ts:::::ssss::::::s
# s::::::::::::::s       tt::::::::::::::tr:::::r             u:::::::::::::::u c:::::::::::::::::c      tt::::::::::::::ts::::::::::::::s
#  s:::::::::::ss          tt:::::::::::ttr:::::r              uu::::::::uu:::u  cc:::::::::::::::c        tt:::::::::::tt s:::::::::::ss
#   sssssssssss              ttttttttttt  rrrrrrr                uuuuuuuu  uuuu    cccccccccccccccc          ttttttttttt    sssssssssss


class struc_Tile:
    def __init__(self, blockPath):
        self.blockPath = blockPath
        self.explored = False

class struc_Preferences:
    def __init__(self):

        self.musicVol = .1
        self.FXVol = .1




#                 bbbbbbbb
#                 b::::::b             jjjj                                                  tttt
#                 b::::::b            j::::j                                              ttt:::t
#                 b::::::b             jjjj                                               t:::::t
#                  b:::::b                                                                t:::::t
#    ooooooooooo   b:::::bbbbbbbbb   jjjjjjj    eeeeeeeeeeee        ccccccccccccccccttttttt:::::ttttttt        ssssssssss
#  oo:::::::::::oo b::::::::::::::bb j:::::j  ee::::::::::::ee    cc:::::::::::::::ct:::::::::::::::::t      ss::::::::::s
# o:::::::::::::::ob::::::::::::::::b j::::j e::::::eeeee:::::ee c:::::::::::::::::ct:::::::::::::::::t    ss:::::::::::::s
# o:::::ooooo:::::ob:::::bbbbb:::::::bj::::je::::::e     e:::::ec:::::::cccccc:::::ctttttt:::::::tttttt    s::::::ssss:::::s
# o::::o     o::::ob:::::b    b::::::bj::::je:::::::eeeee::::::ec::::::c     ccccccc      t:::::t           s:::::s  ssssss
# o::::o     o::::ob:::::b     b:::::bj::::je:::::::::::::::::e c:::::c                   t:::::t             s::::::s
# o::::o     o::::ob:::::b     b:::::bj::::je::::::eeeeeeeeeee  c:::::c                   t:::::t                s::::::s
# o::::o     o::::ob:::::b     b:::::bj::::je:::::::e           c::::::c     ccccccc      t:::::t    ttttttssssss   s:::::s
# o:::::ooooo:::::ob:::::bbbbbb::::::bj::::je::::::::e          c:::::::cccccc:::::c      t::::::tttt:::::ts:::::ssss::::::s
# o:::::::::::::::ob::::::::::::::::b j::::j e::::::::eeeeeeee   c:::::::::::::::::c      tt::::::::::::::ts::::::::::::::s
#  oo:::::::::::oo b:::::::::::::::b  j::::j  ee:::::::::::::e    cc:::::::::::::::c        tt:::::::::::tt s:::::::::::ss
#    ooooooooooo   bbbbbbbbbbbbbbbb   j::::j    eeeeeeeeeeeeee      cccccccccccccccc          ttttttttttt    sssssssssss
#                                     j::::j
#                           jjjj      j::::j
#                          j::::jj   j:::::j
#                          j::::::jjj::::::j
#                           jj::::::::::::j
#                             jjj::::::jjj
#                                jjjjjj


class obj_Actor:
    # this class represents every object in the game
    def __init__(self,
                 x, y,
                 nameObject,
                 animationKey,
                 depth = 1,
                 animationSpeed=None,
                 creature=None,
                 ai=None,
                 container=None,
                 item=None,
                 spellBook=None,
                 equipment=None,
                 stairs = None):

        self.x = x  # map address
        self.y = y  # map address
        self.nameObject = nameObject  # instance name
        self.animationKey = animationKey
        self.animation = ASSETS.animationDict[self.animationKey]  # list of images
        self.depth = depth # where in the draw order
        self.animationSpeed = animationSpeed  # in seconds
        self.spriteImage = 0  # index number of self.animation

        # animation flicker speed
        if animationSpeed:
            self.flickerSpeed = self.animationSpeed / len(self.animation)
            self.flicker = self.animationSpeed / len(self.animation)
            self.flickerTimer = 0

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            self.item = com_Item()
            self.item.owner = self

        self.stairs = stairs
        if self.stairs:
            self.stairs.owner = self

    def draw(self):

        isVisible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if isVisible:
            # if self.animation is just 1 image, blit it. No animation code
            if self.animationSpeed == None:
                SURFACE_MAP.blit(
                    self.animation, (self.x * constants.CELL_WIDTH,
                                     self.y * constants.CELL_HEIGHT))

            # if self.animation is multiple images, animate them
            elif len(self.animation) > 1:

                # > 0.0 because get_fps doesn't have a value until 10 frames have passed (?)
                if CLOCK.get_fps() > 0.0:

                    # the flickerTimer increments by the (1 / fps)
                    self.flickerTimer += 1 / CLOCK.get_fps()

                    # when the flickerTimer reaches the flickerSpeed, reset the timer
                if self.flickerTimer >= self.flickerSpeed:
                    self.flickerTimer = 0.0

                    # this if-else loops us through the image stack in self.animation
                    if self.spriteImage >= len(self.animation) - 1:
                        self.spriteImage = 0
                    else:
                        self.spriteImage += 1

                SURFACE_MAP.blit(self.animation[self.spriteImage],
                                  (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))

    def distanceTo(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    @property
    def displayName(self):
        if self.creature:
            return (self.creature.nameInstance + ' the ' + self.nameObject)

        if self.item:
            if self.equipment and self.equipment.equipped:
                return (self.nameObject + ' (e)')
            else:
                return self.nameObject

    def moveTowards(self, other):

        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        self.creature.move(dx, dy)

    def animationDestroy(self):
        self.animation = None

    def animationInit(self):
        self.animation = ASSETS.animationDict[self.animationKey]

class obj_Game:
    # this class is used to consolidate global game variables
    def __init__(self):
        self.msgHistory = []
        self.currentObj = []
        self.previousMaps = []
        self.nextMaps = []
        self.currentMap, self.roomList = mapCreate()

    def transitionNextMap(self):
        global FOV_CALC

        FOV_CALC = True

        # if we are going to a new map
        if len(self.nextMaps) == 0:

            # remove surfaces from saved objects
            for obj in self.currentObj:
                obj.animationDestroy()
            # save currentMap
            self.previousMaps.append((PLAYER.x, PLAYER.y,
                                      self.currentMap,
                                      self.roomList,
                                      self.currentObj))
            # make a new map
            self.currentObj = [PLAYER]
            self.currentMap, self.roomList = mapCreate()
            mapPlaceObjects(self.roomList)

            # initialize surfaces
            for obj in self.currentObj:
                obj.animationInit()

        # go to a previously visited map
        else:

            # remove surfaces from saved objects
            for obj in self.currentObj:
                obj.animationDestroy()

            self.previousMaps.append((PLAYER.x, PLAYER.y,
                                      self.currentMap,
                                      self.roomList,
                                      self.currentObj))
            (PLAYER.x, PLAYER.y,
             self.currentMap,
             self.roomList,
             self.currentObj) = self.nextMaps[-1]

            # initialize surfaces
            for obj in self.currentObj:
                obj.animationInit()

            mapMakeFOV(self.currentMap)
            FOV_CALC = True

            del self.nextMaps[-1]

    def transitionPreviousMap(self):

        global FOV_CALC

        if len(self.previousMaps) != 0:

            # remove surfaces from saved objects
            for obj in self.currentObj:
                obj.animationDestroy()

            self.nextMaps.append((PLAYER.x, PLAYER.y,
                                      self.currentMap,
                                      self.roomList,
                                      self.currentObj))
            (PLAYER.x, PLAYER.y,
             self.currentMap,
             self.roomList,
             self.currentObj) = self.previousMaps[-1]

            # initialize surfaces
            for obj in self.currentObj:
                obj.animationInit()

            mapMakeFOV(self.currentMap)
            FOV_CALC = True

            del self.previousMaps[-1]

class obj_Spritesheet:
    # This class is used to grab images out of a spritesheet
    def __init__(self, fileName):

        # load the sprite sheet
        self.spriteSheet = pygame.image.load(fileName).convert()

        # all this does is tell the computer what number to use for each letter.
        # the letters are just for the custom sprite sheet we use. (see aquaticcreatures.png)
        self.tileDict = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8,
                         'i': 9, 'j': 10, 'k': 11, 'l': 12,
                         'm': 13, 'n': 14, 'o': 15, 'p': 16, '0': 0}
    # self.S_TITLE = self.title.getImage('0', 0, 16, 16, (32, 32))[0]
    def getImage(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT,
                 T_scale=None):
        # this func gets the desired image off the spritesheet

        # this will hold the images for animations
        imageList = []

        # get a surface to draw to
        image = pygame.Surface([width, height]).convert()

        # blit the image onto the surface
        # blit(spritesheet, address on surface, x of spritesheet, y of spritesheet, how wide, how high)
        image.blit(self.spriteSheet, (0, 0),
                   (self.tileDict[column] * width, row * height, width, height))

        # transparency?
        image.set_colorkey(constants.COLOR_BLACK)

        # if we need to rescale the image
        if T_scale:
            (newX, newY) = T_scale
            image = pygame.transform.scale(image, (newX, newY))

        imageList.append(image)

        return imageList

    def getAnimation(self, column, row, width=constants.CELL_WIDTH, height=constants.CELL_HEIGHT,
                     numSprites=1, T_scale=None):
        # this func gets the desired image off the spritesheet

        # this will hold the images for animations
        imageList = []

        for i in range(numSprites):
            # get a surface to draw to
            image = pygame.Surface([width, height]).convert()

            # blit the image onto the surface
            # blit(spritesheet, address on surface, x of spritesheet, y of spritesheet, how wide, how high)
            image.blit(self.spriteSheet, (0, 0),
                       (self.tileDict[column] * width + (width * i), row * height, width, height))

            # transparency?
            image.set_colorkey(constants.COLOR_BLACK)

            # if we need to rescale the image
            if T_scale:
                (newX, newY) = T_scale
                image = pygame.transform.scale(image, (newX, newY))

            imageList.append(image)

        return imageList

class obj_Room:
    '''This is a rectangle that represents a room
    '''
    def __init__(self, T_coords, T_size):
        #T_coords (ULx, ULy) are the upper-left corner of the rectangle
        self.ULx, self.ULy = T_coords

        self.width, self.height = T_size

        #(LRx, LRy) are the lower-right corner
        self.LRx = self.ULx + self.width
        self.LRy = self.ULy + self.height

    @property
    def center(self):
        # what is the center point of the room
        centerX = (self.ULx + self.LRx) // 2
        centerY = (self.ULy + self.LRy) // 2
        return (centerX, centerY)

    def intersects(self, other):
        # return True is other obj intercepts with this one

        # (self.leftWall <= other.rightWall) and (self.rightWall >= other.leftwall) and
        # (self.bottomWall <= other.topWall) and (self.topWall >= other.bottom wall)

        objectsIntersect = (self.ULx <= other.LRx and self.LRx >= other.ULx and
                            self.ULy <= other.LRy and self.LRy >= other.ULy)

        return objectsIntersect

class obj_Camera:

    def __init__(self):
        self.width = constants.CAMERA_WIDTH
        self.height = constants.CAMERA_HEIGHT
        self.x, self.y = (0, 0)

    def update(self):
        targetX = PLAYER.x * constants.CELL_WIDTH + (constants.CELL_WIDTH // 2)
        targetY = PLAYER.y * constants.CELL_HEIGHT + (constants.CELL_HEIGHT // 2)

        distanceX, distanceY = self.mapDist((targetX, targetY))


        self.x += int(distanceX * .1)
        self.y += int(distanceY * .1)

    def winToMap(self, T_coords):
        targetX, targetY = T_coords
        # convert window coords to distance from camera
        camDistX, camDistY = self.cameraDist((targetX, targetY))

        # convert distance from camera to map pixelCoord
        mapPixelX = self.x + camDistX
        mapPixelY = self.y + camDistY

        return ((mapPixelX, mapPixelY))
    def mapDist(self, T_coords):
        newX, newY = T_coords

        distX = newX - self.x
        distY = newY - self.y

        return (distX, distY)

    # how far away something is from the camera (in pixels on the window)
    def cameraDist(self, T_coords):
        winX, winY = T_coords

        distX = winX - (self.width // 2)
        distY = winY - (self.height // 2)

        return (distX, distY)

    @property
    def rectangle(self):
        posRect = pygame.Rect((0, 0), (constants.CAMERA_WIDTH,
                                       constants.CAMERA_HEIGHT))

        posRect.center = (self.x, self.y)

        return posRect

    @property
    def mapAddress(self):
        mapX = self.x // constants.CELL_WIDTH
        mapY = self.y // constants.CELL_HEIGHT

        return (mapX, mapY)

class obj_Assets:
    def __init__(self):
        self.loadAssets()
        self.adjustFXVol()
        self.adjustMusicVol()

    def loadAssets(self):

        ##################
        ## SPRITESHEETS ##
        ##################

        # title image
        self.title = obj_Spritesheet(constants.PATH + 'data/graphics/game/4176436.png')
        # creatures
        self.rodent = obj_Spritesheet(constants.PATH + 'data/graphics/Characters/Rodent.png')
        self.reptile = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Reptile.png")
        self.aquatic = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Aquatic.png")
        self.flesh = obj_Spritesheet(constants.PATH + "data/graphics/Items/Flesh.png")
        #walls and floors
        self.wall = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Wall.png")
        self.floor = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Floor.png")
        self.tile = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Tile.png")
        #equipment
        self.shortWep = obj_Spritesheet(constants.PATH + "data/graphics/Items/ShortWep.png")
        self.shield = obj_Spritesheet(constants.PATH + "data/graphics/Items/Shield.png")
        #items
        self.scroll = obj_Spritesheet(constants.PATH + "data/graphics/Items/Scroll.png")

        ################
        ## ANIMATIONS ##
        ################

        # title
        # image.blit(self.spriteSheet, (0, 0),
        #            (self.tileDict[column] * width, row * height, width, height))
        self.S_TITLE = self.title.getImage('0', 0, 260, 260)[0]

        self.A_PLAYER = self.reptile.getAnimation('o', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_ANACONDA_01 = self.reptile.getAnimation('a', 5, 16, 16, 2, (16, 16))
        self.A_SNAKE_ANACONDA_02 = self.reptile.getAnimation('c', 5, 16, 16, 2, (24, 24))
        self.A_SNAKE_ANACONDA_03 = self.reptile.getAnimation('e', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_COBRA_01 = self.reptile.getAnimation('g', 5, 16, 16, 2, (16, 16))
        self.A_SNAKE_COBRA_02 = self.reptile.getAnimation('i', 5, 16, 16, 2, (24, 24))
        self.A_SNAKE_COBRA_03 = self.reptile.getAnimation('k', 5, 16, 16, 2, (32, 32))
        self.A_SQUIREL = self.rodent.getAnimation('a', 1, 16, 16, 2, (32, 32))

        # corpse
        self.S_FLESH_TAIL = self.flesh.getImage('b', 4, 16, 16, (32, 32))[0]
        self.S_FLESH_TAIL_SMALL = self.flesh.getImage('b', 4, 16, 16, (16, 16))[0]
        self.S_FLESH_CORPSE_DEFAULT = self.flesh.getImage('d', 1, 16, 16, (32, 32))[0]

        # SPRITES ##
        self.S_WALL = self.wall.getImage('d', 10, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED = self.wall.getImage('d', 13, 16, 16, (32, 32))[0]

        self.S_FLOOR = self.floor.getImage('b', 8, 16, 16, (32, 32))[0]
        self.S_FLOOR_EXPLORED = self.floor.getImage('b', 14, 16, 16, (32, 32))[0]

        # EQUIPMENT
        self.S_SWORD = self.shortWep.getImage('a', 1, 16, 16, (32, 32))[0]
        self.S_SHIELD = self.shield.getImage('a', 1, 16, 16, (32, 32))[0]

        # ITEMS
        #lightning scroll
        self.S_SCROLL_01 = self.scroll.getImage('a', 1, 16, 16, (32, 32))[0]
        #fireball scrol
        self.S_SCROLL_02 = self.scroll.getImage('c', 2, 16, 16, (32, 32))[0]
        #confusion scroll
        self.S_SCROLL_03 = self.scroll.getImage('d', 6, 16, 16, (32, 32))[0]

        # SPECIAL
        self.S_STAIRS_DOWN = self.tile.getImage('h', 4, 16, 16, (32, 32))[0]
        self.S_STAIRS_UP = self.tile.getImage('e', 4, 16, 16, (32, 32))[0]

        self.animationDict = {

            "A_PLAYER" : self.A_PLAYER,
            "A_SNAKE_ANACONDA_01" : self.A_SNAKE_ANACONDA_01,
            "A_SNAKE_ANACONDA_02" : self.A_SNAKE_ANACONDA_02,
            "A_SNAKE_ANACONDA_03" : self.A_SNAKE_ANACONDA_03,
            "A_SNAKE_COBRA_01" : self.A_SNAKE_COBRA_01,
            "A_SNAKE_COBRA_02" : self.A_SNAKE_COBRA_02,
            "A_SNAKE_COBRA_03" : self.A_SNAKE_COBRA_03,
            "A_SQUIREL" : self.A_SQUIREL,

            # corpse
            "S_FLESH_TAIL" : self.S_FLESH_TAIL,
            "S_FLESH_TAIL_SMALL" : self.S_FLESH_TAIL_SMALL,
            "S_FLESH_CORPSE_DEFAULT" : self.S_FLESH_CORPSE_DEFAULT,

            # EQUIPMENT
            "S_SWORD" : self.S_SWORD,
            "S_SHIELD" : self.S_SHIELD,

            # ITEMS
            #lightning scroll
            "S_SCROLL_01" : self.S_SCROLL_01,
            #fireball scrol
            "S_SCROLL_02" : self.S_SCROLL_02,
            #confusion scroll
            "S_SCROLL_03" : self.S_SCROLL_03,

            # SPECIAL
            "S_STAIRS_DOWN" : self.S_STAIRS_DOWN,
            "S_STAIRS_UP" : self.S_STAIRS_UP

        }
        ###########
        ## AUDIO ##
        ###########

        # MUSIC
        self.musicMain = constants.PATH + 'data/sounds/cat theme.mp3'
        self.musicBkg = constants.PATH + 'data/sounds/level song.mp3'

        # FX

        #complete list of all sound FX
        self.soundFXList = []

        #hit sounds
        self.snd_hit_0 = self.addSoundFX(constants.PATH + 'data/sounds/hit_0.wav')
        self.snd_hit_1 = self.addSoundFX(constants.PATH + 'data/sounds/hit_1.wav')
        self.snd_hit_2 = self.addSoundFX(constants.PATH + 'data/sounds/hit_2.wav')
        self.snd_hit_3 = self.addSoundFX(constants.PATH + 'data/sounds/hit_3.wav')
        self.snd_hit_4 = self.addSoundFX(constants.PATH + 'data/sounds/hit_4.wav')
        self.snd_hit_5 = self.addSoundFX(constants.PATH + 'data/sounds/hit_5.wav')
        self.snd_hit_6 = self.addSoundFX(constants.PATH + 'data/sounds/hit_6.wav')
        self.snd_hit_7 = self.addSoundFX(constants.PATH + 'data/sounds/hit_7.wav')

        #sound list for getting hit
        self.snd_hitList = [self.snd_hit_0,
                            self.snd_hit_1,
                            self.snd_hit_2,
                            self.snd_hit_3,
                            self.snd_hit_4,
                            self.snd_hit_5,
                            self.snd_hit_6,
                            self.snd_hit_7]

    # adds sounds to self.soundFXList
    def addSoundFX(self, file):
        newSound = pygame.mixer.Sound(file)
        self.soundFXList.append(newSound)

        return newSound

    def adjustFXVol(self):
        for sound in self.soundFXList:
            sound.set_volume(PREF.FXVol)

    def adjustMusicVol(self):

        pygame.mixer.music.set_volume(PREF.musicVol)











#     cccccccccccccccc   ooooooooooo      mmmmmmm    mmmmmmm   ppppp   ppppppppp      ooooooooooo   nnnn  nnnnnnnn        eeeeeeeeeeee    nnnn  nnnnnnnn    ttttttt:::::ttttttt        ssssssssss
#   cc:::::::::::::::c oo:::::::::::oo  mm:::::::m  m:::::::mm p::::ppp:::::::::p   oo:::::::::::oo n:::nn::::::::nn    ee::::::::::::ee  n:::nn::::::::nn  t:::::::::::::::::t      ss::::::::::s
#  c:::::::::::::::::co:::::::::::::::om::::::::::mm::::::::::mp:::::::::::::::::p o:::::::::::::::on::::::::::::::nn  e::::::eeeee:::::een::::::::::::::nn t:::::::::::::::::t    ss:::::::::::::s
# c:::::::cccccc:::::co:::::ooooo:::::om::::::::::::::::::::::mpp::::::ppppp::::::po:::::ooooo:::::onn:::::::::::::::ne::::::e     e:::::enn:::::::::::::::ntttttt:::::::tttttt    s::::::ssss:::::s
# c::::::c     ccccccco::::o     o::::om:::::mmm::::::mmm:::::m p:::::p     p:::::po::::o     o::::o  n:::::nnnn:::::ne:::::::eeeee::::::e  n:::::nnnn:::::n      t:::::t           s:::::s  ssssss
# c:::::c             o::::o     o::::om::::m   m::::m   m::::m p:::::p     p:::::po::::o     o::::o  n::::n    n::::ne:::::::::::::::::e   n::::n    n::::n      t:::::t             s::::::s
# c:::::c             o::::o     o::::om::::m   m::::m   m::::m p:::::p     p:::::po::::o     o::::o  n::::n    n::::ne::::::eeeeeeeeeee    n::::n    n::::n      t:::::t                s::::::s
# c::::::c     ccccccco::::o     o::::om::::m   m::::m   m::::m p:::::p    p::::::po::::o     o::::o  n::::n    n::::ne:::::::e             n::::n    n::::n      t:::::t    ttttttssssss   s:::::s
# c:::::::cccccc:::::co:::::ooooo:::::om::::m   m::::m   m::::m p:::::ppppp:::::::po:::::ooooo:::::o  n::::n    n::::ne::::::::e            n::::n    n::::n      t::::::tttt:::::ts:::::ssss::::::s
#  c:::::::::::::::::co:::::::::::::::om::::m   m::::m   m::::m p::::::::::::::::p o:::::::::::::::o  n::::n    n::::n e::::::::eeeeeeee    n::::n    n::::n      tt::::::::::::::ts::::::::::::::s
#   cc:::::::::::::::c oo:::::::::::oo m::::m   m::::m   m::::m p::::::::::::::pp   oo:::::::::::oo   n::::n    n::::n  ee:::::::::::::e    n::::n    n::::n        tt:::::::::::tt s:::::::::::ss
#     cccccccccccccccc   ooooooooooo   mmmmmm   mmmmmm   mmmmmm p::::::pppppppp       ooooooooooo     nnnnnn    nnnnnn    eeeeeeeeeeeeee    nnnnnn    nnnnnn          ttttttttttt    sssssssssss
#                                                               p:::::p
#                                                               p:::::p
#                                                              p:::::::p
#                                                              p:::::::p
#                                                              p:::::::p
#                                                              ppppppppp


class com_Creature:
    # creature have health, can attack and die
    def __init__(self, nameInstance, baseAtk=2, baseDef=0, faction='monster', maxHP=10, deathFunc=None):
        self.nameInstance = nameInstance
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.faction = faction
        self.maxHP = maxHP
        self.currentHP = maxHP
        self.deathFunc = deathFunc

    def move(self, dx, dy):
        # if tile is wall: True else: False
        tileIsWall = mapCheckForWall(self.owner.x + dx, self.owner.y + dy)
        # tileIsWall = (GAME.currentMap[self.owner.x + dx][self.owner.y + dy].blockPath == True)

        # mapCheckForCreature( x and y you want to check,  exclude = self)
        target = mapCheckForCreature(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target and target.creature.faction != self.faction:
            self.attack(target)

        # if tile isn't a wall
        if not tileIsWall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target):

        damageDelt = (self.power) - (target.creature.defense)
        if damageDelt <= 0:
            damageDelt = 0
            gameMessage(self.owner.displayName +
                        "'s attack does no damage!")
        else:
            gameMessage(self.nameInstance +
                        ' attacks ' +
                        target.creature.nameInstance +
                        ' for ' +
                        str(damageDelt) +
                        ' damage!',
                        constants.COLOR_WHITE)

        target.creature.takeDamage(damageDelt)

        if damageDelt > 0:
            pygame.mixer.Sound.play(RANDOM_ENGINE.choice(ASSETS.snd_hitList))

    def takeDamage(self, damage):
        self.currentHP -= damage - self.baseDef
        gameMessage(self.nameInstance + "'s health is " + str(self.currentHP) +
                    '/' + str(self.maxHP), constants.COLOR_RED)

        if self.currentHP <= 0:
            if self.deathFunc is not None:
                self.deathFunc(self.owner)

    def heal(self, value):

        self.currentHP += value

        if self.currentHP > self.maxHP:
            self.currentHP = self.maxHP

    @property
    def power(self):
        atkBonus = 0
        if self.owner.container:
            for obj in self.owner.container.equippedItems:
                if obj.equipment.equipped:
                    atkBonus += obj.equipment.attackBonus
        totalPower = self.baseAtk + atkBonus
        return totalPower

    @property
    def defense(self):
        defBonus = 0
        if self.owner.container:
            for obj in self.owner.container.equippedItems:
                if obj.equipment.equipped:
                    defBonus += obj.equipment.defenseBonus
        totalDef = self.baseDef + defBonus
        return totalDef


class com_Container:

    def __init__(self, volume=10, inventory=[]):
        self.inventory = inventory
        self.maxVol = volume

    # TODO Get names of everything in our inventory

    # TODO Get volumne of within the container

    # if i '#' this out:
    # AttributeError: type object 'com_Container' has no attribute 'volume'
    @property
    def volume(self):
        return 0
    # TODO Get weight of everything in the inventory
    @property
    def equippedItems(self):
        equipmentList = [obj for obj in self.inventory
                         if obj.equipment and obj.equipment.equipped]
        return equipmentList


class com_Item:
    def __init__(self, weight=0, volume=0,
                 useFunc=None, value=None):
        self.weight = weight
        self.volume = volume
        self.value = value
        self.useFunc = useFunc

    # pick up an item
    def pickUp(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.maxVol:
                gameMessage('Not enough room to pick up!')
            else:
                gameMessage('Picking up...')
                self.owner.animationDestroy()
                actor.container.inventory.append(self.owner)
                GAME.currentObj.remove(self.owner)
                self.container = actor.container

    # drop an item
    def drop(self, newX, newY):
        GAME.currentObj.append(self.owner)
        self.owner.animationInit()
        self.container.inventory.remove(self.owner)
        self.owner.x = newX
        self.owner.y = newY
        gameMessage('Item dropped')

    # TODO way to use the item
    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggleEquip()
            return

        if self.useFunc:
            result = self.useFunc(self.container.owner, self.value)
            self.container.inventory.remove(self.owner)
            return result

        if result == 'canceled' or not result:
            return 'canceled'
        else:
            self.container.inventory.remove(self.owner)


class com_Equipment:
    def __init__(self, attackBonus=0, defenseBonus=0, slot=None):

        self.attackBonus = attackBonus
        self.defenseBonus = defenseBonus
        self.slot = slot

        self.equipped = False

    def toggleEquip(self):
        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        equippedItems = self.owner.item.container.equippedItems

        if not self.equipped:
            for item in equippedItems:
                if item.equipment.slot and (item.equipment.slot == self.slot):
                    gameMessage("That slot is full")
                    return

        self.equipped = True
        gameMessage(self.owner.nameObject + " is equipped")

    def unequip(self):
        self.equipped = False
        gameMessage(self.owner.nameObject + " is unequipped")


class com_SpellBook:
    # list of spells actor is able to cast
    def __init__(self, spellBook=[]):
        self.spellBook = spellBook


class com_Spell:
    def __init__(self, spellName, castFunc):
        self.spellName = spellName
        self.castFunc = castFunc

    # pick up an item
    def learnSpell(self, actor):
        if actor.SpellBook:
            actor.SpellBook.spellList.append(self.owner)

    # TODO way to use the item
    def cast(self):
        self.castFunc

class com_Stairs:
    def __init__(self, downwards = True):
        self.downwards = downwards

    def use(self):

        if self.downwards:
            GAME.transitionNextMap()
        else:
            GAME.transitionPreviousMap()

#                AAA               IIIIIIIIII
#               A:::A              I::::::::I
#              A:::::A             I::::::::I
#             A:::::::A            II::::::II
#            A:::::::::A             I::::I
#           A:::::A:::::A            I::::I
#          A:::::A A:::::A           I::::I
#         A:::::A   A:::::A          I::::I
#        A:::::A     A:::::A         I::::I
#       A:::::AAAAAAAAA:::::A        I::::I
#      A:::::::::::::::::::::A       I::::I
#     A:::::AAAAAAAAAAAAA:::::A      I::::I
#    A:::::A             A:::::A   II::::::II
#   A:::::A               A:::::A  I::::::::I
#  A:::::A                 A:::::A I::::::::I
# AAAAAAA                   AAAAAAAIIIIIIIIII

class ai_confuse:
    def __init__(self, oldAI, numTurns):
        self.oldAI = oldAI
        self.numTurns = numTurns
    # once per turn, execute

    def takeTurn(self):
        if self.numTurns > 0:
            self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                     libtcod.random_get_int(0, -1, 1))
            self.numTurns -= 1
        else:
            self.owner.ai = self.oldAI
            gameMessage(self.owner.creature.nameInstance + " the " +
                        self.owner.nameObject + " has come to their senses!")


class ai_chase:
    ''' A simple AI that just runs down the enemy and tries to attack'''

    def takeTurn(self):

        monster = self.owner
        faction = self.owner.creature.faction

        if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):

            # move towards enemy if too far away
            if monster.distanceTo(PLAYER) >= 2:
                if PLAYER.creature.currentHP > 0:
                    self.owner.moveTowards(PLAYER)
                else:
                    self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                             libtcod.random_get_int(0, -1, 1))
            # TODO attack if close enough
            elif PLAYER.creature.currentHP > 0:
                monster.creature.attack(PLAYER)

#             dddddddd
#             d::::::d                                            tttt         hhhhhhh
#             d::::::d                                         ttt:::t         h:::::h
#             d::::::d                                         t:::::t         h:::::h
#             d:::::d                                          t:::::t         h:::::h
#     ddddddddd:::::d     eeeeeeeeeeee    aaaaaaaaaaaaa  ttttttt:::::ttttttt    h::::h hhhhh
#   dd::::::::::::::d   ee::::::::::::ee  a::::::::::::a t:::::::::::::::::t    h::::hh:::::hhh
#  d::::::::::::::::d  e::::::eeeee:::::eeaaaaaaaaa:::::at:::::::::::::::::t    h::::::::::::::hh
# d:::::::ddddd:::::d e::::::e     e:::::e         a::::atttttt:::::::tttttt    h:::::::hhh::::::h
# d::::::d    d:::::d e:::::::eeeee::::::e  aaaaaaa:::::a      t:::::t          h::::::h   h::::::h
# d:::::d     d:::::d e:::::::::::::::::e aa::::::::::::a      t:::::t          h:::::h     h:::::h
# d:::::d     d:::::d e::::::eeeeeeeeeee a::::aaaa::::::a      t:::::t          h:::::h     h:::::h
# d:::::d     d:::::d e:::::::e         a::::a    a:::::a      t:::::t    tttttth:::::h     h:::::h
# d::::::ddddd::::::dde::::::::e        a::::a    a:::::a      t::::::tttt:::::th:::::h     h:::::h
#  d:::::::::::::::::d e::::::::eeeeeeeea:::::aaaa::::::a      tt::::::::::::::th:::::h     h:::::h
#   d:::::::::ddd::::d  ee:::::::::::::e a::::::::::aa:::a       tt:::::::::::tth:::::h     h:::::h
#    ddddddddd   ddddd    eeeeeeeeeeeeee  aaaaaaaaaa  aaaa         ttttttttttt  hhhhhhh     hhhhhhh

def death_Mob(mob):
    gameMessage(mob.creature.nameInstance + ' is dead!', constants.COLOR_GREY)

    mob.animationSpeed = None
    mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT
    mob.animationKey = "S_FLESH_CORPSE_DEFAULT"
    mob.depth = constants.DEPTH_CORPSE
    mob.creature = None
    mob.ai = None

def death_Snake(mob):
    gameMessage(mob.creature.nameInstance + ' is dead!', constants.COLOR_GREY)

    mob.animationSpeed = None
    if mob.creature.faction == 'neonates':
        mob.animation = ASSETS.S_FLESH_TAIL_SMALL
        mob.animationKey = "S_FLESH_TAIL_SMALL"
    else:
        mob.animation = ASSETS.S_FLESH_TAIL
        mob.animationKey = "S_FLESH_TAIL"
    mob.depth = constants.DEPTH_CORPSE
    mob.creature = None
    mob.ai = None

#    mmmmmmm    mmmmmmm     aaaaaaaaaaaaa  ppppp   ppppppppp
#  mm:::::::m  m:::::::mm   a::::::::::::a p::::ppp:::::::::p
# m::::::::::mm::::::::::m  aaaaaaaaa:::::ap:::::::::::::::::p
# m::::::::::::::::::::::m           a::::app::::::ppppp::::::p
# m:::::mmm::::::mmm:::::m    aaaaaaa:::::a p:::::p     p:::::p
# m::::m   m::::m   m::::m  aa::::::::::::a p:::::p     p:::::p
# m::::m   m::::m   m::::m a::::aaaa::::::a p:::::p     p:::::p
# m::::m   m::::m   m::::ma::::a    a:::::a p:::::p    p::::::p
# m::::m   m::::m   m::::ma::::a    a:::::a p:::::ppppp:::::::p
# m::::m   m::::m   m::::ma:::::aaaa::::::a p::::::::::::::::p
# m::::m   m::::m   m::::m a::::::::::aa:::ap::::::::::::::pp
# mmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaap::::::pppppppp
#                                           p:::::p
#                                           p:::::p
#                                          p:::::::p
#                                          p:::::::p
#                                          p:::::::p
#                                          ppppppppp

def mapCreate():
    # make a 2d list of out map
    newMap = [[struc_Tile(True) for y in list(range(0, constants.MAP_HEIGHT))]
              for x in list(range(0, constants.MAP_WIDTH))]

    # initialize our variables
    roomList = []
    numOfRooms = 0

    # generate a room with random dimentions
    for i in range(constants.MAP_MAX_ROOMS):
        w = libtcod.random_get_int(0, constants.ROOM_MIN_WIDTH,
                                      constants.ROOM_MAX_WIDTH)
        h = libtcod.random_get_int(0, constants.ROOM_MIN_HEIGHT,
                                      constants.ROOM_MAX_HEIGHT)
        x = libtcod.random_get_int(0, 2, constants.MAP_WIDTH - w - 2)
        y = libtcod.random_get_int(0, 2, constants.MAP_HEIGHT - h - 2)
        #create the room
        newRoom = obj_Room((x, y), (w, h))

        # place our room
        failed = False
        for otherRoom in roomList:
            # if our new room intersects a previously placed room, we're done
            if newRoom.intersects(otherRoom):
                failed = True
                break

        # if it doesn't intersect, carve the room into the map
        if not failed:
            mapCreateRoom(newMap, newRoom)
            currentCenter = newRoom.center

            # if this isn't the first room, tunnle from our previous room, to the new one
            if len(roomList) != 0:
                previousCenter = roomList[-1].center
                mapCreateTunnels(previousCenter, currentCenter, newMap)
            # add room to roomlist
            roomList.append(newRoom)
    # update the FOV map
    mapMakeFOV(newMap)
    return (newMap, roomList)

def mapPlaceObjects(roomList):
    topLevel = (len(GAME.previousMaps) == 0)


    i = 0
    for room in roomList:

        firstRoom = (room == roomList[0])
        lastRoom = (room == roomList[-1])

        if firstRoom: PLAYER.x, PLAYER.y = room.center

        if firstRoom and not topLevel: gen_stairs((PLAYER.x, PLAYER.y),
                                                  downwards = False)
        if lastRoom: gen_stairs(room.center)

        if i == 0:
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)
            gen_item((x, y))
        else:
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)
            gen_enemy((x, y))
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)
            gen_item((x, y))
        i += 1

def mapCreateRoom(map, incomingRoom):
    for x in range(incomingRoom.ULx, incomingRoom.LRx):
        for y in range(incomingRoom.ULy, incomingRoom.LRy):
            map[x][y].blockPath = False

def mapCreateTunnels(centerOld, centerNew, map):
    x1, y1 = centerOld
    x2, y2 = centerNew

    # 50/50 on whether we tunnel x or y first
    coinFlip = (libtcod.random_get_int(0, 0, 1) == 1)

    if coinFlip:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x][y1].blockPath = False
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x2][y].blockPath = False
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            map[x2][y].blockPath = False
        for x in range(min(x1, x2), max(x1, x2) + 1):
            map[x][y1].blockPath = False

def mapCheckForCreature(x, y, excludeObj=None):

    target = None

    if excludeObj:
        # check GAME.currentObj at x, y for a creature that isn't excluded
        for object in GAME.currentObj:
            if (object is not excludeObj and
                object.x == x and
                object.y == y and
                    object.creature):

                target = object

            if target:
                return target
    else:
        # check GAME.currentObj at x, y for any creature
        for object in GAME.currentObj:
            if (object.x == x and
                object.y == y and
                    object.creature):

                target = object

            if target:
                return target

def mapMakeFOV(incomingMap):
    global FOV_MAP

    # make another map to be used for FOV
    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    # set every tile in new map to be not transparent and not walkable
    for y in list(range(constants.MAP_HEIGHT)):
        for x in list(range(constants.MAP_WIDTH)):
            # libtcod.map_set_properties(map, x, y, transparent, walkable)
            libtcod.map_set_properties(FOV_MAP, x, y,
                                       not incomingMap[x][y].blockPath, not incomingMap[x][y].blockPath)

def mapCalcFOV():
    global FOV_CALC

    if FOV_CALC:
        FOV_CALC = False
    # libtcod.map_compute_fov(fov map, x, y, view radius, light walls = True, algo = FOV_BASIC)
    libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS,
                            constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)

def mapAtCoords(coordsX, coordsY):
    #
    objectOptions = [obj for obj in GAME.currentObj
                     if obj.x == coordsX and obj.y == coordsY]
    return objectOptions

def mapCheckForWall(x, y):
    '''This function checks to see if [x][y] is a wall or not

    ARGS:
    x = x you want to check
    y = y you want to check

    returns True if wall, False if not a wall
    '''

    isWall = GAME.currentMap[x][y].blockPath
    return isWall

def mapFindLine(T_coords1, T_coords2, range=None):
    ''' converts 2 (x, y) coords into a list of tiles

    ARGS:
        T_coords1 = a tuple of a map address(x1, y1)
        T_coords2 = a tuple of a map address(x2, y2)

    returns a list of tuple coords
    '''
    x1, y1 = T_coords1
    x2, y2 = T_coords2

    # THIS IS NOT IN THE TUTORIAL
    ''' the tutorial called for libtcod.line_init() and libtcod.line_step(),
        but those have been deprecated.
        line_iter() returns a iterable
    '''
    # returns an iterable
    lineIter = libtcod.line_iter(x1, y1, x2, y2)

    coordsList = []

    # if we are selecting ourselves, return ourself
    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    # we iterate over the iterable to generate our list
    for i in lineIter:
        if i != T_coords1:
            coordsList.append(i)

    return coordsList

def mapFindRadius(T_coordsCenter, radius):
    ''' This function returns a list of all the tiles in a square of size radius
        centered on T_coordsCenter

        ARGS:
        T_coordsCenter = (x, y) of center of square
        radius = how many tiles from center

        RETURN: a list of tuples representing all the tiles in the square

    '''
    # unpack our coords
    centerX, centerY = T_coordsCenter

    startX = (centerX - radius)
    endX = centerX + (radius + 1)
    startY = (centerY - radius)
    endY = centerY + (radius + 1)

    tileList = []

    for x in range(startX, endX):
        for y in range(startY, endY):
            tileList.append((x, y))

    return tileList






#             dddddddd
#             d::::::d                                                                           iiii
#             d::::::d                                                                          i::::i
#             d::::::d                                                                           iiii
#             d:::::d
#     ddddddddd:::::drrrrr   rrrrrrrrr   aaaaaaaaaaaaawwwwwww           wwwww           wwwwwwwiiiiiiinnnn  nnnnnnnn       ggggggggg   ggggg
#   dd::::::::::::::dr::::rrr:::::::::r  a::::::::::::aw:::::w         w:::::w         w:::::w i:::::in:::nn::::::::nn    g:::::::::ggg::::g
#  d::::::::::::::::dr:::::::::::::::::r aaaaaaaaa:::::aw:::::w       w:::::::w       w:::::w   i::::in::::::::::::::nn  g:::::::::::::::::g
# d:::::::ddddd:::::drr::::::rrrrr::::::r         a::::a w:::::w     w:::::::::w     w:::::w    i::::inn:::::::::::::::ng::::::ggggg::::::gg
# d::::::d    d:::::d r:::::r     r:::::r  aaaaaaa:::::a  w:::::w   w:::::w:::::w   w:::::w     i::::i  n:::::nnnn:::::ng:::::g     g:::::g
# d:::::d     d:::::d r:::::r     rrrrrrraa::::::::::::a   w:::::w w:::::w w:::::w w:::::w      i::::i  n::::n    n::::ng:::::g     g:::::g
# d:::::d     d:::::d r:::::r           a::::aaaa::::::a    w:::::w:::::w   w:::::w:::::w       i::::i  n::::n    n::::ng:::::g     g:::::g
# d:::::d     d:::::d r:::::r          a::::a    a:::::a     w:::::::::w     w:::::::::w        i::::i  n::::n    n::::ng::::::g    g:::::g
# d::::::ddddd::::::ddr:::::r          a::::a    a:::::a      w:::::::w       w:::::::w        i::::::i n::::n    n::::ng:::::::ggggg:::::g
#  d:::::::::::::::::dr:::::r          a:::::aaaa::::::a       w:::::w         w:::::w         i::::::i n::::n    n::::n g::::::::::::::::g
#   d:::::::::ddd::::dr:::::r           a::::::::::aa:::a       w:::w           w:::w          i::::::i n::::n    n::::n  gg::::::::::::::g
#    ddddddddd   dddddrrrrrrr            aaaaaaaaaa  aaaa        www             www           iiiiiiii nnnnnn    nnnnnn    gggggggg::::::g
#                                                                                                                                   g:::::g
#                                                                                                                       gggggg      g:::::g
#                                                                                                                       g:::::gg   gg:::::g
#                                                                                                                        g::::::ggg:::::::g
#                                                                                                                         gg:::::::::::::g
#                                                                                                                           ggg::::::ggg
#


def drawGame():
    # clear screen
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    SURFACE_MAP.fill(constants.COLOR_MAP_FOG)

    # update possition of camera
    CAMERA.update()

    # draw map
    drawMap(GAME.currentMap)

    # draw actors
    for obj in sorted(GAME.currentObj, key = lambda obj: obj.depth, reverse = True):
        obj.draw()

    SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

    drawDebug()
    drawMessages()

    # update the display
    pygame.display.flip()


def drawMap(mapToDraw):
    # get camera possition
    camX, camY = CAMERA.mapAddress

    # set the dimentions of the map display (in tiles)
    displayMapWidth = constants.CAMERA_WIDTH // constants.CELL_WIDTH
    displayMapHeight = constants.CAMERA_HEIGHT // constants.CELL_HEIGHT

    # set the parameters for our list of tiles to render
    renderWidthMin = camX - (displayMapWidth // 2)
    renderHeightMin = camY - (displayMapHeight // 2)
    renderWidthMax = camX + (displayMapWidth // 2)
    renderHeightMax = camY + (displayMapHeight // 2)

    # prevent rendering of the map
    if renderWidthMin < 0: renderWidthMin = 0
    if renderHeightMin < 0: renderHeightMin = 0
    if renderWidthMax > constants.MAP_WIDTH: renderWidthMax = constants.MAP_WIDTH
    if renderHeightMax > constants.MAP_HEIGHT: renderHeightMax = constants.MAP_HEIGHT

    for x in range(renderWidthMin, renderWidthMax):
        for y in range(renderHeightMin, renderHeightMax):

            isVisible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if isVisible:

                # the player will remember this tile when not seen
                mapToDraw[x][y].explored = True

                if mapToDraw[x][y].blockPath == True:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.S_WALL, (x * constants.CELL_WIDTH,
                                                      y * constants.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAP.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH,
                                                       y * constants.CELL_HEIGHT))

            #if not visible, but is explored
            elif mapToDraw[x][y].explored:

                if mapToDraw[x][y].blockPath == True:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.S_WALL_EXPLORED,
                                      (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAP.blit(ASSETS.S_FLOOR_EXPLORED,
                                      (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))


def drawText(displaySurf, textToDisplay, T_coords, textColor, font=constants.FONT_DEBUG_MESSAGE,
             backColor=None, centered=False):
    # This function takes text and displays it on the displaySurf

    # helperTextObjects() returns (text surface, text rectangle)
    # textRect is the box the text is in, textSurface is the 'image' of the text
    textSurf, textRect = helperTextObjects(
        textToDisplay, helperFont=font, incomingColor=textColor, incomingBgColor=backColor)

    # the top left corner of our text rectangle will be at the (x, y) in T_coords
    if centered:
        textRect.center = T_coords
    else:
        textRect.topleft = T_coords

    #
    displaySurf.blit(textSurf, textRect)


def drawMessages():

    if len(GAME.msgHistory) <= constants.NUM_MESSAGES:
        toDraw = GAME.msgHistory
    else:
        toDraw = GAME.msgHistory[-constants.NUM_MESSAGES:]

    textHeight = helperTextHeight(constants.FONT_DEBUG_MESSAGE)

    startY = (constants.CAMERA_HEIGHT -
              (constants.NUM_MESSAGES * textHeight)) - 5

    i = 0

    for message, color in toDraw:
        # drawText(surface, message, x, y)
        drawText(SURFACE_MAIN, message,
                 (0, (startY + (i * textHeight))), color, font=constants.FONT_MESSAGE_TEXT,
                 backColor=constants.COLOR_BLACK)

        i += 1


def drawDebug():

    drawText(SURFACE_MAIN, "fps: " + str(int(CLOCK.get_fps())),
             (0, 0), constants.COLOR_RED, backColor=constants.COLOR_BLACK)


def drawTileRect(T_coords, rectAlpha=None, mark=None, rectColor=constants.COLOR_BLACK):
    # convert (T_coords) to a tile address
    x, y = T_coords
    newX = x * constants.CELL_WIDTH
    newY = y * constants.CELL_WIDTH
    # make a new surface for the tile
    tileSurf = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    # fill the surf  with color
    tileSurf.fill(rectColor)
    # set the transparency
    if rectAlpha == None:
        tileSurf.set_alpha(100)
    else:
        tileSurf.set_alpha(rectAlpha)

    if mark:
        r, g, b = rectColor
        if ((r + g + b) / 3) < 80:
            drawText(tileSurf, mark, font=constants.FONT_CURSOR_TEXT, T_coords=(
                (constants.CELL_WIDTH // 2) - 0, (constants.CELL_HEIGHT // 2) - 1), textColor=constants.COLOR_WHITE, centered=True)
        else:
            drawText(tileSurf, mark, font=constants.FONT_CURSOR_TEXT, T_coords=(
                (constants.CELL_WIDTH // 2) - 0, (constants.CELL_HEIGHT // 2) - 1), textColor=constants.COLOR_BLACK, centered=True)
    # blit the rectancge to the map address
    SURFACE_MAP.blit(tileSurf, (newX, newY))


# hhhhhhh                                lllllll
# h:::::h                                l:::::l
# h:::::h                                l:::::l
# h:::::h                                l:::::l
#  h::::h hhhhh           eeeeeeeeeeee    l::::lppppp   ppppppppp       eeeeeeeeeeee    rrrrr   rrrrrrrrr       ssssssssss
#  h::::hh:::::hhh      ee::::::::::::ee  l::::lp::::ppp:::::::::p    ee::::::::::::ee  r::::rrr:::::::::r    ss::::::::::s
#  h::::::::::::::hh   e::::::eeeee:::::eel::::lp:::::::::::::::::p  e::::::eeeee:::::eer:::::::::::::::::r ss:::::::::::::s
#  h:::::::hhh::::::h e::::::e     e:::::el::::lpp::::::ppppp::::::pe::::::e     e:::::err::::::rrrrr::::::rs::::::ssss:::::s
#  h::::::h   h::::::he:::::::eeeee::::::el::::l p:::::p     p:::::pe:::::::eeeee::::::e r:::::r     r:::::r s:::::s  ssssss
#  h:::::h     h:::::he:::::::::::::::::e l::::l p:::::p     p:::::pe:::::::::::::::::e  r:::::r     rrrrrrr   s::::::s
#  h:::::h     h:::::he::::::eeeeeeeeeee  l::::l p:::::p     p:::::pe::::::eeeeeeeeeee   r:::::r                  s::::::s
#  h:::::h     h:::::he:::::::e           l::::l p:::::p    p::::::pe:::::::e            r:::::r            ssssss   s:::::s
#  h:::::h     h:::::he::::::::e         l::::::lp:::::ppppp:::::::pe::::::::e           r:::::r            s:::::ssss::::::s
#  h:::::h     h:::::h e::::::::eeeeeeee l::::::lp::::::::::::::::p  e::::::::eeeeeeee   r:::::r            s::::::::::::::s
#  h:::::h     h:::::h  ee:::::::::::::e l::::::lp::::::::::::::pp    ee:::::::::::::e   r:::::r             s:::::::::::ss
#  hhhhhhh     hhhhhhh    eeeeeeeeeeeeee llllllllp::::::pppppppp        eeeeeeeeeeeeee   rrrrrrr              sssssssssss
#                                                p:::::p
#                                                p:::::p
#                                               p:::::::p
#                                               p:::::::p
#                                               p:::::::p
#                                               ppppppppp

def helperTextObjects(incomingText, helperFont=constants.FONT_DEBUG_MESSAGE, incomingColor=constants.COLOR_WHITE, incomingBgColor=None):
    if incomingBgColor:
        # .render(text, aliasing, color)
        textSurf = helperFont.render(incomingText, False, incomingColor, incomingBgColor)
    else:
        textSurf = helperFont.render(incomingText, False, incomingColor)

    return textSurf, textSurf.get_rect()

# these two functions help with aligning text


def helperTextWidth(font):
    fontObj = font.render('A', False, (0, 0, 0))
    fontRect = fontObj.get_rect()

    return fontRect.width


def helperTextHeight(font):
    fontObj = font.render('A', False, (0, 0, 0))
    fontRect = fontObj.get_rect()

    return fontRect.height


#                                                                iiii
#                                                               i::::i
#                                                                iiii
#
#    mmmmmmm    mmmmmmm     aaaaaaaaaaaaa     ggggggggg   gggggiiiiiii     cccccccccccccccc
#  mm:::::::m  m:::::::mm   a::::::::::::a   g:::::::::ggg::::gi:::::i   cc:::::::::::::::c
# m::::::::::mm::::::::::m  aaaaaaaaa:::::a g:::::::::::::::::g i::::i  c:::::::::::::::::c
# m::::::::::::::::::::::m           a::::ag::::::ggggg::::::gg i::::i c:::::::cccccc:::::c
# m:::::mmm::::::mmm:::::m    aaaaaaa:::::ag:::::g     g:::::g  i::::i c::::::c     ccccccc
# m::::m   m::::m   m::::m  aa::::::::::::ag:::::g     g:::::g  i::::i c:::::c
# m::::m   m::::m   m::::m a::::aaaa::::::ag:::::g     g:::::g  i::::i c:::::c
# m::::m   m::::m   m::::ma::::a    a:::::ag::::::g    g:::::g  i::::i c::::::c     ccccccc
# m::::m   m::::m   m::::ma::::a    a:::::ag:::::::ggggg:::::g i::::::ic:::::::cccccc:::::c
# m::::m   m::::m   m::::ma:::::aaaa::::::a g::::::::::::::::g i::::::i c:::::::::::::::::c
# m::::m   m::::m   m::::m a::::::::::aa:::a gg::::::::::::::g i::::::i  cc:::::::::::::::c
# mmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaa   gggggggg::::::g iiiiiiii    cccccccccccccccc
#                                                      g:::::g
#                                          gggggg      g:::::g
#                                          g:::::gg   gg:::::g
#                                           g::::::ggg:::::::g
#                                            gg:::::::::::::g
#                                              ggg::::::ggg
#                                                 gggggg
def cast_look():

    coords = menu_tileSelect()
    if coords == 'canceled':
        return 'canceled'
    else:
        mapCoordsX, mapCoordsY = coords
        target = mapCheckForCreature(mapCoordsX, mapCoordsY)
        if target:
            gameMessage(target.displayName, constants.COLOR_WHITE)
            gameMessage(str(target.creature.nameInstance) +
                        "'s faction is " + str(target.creature.faction))
            gameMessage('HP: ' + str(target.creature.currentHP) + '/' +
                        str(target.creature.maxHP), constants.COLOR_RED)

        gameMessage('Map Address: (' + str(mapCoordsX) + ',' +
                    str(mapCoordsY) + ')', constants.COLOR_CYAN)


def cast_heal(target, value):
    if target.creature.currentHP == target.creature.maxHP:
        gameMessage(target.displayName + ' is at full health!', constants.COLOR_WHITE)
        return 'canceled'
    else:
        gameMessage(target.displayName + ' is healed for ' + str(value), constants.COLOR_YELLOW)
        target.creature.heal(value)
        gameMessage(target.displayName + ' health is now ' +
                    str(target.creature.currentHP) + '/' + str(target.creature.maxHP), constants.COLOR_WHITE)
        return 'cast heal'


def cast_lightning(caster,T_damage_maxRange = (5, 5),
                  local_penetrateWalls=False,
                  penetrateCreatures=True,
                  local_lineColor=constants.COLOR_WHITE,
                  local_lineAlpha=100):

    damage, spellRange = T_damage_maxRange

    coordsOrigin = (caster.x, caster.y)

    listOfTiles = []
    # select target via target select
    selectedTile, listOfTiles = menu_tileSelectLine(coordsOrigin,
                                                    range=spellRange,
                                                    hasRadius=False,
                                                    penetrateWalls=local_penetrateWalls,
                                                    lineColor=local_lineColor,
                                                    lineAlpha=local_lineAlpha)
    if selectedTile == 'canceled':
        return 'canceled'
    else:
        # apply damage to everything in the list
        for i, (x, y) in enumerate(listOfTiles):
            target = mapCheckForCreature(x, y)
            # if there is a target its not the caster
            if target:
                gameMessage(target.displayName + ' is hit by the lightning!', constants.COLOR_WHITE)
                target.creature.takeDamage(damage)
        return 'cast lightning'


def cast_fireball(caster, T_damage_radius_maxRange=(5, 1, 5)):

    # spell parameters
    damage, radius, maxRange = T_damage_radius_maxRange

    coordsOrigin = (caster.x, caster.y)
    # get list of line tiles
    listOfLineTiles = []
    selectedTile, listOfLineTiles = menu_tileSelectLine(coordsOrigin,
                                                        maxRange,
                                                        hasRadius=True,
                                                        radiusValue=radius,
                                                        radiusColor=constants.COLOR_RED,
                                                        radiusAlpha=60,
                                                        penetrateWalls=False,
                                                        penetrateCreatures=False,
                                                        lineColor=constants.COLOR_ORANGE,
                                                        lineAlpha=100)
    # get radius from selected tile
    if listOfLineTiles != None:
        listOfRadiusTiles = mapFindRadius(listOfLineTiles[-1], radius)
    if selectedTile == 'canceled':
        return 'canceled'
    else:
        for x, y in listOfRadiusTiles:

            target = mapCheckForCreature(x, y)
            # damage everything in radius
            if target:
                gameMessage(target.displayName + ' is hit by the fireball!', constants.COLOR_ORANGE)
                target.creature.takeDamage(damage)
        return 'cast fireball'


def cast_confusion(caster=None, spellDuration=5):
    # select tile
    selectedTile = menu_tileSelect(tileColor=constants.COLOR_PURPLE,)
    if selectedTile == 'canceled':
        return 'canceled'
    else:
        x, y = selectedTile
        # get target
        target = mapCheckForCreature(x, y)

    if target:
        localOldAI = target.ai

        target.ai = ai_confuse(oldAI=localOldAI, numTurns=spellDuration)
        target.ai.owner = target
        gameMessage(target.displayName + ' is confused!', constants.COLOR_PURPLE)
        return 'cast confusion'
    # temporarily confuse target


# UUUUUUUU     UUUUUUUUIIIIIIIIII
# U::::::U     U::::::UI::::::::I
# U::::::U     U::::::UI::::::::I
# UU:::::U     U:::::UUII::::::II
#  U:::::U     U:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U:::::D     D:::::U   I::::I
#  U::::::U   U::::::U   I::::I
#  U:::::::UUU:::::::U II::::::II
#   UU:::::::::::::UU  I::::::::I
#     UU:::::::::UU    I::::::::I
#       UUUUUUUUU      IIIIIIIIII

class ui_Button:
    def __init__(self, surface, buttonText, size, T_coordsCenter,
                 color = constants.COLOR_GREY,
                 box_mouseOverColor = constants.COLOR_RED,
                 box_colorDefault = constants.COLOR_BLUE,
                 text_mouseOverColor = constants.COLOR_WHITE,
                 text_colorDefault = constants.COLOR_WHITE):

        self.surface = surface
        self.buttonText  = buttonText
        self.size = size
        self.T_coordsCenter = T_coordsCenter

        self.color = color
        self.box_mouseOverColor = box_mouseOverColor
        self.box_colorDefault = box_colorDefault
        self.text_mouseOverColor = text_mouseOverColor
        self.text_colorDefault = text_colorDefault

        self.box_currentColor = box_colorDefault
        self.text_currentColor = text_colorDefault

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = T_coordsCenter

    @property
    def mouseInSurface(self):
        # dimensions of our window
        windowWidth = constants.CAMERA_WIDTH
        windowHeight = constants.CAMERA_HEIGHT

        # dimensions of our Button
        surfaceX, surfaceY = self.rect.topleft
        surfaceWidth, surfaceHeight = self.size
        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX_rel = mouseX - surfaceX
        mouseY_rel = mouseY - surfaceY
        mouseInSurface = (mouseX_rel >= 0 and
                          mouseY_rel >= 0 and
                          mouseX_rel <= surfaceWidth and
                          mouseY_rel <= surfaceHeight)
        return mouseInSurface

    def update(self, playerInput):
        buttonPressed = False
        if self.mouseInSurface:
            for event in playerInput:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        buttonPressed = True
        return buttonPressed

    def draw(self):
        if self.mouseInSurface:
            self.box_currentColor = self.box_mouseOverColor
            self.text_currentColor = self.text_mouseOverColor
        else:
            self.box_currentColor = self.box_colorDefault
            self.text_currentColor = self.text_colorDefault

        pygame.draw.rect(self.surface, self.box_currentColor, self.rect)
        drawText(self.surface,
                 self.buttonText,
                 T_coords = self.T_coordsCenter,
                 textColor = self.text_currentColor,
                 centered = True)

class ui_Slider:

    def __init__(self, destSurface, initValue, T_sliderCoords,
                 sliderLen,
                 sliderHeight = 25,
                 T_XYcorrection = (0, 0),
                 handle_buttonDownColor = constants.COLOR_RED,
                 handle_colorDefault = constants.COLOR_BLUE,
                 fill_color = constants.COLOR_GREEN,
                 empty_color = constants.COLOR_BLACK,
                 text = None):

        # where the slider will be blit'ed to
        self.destSurface = destSurface
        self.T_sliderCoords = T_sliderCoords
        self.sliderCoordsX, self.sliderCoordsY = T_sliderCoords

        # the scale of our slider
        self.initValue = .5
        self.currentValue = initValue

        # slider dimentions
        self.sliderLen = sliderLen
        self.sliderHeight = sliderHeight
        self.handleWidth = 10
        self.handleSize = (self.handleWidth, sliderHeight)

        # the surface of the slider
        self.notchBuffer = 0
        self.sliderSurface = pygame.Surface((sliderLen, sliderHeight + self.notchBuffer))
        self.handleSurface = pygame.Surface((self.handleSize))

        # topleft of the handle
        self.T_handleCoords = ((self.currentValue * self.sliderLen),
                                self.notchBuffer)
        self.handleCoordsX, self.handleCoordsY = self.T_handleCoords

        # center of the handle
        self.handleCoordsCenterX = self.handleCoordsX - (self.handleWidth // 2)
        self.handleCoordsCenterY = self.handleCoordsY + (self.sliderHeight // 2)
        self.T_handleCoordsCenter = self.handleCoordsCenterX, self.handleCoordsCenterY

        # callibrate the mousePos for the (x, y) of the sliderSurface
        self.T_XYcorrection = T_XYcorrection

        # highlighting
        self.handle_buttonDownColor = handle_buttonDownColor
        self.handle_colorDefault = handle_colorDefault
        self.handle_currentColor = handle_colorDefault
        self.fill_color = fill_color
        self.empty_color = empty_color

        # fill and empty rects
        self.fillRect = pygame.Rect((0, sliderHeight // 3), (self.sliderLen, self.sliderHeight // 3))
        self.fillRect.left = 0
        self.fillRect.right = self.sliderLen
        self.emptyRect = pygame.Rect((self.sliderLen, sliderHeight // 3), ((self.sliderLen), (self.sliderHeight // 3)))
        self.emptyRect.left = self.handleCoordsCenterX + (self.handleWidth // 2)

        # optional text
        self.text = text

    @property
    def mouseInSurface(self):
        # dimensions of our window
        windowWidth = constants.CAMERA_WIDTH
        windowHeight = constants.CAMERA_HEIGHT

        # dimensions of our handle
        handleX, handleY = self.T_handleCoords
        handleWidth, handleHeight = self.handleSize
        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        Xcorrect, Ycorrect = self.T_XYcorrection
        # Xcorrect += self.destSurface.width
        self.sliderXMouse = (mouseX) - Xcorrect
        self.sliderYMouse = (mouseY) - Ycorrect
        mouseInSurface = (self.sliderXMouse >= 0 and
                          self.sliderYMouse >= 0 and
                          self.sliderXMouse <= self.sliderLen and
                          self.sliderYMouse <= handleHeight)
        return mouseInSurface

    @property
    def buttonDown(self):
        buttonDown = pygame.mouse.get_pressed()[0]
        return buttonDown

    def draw(self):

        handleX, handleY = self.T_handleCoords
        handleXCenter, handleYCenter = self.T_handleCoordsCenter
        scale = (self.sliderLen - (self.handleWidth / 2))

        # if we have text, draw it 12 pixels above the sliderSurface
        if self.text:
            textX, textY = self.T_sliderCoords
            textY -= 10
            drawText(self.destSurface, self.text, (textX, textY), (constants.COLOR_GREY))

        # determine if we are dragging the handle
        if self.mouseInSurface:
            self.handle_currentColor = self.handle_colorDefault + pygame.Color(100, 100, 0)
            if self.buttonDown:
                # change color of handel to indicate the mouse button is down
                self.handle_currentColor = self.handle_buttonDownColor

                # what percentage of the slider is full
                self.currentValue = self.handleCoordsCenterX / scale
                self.currentValue = round(self.currentValue, 2)
                if not (self.sliderXMouse <= self.handleWidth // 2) and not (self.sliderXMouse >= scale):
                    if (self.sliderXMouse < self.sliderLen * .05) and not (self.sliderXMouse < 0):
                        self.handleCoordsX = 0
                        self.handleCoordsCenterX = self.handleCoordsX + (self.handleWidth // 2)
                    elif (self.sliderXMouse > self.sliderLen * .95) and (self.sliderXMouse > self.sliderLen):
                        self.handleCoordsX = self.sliderLen - (self.handleWidth // 2)
                    else:
                        self.T_handleCoords = (self.sliderXMouse - (self.handleWidth // 2), 0)
                        self.handleCoordsX, self.handleCoordsY = self.T_handleCoords
                        self.handleCoordsCenterX = self.handleCoordsX + (self.handleWidth // 2)
                # tie our empty rect to the handle
                self.emptyRect.left = self.handleCoordsCenterX
                self.fillRect.right = self.handleCoordsCenterX

                # change color of handel to indicate the mouse button is down
                self.handle_currentColor = self.handle_buttonDownColor
        else:
            self.handle_currentColor = self.handle_colorDefault

        # draw it all in the correct order

        self.sliderSurface.fill(constants.COLOR_DARK_GREY)
        self.handleSurface.fill(constants.COLOR_DARK_GREY)

        pygame.draw.rect(self.sliderSurface, self.fill_color, self.fillRect)
        pygame.draw.rect(self.sliderSurface, self.empty_color, self.emptyRect)

        pygame.draw.polygon(self.handleSurface, self.handle_currentColor,
                                            [ (0, (self.sliderHeight * .8) - 1),
                                              (1, self.sliderHeight * .8),
                                              (self.handleWidth - 2, self.sliderHeight * .8),
                                              (self.handleWidth, (self.sliderHeight * .8) - 2),
                                              (self.handleWidth, (self.sliderHeight * .15) + 1),
                                              (self.handleWidth - 2, (self.sliderHeight * .15)),
                                              (1, (self.sliderHeight * .15)),
                                              (0, (self.sliderHeight * .15) + 1) ])



        self.sliderSurface.blit(self.handleSurface, (self.handleCoordsX, self.handleCoordsY))
        self.destSurface.blit(self.sliderSurface, self.T_sliderCoords)



#    mmmmmmm    mmmmmmm       eeeeeeeeeeee    nnnn  nnnnnnnn    uuuuuu    uuuuuu
#  mm:::::::m  m:::::::mm   ee::::::::::::ee  n:::nn::::::::nn  u::::u    u::::u
# m::::::::::mm::::::::::m e::::::eeeee:::::een::::::::::::::nn u::::u    u::::u
# m::::::::::::::::::::::me::::::e     e:::::enn:::::::::::::::nu::::u    u::::u
# m:::::mmm::::::mmm:::::me:::::::eeeee::::::e  n:::::nnnn:::::nu::::u    u::::u
# m::::m   m::::m   m::::me:::::::::::::::::e   n::::n    n::::nu::::u    u::::u
# m::::m   m::::m   m::::me::::::eeeeeeeeeee    n::::n    n::::nu::::u    u::::u
# m::::m   m::::m   m::::me:::::::e             n::::n    n::::nu:::::uuuu:::::u
# m::::m   m::::m   m::::me::::::::e            n::::n    n::::nu:::::::::::::::uu
# m::::m   m::::m   m::::m e::::::::eeeeeeee    n::::n    n::::n u:::::::::::::::u
# m::::m   m::::m   m::::m  ee:::::::::::::e    n::::n    n::::n  uu::::::::uu:::u
# mmmmmm   mmmmmm   mmmmmm    eeeeeeeeeeeeee    nnnnnn    nnnnnn    uuuuuuuu  uuuu

def menu_main():

    gameInit()

    # Title surface dimentions
    titleSurfDimX = constants.CAMERA_WIDTH * 0.75
    titleSurfDimY = constants.CAMERA_HEIGHT * .5
    windowCenterX = constants.CAMERA_WIDTH * .5
    windowCenterY = constants.CAMERA_HEIGHT * .5
    titleSurfCenter = (titleSurfDimX // 2, titleSurfDimY // 2)
    titleSurfCenterX, titleSurfCenterY = titleSurfCenter
    titleSurfBottomY = titleSurfDimY + (windowCenterY * .125)

    # create title surface
    titleSurface = pygame.Surface((titleSurfDimX, titleSurfDimY))
    titleRectWidth, titleRectHeight = (260, 260)
    titleRectCenterX = titleRectWidth // 2
    titleRectCenterY = titleRectHeight // 2
    titleRectCenter = (titleRectCenterX, titleRectCenterY)
    titleRect = pygame.Rect((titleSurfCenterX - titleRectCenterX, titleSurfCenterY - titleRectCenterY),
                            (titleRectWidth, titleRectHeight))

    pygame.mixer.music.load(ASSETS.musicMain)
    pygame.mixer.music.play(-1)

    menuRunning = True

    buttonWidth = 200
    buttonHeight = 50
    newGameButton = ui_Button(SURFACE_MAIN,
                           'New Game',
                           (buttonWidth, buttonHeight),
                           (windowCenterX - (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 1.5)))

    loadGameButton = ui_Button(SURFACE_MAIN,
                           'Continue',
                           (buttonWidth, buttonHeight),
                           (windowCenterX + (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 1.5)))

    optionsButton = ui_Button(SURFACE_MAIN,
                           'Options',
                           (buttonWidth, buttonHeight),
                           (windowCenterX + (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 3)))
    quitGameButton = ui_Button(SURFACE_MAIN,
                           'Quit',
                           (buttonWidth, buttonHeight),
                           (windowCenterX - (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 3)))
    while menuRunning:
        eventsList = pygame.event.get()
        mousePosX, mousePosY = pygame.mouse.get_pos()

        menuInput = (eventsList)

        for event in eventsList:
            if event.type == pygame.QUIT:
                gameExit(save = False)

            if event.type == pygame.KEYDOWN:

                # quick quit
                if event.key == pygame.K_q:
                    gameExit(save = False)
        newGame = newGameButton.update(menuInput)
        loadGame = loadGameButton.update(menuInput)
        quit = quitGameButton.update(menuInput)
        options = optionsButton.update(menuInput)
        if newGame:
            pygame.mixer.music.stop()
            gameStart()
            break

        if loadGame:
            pygame.mixer.music.stop()
            gameStart(False)
            break

        if quit:
            pygame.quit()
            exit()
            break
        if options:
            menu_mainOptions()

        # draw menu
        SURFACE_MAIN.fill(constants.COLOR_BLACK)

        newGameButton.draw()
        loadGameButton.draw()
        optionsButton.draw()
        quitGameButton.draw()

        # update surface
        SURFACE_MAIN.blit(titleSurface,(windowCenterX * .25, windowCenterY * .125))
        titleSurface.fill(constants.COLOR_BLACK)
        pygame.draw.rect(titleSurface, constants.COLOR_BLACK, titleRect)
        titleSurface.blit(ASSETS.S_TITLE, titleRect, area = None)

        drawText(titleSurface,
                 "Python Roguelike Tutorial",
                 titleSurfCenter,
                 constants.COLOR_WHITE,
                 font = constants.FONT_TITLE_TEXT,
                 centered = True)

        pygame.display.update()
        # gameLoop()

def menu_mainOptions():
    # toggle the menu
    menuClose = False

    # dimensions of menu and main window
    windowWidth = constants.CAMERA_WIDTH
    windowHeight = constants.CAMERA_HEIGHT

    menuWidth = 400
    menuHeight = 400
    menuX = (windowWidth // 2) - (menuWidth // 2)
    menuY = (windowHeight // 2) - (menuHeight // 2)

    # font...
    menuFont = constants.FONT_DEBUG_MESSAGE
    textHeight = helperTextHeight(menuFont)
    menuTextColor = constants.COLOR_WHITE

    # Surface to draw onto
    optionsSurf = pygame.Surface((menuWidth, menuHeight))

    # FXSlider
    FXSlider = ui_Slider(optionsSurf,
                         initValue = PREF.FXVol,
                         T_sliderCoords = (menuWidth // 6, menuHeight // 6),
                         sliderLen = (menuWidth * 2) // 3,
                         T_XYcorrection = (menuX + (menuWidth // 6), menuY + (menuHeight // 6)),
                         text = 'Sound Effects')

    musicSlider = ui_Slider(optionsSurf,
                         initValue = PREF.musicVol,
                         T_sliderCoords = (menuWidth // 6, menuHeight // 3),
                         sliderLen = (menuWidth * 2) // 3,
                         T_XYcorrection = (menuX + (menuWidth // 6), menuY + (menuHeight // 3)),
                         text = 'Music')

    # your standard "while not" menu technique
    while not menuClose:

        # random = libtcod.random_get_int(0, 1, 1000)
        # print(str(PREF.musicVol))
        # if random == 999:
        #     menuClose=True

        # Clear the menu
        optionsSurf.fill(constants.COLOR_MENU)


        # generate a list of events (inputs)
        eventsList = pygame.event.get()

        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX_rel = mouseX - menuX
        mouseY_rel = mouseY - menuY
        mouseInMenu = (mouseX_rel >= 0 and
                       mouseY_rel >= 0 and
                       mouseX_rel <= menuWidth and
                       mouseY_rel <= menuHeight)
        mouseLineSelect = mouseY_rel // textHeight

        # iterate over the events list
        for event in eventsList:
            result = 'menu open'
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    prefSave()
                    result = 'canceled'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass

            if result == 'canceled' or not result:
                return 'no action'
            elif result == 'menu open':
                pass
            else:
                return 'result'


        # update the FX volume
        FXSlider.draw()
        PREF.FXVol = FXSlider.currentValue
        pygame.mixer.music.set_volume(PREF.FXVol)

        # update the music volume
        musicSlider.draw()
        PREF.musicVol = musicSlider.currentValue
        pygame.mixer.music.set_volume(PREF.musicVol)

        musicSlider.draw()

        SURFACE_MAIN.blit(optionsSurf,
                          (menuX, menuY))

        CLOCK.tick(constants.GAME_FPS)
        # actually draw everything
        pygame.display.update()

def menu_pause():

    # toggle variable
    menuClose = False

    # menu gui
    windowWidth = constants.CAMERA_WIDTH
    windowHeight = constants.CAMERA_HEIGHT
    menuText = "PAUSED"
    menuFont = constants.FONT_DEBUG_MESSAGE

    textWidth = len(menuText) * helperTextWidth(menuFont)
    textHeight = helperTextHeight(menuFont)

    # while menuClose is not True:
    while not menuClose:
        # creat a list of all the inputs (events) that happened this tick
        eventsList = pygame.event.get()
        # iterate over that list
        for event in eventsList:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_TAB:
                    menuClose = True

        drawText(SURFACE_MAIN, menuText,
                 T_coords=((windowWidth // 2) - (textWidth // 2),
                           (windowHeight // 2) - (textHeight // 2)),
                 textColor=constants.COLOR_WHITE, backColor=constants.COLOR_BLACK)

        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

def menu_inventory():

    # toggle the menu
    menuClose = False

    # dimensions of menu and main window
    windowWidth = constants.CAMERA_WIDTH
    windowHeight = constants.CAMERA_HEIGHT

    menuWidth = 200
    menuHeight = 200
    menuX = (windowWidth // 2) - (menuWidth // 2)
    menuY = (windowHeight // 2) - (menuHeight // 2)

    # font...
    menuFont = constants.FONT_DEBUG_MESSAGE
    textHeight = helperTextHeight(menuFont)
    menuTextColor = constants.COLOR_WHITE

    # Surface to draw onto
    localInventorySurf = pygame.Surface((menuWidth, menuHeight))

    # your standard "while not" menu technique
    while not menuClose:

        # Clear the menu
        localInventorySurf.fill(constants.COLOR_MENU)

        # generate a list of whats in the players inventory
        printList = [obj.displayName for obj in PLAYER.container.inventory]

        # generate a list of events (inputs)
        eventsList = pygame.event.get()

        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX_rel = mouseX - menuX
        mouseY_rel = mouseY - menuY
        mouseInMenu = (mouseX_rel >= 0 and
                       mouseY_rel >= 0 and
                       mouseX_rel <= menuWidth and
                       mouseY_rel <= menuHeight)
        mouseLineSelect = mouseY_rel // textHeight

        # iterate over the events list
        for event in eventsList:
            result = 'menu open'
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    result = 'canceled'
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if (mouseInMenu and
                            mouseLineSelect <= len(printList) - 1):

                        result = PLAYER.container.inventory[mouseLineSelect].item.use()


            if result == 'canceled' or not result:
                return 'no action'
            elif result == 'menu open':
                pass
            else:
                return 'result'

        # iterate and draw the inventory list
        line = 0
        for name in printList:
            # drawText(displaySurf,
                     # textToDisplay,
                     # T_coords,
                     # textColor,
                     # backColor = None):
            if line == mouseLineSelect and mouseInMenu:
                drawText(localInventorySurf,
                         name,
                         font=constants.FONT_MESSAGE_TEXT,
                         T_coords=(0, (0 + (line * textHeight))),
                         textColor=menuTextColor,
                         backColor=constants.COLOR_GREY)
            else:
                drawText(localInventorySurf,
                         name,
                         font=constants.FONT_MESSAGE_TEXT,
                         T_coords=(0, (0 + (line * textHeight))),
                         textColor=menuTextColor)
            line += 1

        '''
        This code is boilerplate menu code.
        drawGame ensures the animations continue
        - THEN -
        SURFACE_MAIN.blit puts our menu up on the screen
        - THEN -
        CLOCK.tick prevents the animations from backlogging
        - THEN -
        display.update
        '''
        drawGame()

        # blit our menu onto the main window and position it (center it)
        SURFACE_MAIN.blit(localInventorySurf,
                          (menuX, menuY))

        CLOCK.tick(constants.GAME_FPS)
        # actually draw everything
        pygame.display.update()

def menu_magic():

    # toggle the menu
    menuClose = False

    # dimensions of menu and main window
    windowWidth = constants.CAMERA_WIDTH
    windowHeight = constants.CAMERA_HEIGHT

    menuWidth = 200
    menuHeight = 200
    menuX = (windowWidth // 2) - (menuWidth // 2)
    menuY = (windowHeight // 2) - (menuHeight // 2)

    # font...
    menuFont = constants.FONT_MESSAGE_TEXT
    textHeight = helperTextHeight(menuFont)
    menuTextColor = constants.COLOR_WHITE

    # Surface to draw onto
    localMenuSurf = pygame.Surface((menuWidth, menuHeight))

    # your standard "while not" menu technique
    while not menuClose:

        # Clear the menu
        localMenuSurf.fill(constants.COLOR_MENU)

        # generate a list of whats in the players inventory
        # CHANGE
        printList = ['Look', 'Lightning', 'Fireball', 'Confuse']

        # generate a list of events (inputs)
        eventsList = pygame.event.get()

        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX_rel = mouseX - menuX
        mouseY_rel = mouseY - menuY
        mouseInMenu = (mouseX_rel >= 0 and
                       mouseY_rel >= 0 and
                       mouseX_rel <= menuWidth and
                       mouseY_rel <= menuHeight)
        mouseLineSelect = mouseY_rel // textHeight

        # iterate over the events list
        for event in eventsList:
            result = 'menu open'
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    result = 'canceled'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if (mouseInMenu and
                            mouseLineSelect <= len(printList) - 1):

                        if printList[mouseLineSelect] == 'Look':
                            result = cast_look()
                        if printList[mouseLineSelect] == 'Lightning':
                            result = cast_lightning(PLAYER)
                        if printList[mouseLineSelect] == 'Fireball':
                            result = cast_fireball(PLAYER)
                        if printList[mouseLineSelect] == 'Confuse':
                            result = cast_confusion()

            if result == 'canceled' or not result:
                return 'no action'
            elif result == 'menu open':
                pass
            else:
                return 'inventory use'
        # iterate and draw the inventory list
        line = 0
        for name in printList:
            # drawText(displaySurf,
                     # textToDisplay,
                     # T_coords,
                     # textColor,
                     # backColor = None):
            if line == mouseLineSelect and mouseInMenu:
                drawText(localMenuSurf,
                         name,
                         font=constants.FONT_MESSAGE_TEXT,
                         T_coords=(0, (0 + (line * textHeight))),
                         textColor=menuTextColor,
                         backColor=constants.COLOR_GREY)
            else:
                drawText(localMenuSurf,
                         name,
                         font=constants.FONT_MESSAGE_TEXT,
                         T_coords=(0, (0 + (line * textHeight))),
                         textColor=menuTextColor)
            line += 1

        '''
        This code is boilerplate menu code.
        drawGame ensures the animations continue
        - THEN -
        SURFACE_MAIN.blit puts our menu up on the screen
        - THEN -
        CLOCK.tick prevents the animations from backlogging
        - THEN -
        display.update
        '''
        drawGame()

        # blit our menu onto the main window and position it (center it)
        SURFACE_MAIN.blit(localMenuSurf,
                          (menuX, menuY))

        CLOCK.tick(constants.GAME_FPS)
        # actually draw everything
        pygame.display.update()

def menu_tileSelect(localAlpha=40, tileColor=constants.COLOR_BLACK):
    ''' this menu lets a player select a tile

    this function pauses the game, produces an on-screen rectangle that follows
    the mouse, and returns the map address when the left mouse button is clicked
    '''
    menuClose = False

    while not menuClose:
        # get mouse x, y pose
        mouseX, mouseY = pygame.mouse.get_pos()

        # convert our real x, y to the map tile x, y
        mapXPixel, mapYPixel = CAMERA.winToMap((mouseX, mouseY))

        mapCoordsX = mapXPixel // constants.CELL_WIDTH
        mapCoordsY = mapYPixel // constants.CELL_HEIGHT

        # generate a list of events (inputs)
        eventsList = pygame.event.get()

        # cancel
        for event in eventsList:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    menuClose = True
                    return 'canceled'

            # return map coords when mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    coords = (mapCoordsX, mapCoordsY)
                    return coords
        # Draw game first
        # clear screen
        SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        SURFACE_MAP.fill(constants.COLOR_MAP_FOG)

        # update possition of camera
        CAMERA.update()

        # draw map
        drawMap(GAME.currentMap)

        # draw actors
        for obj in sorted(GAME.currentObj, key = lambda obj: obj.depth, reverse = True):
            obj.draw()

        # draw a rectangle at mouse on top of game

        drawTileRect((mapCoordsX, mapCoordsY), rectColor=tileColor, mark='X')

        # return the map address

        # keep the animations going
        CLOCK.tick(constants.GAME_FPS)

        SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

        drawDebug()
        drawMessages()

        pygame.display.flip()

def menu_tileSelectLine(coordsOrigin,
                        range=None,
                        hasRadius=False,
                        radiusValue=None,
                        radiusColor=None,
                        radiusAlpha=None,
                        penetrateWalls=True,
                        penetrateCreatures=True,
                        lineColor=constants.COLOR_BLACK,
                        lineAlpha=None):
    ''' this menu lets a player select a tile showing the line of sight

    this function pauses the game, produces an on-screen rectangle that follows
    the mouse, and returns the map address when the left mouse button is clicked

    if mouse button 1 is clicked:
        returns a tuple of the selected (x, y) and
                a list of (x, y) between selected and origin
    if 'c' is pressed:
        returns string 'canceled' and
        None

    '''
    range -= 1
    menuClose = False

    while not menuClose:
        # get mouse x, y pose
        mouseX, mouseY = pygame.mouse.get_pos()

        # convert our real x, y to the map tile x, y
        mapXPixel, mapYPixel = CAMERA.winToMap((mouseX, mouseY))

        mapCoordsX = mapXPixel // constants.CELL_WIDTH
        mapCoordsY = mapYPixel // constants.CELL_HEIGHT

        # generate a list of events (inputs)
        eventsList = pygame.event.get()

        # Draw game first
        # clear screen
        SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
        SURFACE_MAP.fill(constants.COLOR_MAP_FOG)

        # update possition of camera
        CAMERA.update()

        # draw map
        drawMap(GAME.currentMap)

        # draw actors
        for obj in sorted(GAME.currentObj, key = lambda obj: obj.depth, reverse = True):
            obj.draw()

        # draw a rectangle at mouse on top of game

        lineList = []
        rangeList = []

        lineIter = mapFindLine(coordsOrigin, (mapCoordsX, mapCoordsY))
        for i in lineIter:
            lineList.append(i)

        # if there is a range, this shortens the list
        i = 0
        for x, y in lineList:
            rangeList.append(lineList[i])
            # stop at walls
            if (not penetrateWalls) and mapCheckForWall(x, y):
                break
            # stop at creatures
            if (not penetrateCreatures) and (mapCheckForCreature(x, y) != None):
                break
            if range and i == range:
                break

            i += 1

        # cancel
        for event in eventsList:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    menuClose = True
                    return 'canceled', None

            # return map coords when mouse pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menuClose = True
                    # returns coords selected
                    if range:
                        return (mapCoordsX, mapCoordsY), rangeList
                    else:
                        return (mapCoordsX, mapCoordsY), None

        for x, y in rangeList:
            if (x, y) != (coordsOrigin):
                if (x, y) == rangeList[-1]:
                    drawTileRect((x, y), rectAlpha=lineAlpha, rectColor=lineColor, mark='X')
                else:
                    drawTileRect((x, y), rectAlpha=lineAlpha, rectColor=lineColor)

        if hasRadius:
            radiusList = mapFindRadius((rangeList[-1]), radiusValue)
            for (xr, yr) in radiusList:
                drawTileRect((xr, yr), rectAlpha=radiusAlpha, rectColor=radiusColor)

        # keep the animations going
        CLOCK.tick(constants.GAME_FPS)

        SURFACE_MAIN.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)

        drawDebug()
        drawMessages()

        pygame.display.flip()

#                                                                                                                           tttt
#                                                                                                                        ttt:::t
#                                                                                                                        t:::::t
#                                                                                                                        t:::::t
#    ggggggggg   ggggg    eeeeeeeeeeee    nnnn  nnnnnnnn        eeeeeeeeeeee    rrrrr   rrrrrrrrr   aaaaaaaaaaaaa  ttttttt:::::ttttttt       ooooooooooo
#   g:::::::::ggg::::g  ee::::::::::::ee  n:::nn::::::::nn    ee::::::::::::ee  r::::rrr:::::::::r  a::::::::::::a t:::::::::::::::::t     oo:::::::::::oo
#  g:::::::::::::::::g e::::::eeeee:::::een::::::::::::::nn  e::::::eeeee:::::eer:::::::::::::::::r aaaaaaaaa:::::at:::::::::::::::::t    o:::::::::::::::o
# g::::::ggggg::::::gge::::::e     e:::::enn:::::::::::::::ne::::::e     e:::::err::::::rrrrr::::::r         a::::atttttt:::::::tttttt    o:::::ooooo:::::o
# g:::::g     g:::::g e:::::::eeeee::::::e  n:::::nnnn:::::ne:::::::eeeee::::::e r:::::r     r:::::r  aaaaaaa:::::a      t:::::t          o::::o     o::::o
# g:::::g     g:::::g e:::::::::::::::::e   n::::n    n::::ne:::::::::::::::::e  r:::::r     rrrrrrraa::::::::::::a      t:::::t          o::::o     o::::o
# g:::::g     g:::::g e::::::eeeeeeeeeee    n::::n    n::::ne::::::eeeeeeeeeee   r:::::r           a::::aaaa::::::a      t:::::t          o::::o     o::::o
# g::::::g    g:::::g e:::::::e             n::::n    n::::ne:::::::e            r:::::r          a::::a    a:::::a      t:::::t    tttttto::::o     o::::o
# g:::::::ggggg:::::g e::::::::e            n::::n    n::::ne::::::::e           r:::::r          a::::a    a:::::a      t::::::tttt:::::to:::::ooooo:::::o
#  g::::::::::::::::g  e::::::::eeeeeeee    n::::n    n::::n e::::::::eeeeeeee   r:::::r          a:::::aaaa::::::a      tt::::::::::::::to:::::::::::::::o
#   gg::::::::::::::g   ee:::::::::::::e    n::::n    n::::n  ee:::::::::::::e   r:::::r           a::::::::::aa:::a       tt:::::::::::tt oo:::::::::::oo
#     gggggggg::::::g     eeeeeeeeeeeeee    nnnnnn    nnnnnn    eeeeeeeeeeeeee   rrrrrrr            aaaaaaaaaa  aaaa         ttttttttttt     ooooooooooo
#             g:::::g
# gggggg      g:::::g
# g:::::gg   gg:::::g
#  g::::::ggg:::::::g
#   gg:::::::::::::g
#     ggg::::::ggg
#        gggggg


# SPECIAL
def gen_player(T_coords):

    global PLAYER
    x, y = T_coords

    containerCom = com_Container()

    creatureCom = com_Creature("greg", baseAtk=4, faction='player')

    PLAYER = obj_Actor(x, y, "python",
                       animationKey = "A_PLAYER",
                       depth = constants.DEPTH_PLAYER,
                       animationSpeed=1,
                       creature=creatureCom,
                       container=containerCom)

    GAME.currentObj.append(PLAYER)

def gen_stairs(T_coords, downwards = True):
    x, y = T_coords

    if downwards:
        stairs_com = com_Stairs()
        stairs = obj_Actor(x, y, 'stairs',
                  animationKey = "S_STAIRS_DOWN",
                  stairs = stairs_com,
                  depth = constants.DEPTH_DECOR)

    else:
        stairs_com = com_Stairs(downwards = False)
        stairs = obj_Actor(x, y, 'stairs',
                           animationKey = "S_STAIRS_UP",
                           stairs = stairs_com,
                           depth = constants.DEPTH_DECOR)


    GAME.currentObj.append(stairs)
# ITEMS
def gen_item(T_coords):
    ranNum = libtcod.random_get_int(0, 1, 5)

    if ranNum == 1: newItem = gen_scroll_lightning(T_coords)
    elif ranNum == 2: newItem = gen_scroll_fireball(T_coords)
    elif ranNum == 3: newItem = gen_scroll_confusion(T_coords)
    elif ranNum == 4: newItem = gen_weapon(T_coords)
    elif ranNum == 5: newItem = gen_armor_shield(T_coords)

    GAME.currentObj.append(newItem)

def gen_weapon(T_coords):
    x, y = T_coords
    ranBonus = libtcod.random_get_int(0, 1, 3)
    name = '+' + str(ranBonus) + ' Sword'
    equipmentCom = com_Equipment(attackBonus=ranBonus)
    returnObj = obj_Actor(x, y,
                          name,
                          depth = constants.DEPTH_ITEM,
                          animationKey = "S_SWORD",
                          equipment = equipmentCom)
    return returnObj

def gen_armor_shield(T_coords):
    x, y = T_coords
    ranBonus = libtcod.random_get_int(0, 1, 3)
    name = '+' + str(ranBonus) + ' Shield'

    equipmentCom = com_Equipment(defenseBonus=ranBonus)
    returnObj = obj_Actor(x, y,
                          name,
                          depth = constants.DEPTH_ITEM,
                          animationKey = "S_SHIELD",
                          equipment = equipmentCom)
    return returnObj

def gen_scroll_lightning(T_coords):

    x, y = T_coords

    damage = libtcod.random_get_int(0, 5, 7)
    maxRange = libtcod.random_get_int(0, 4, 6)

    item_com = com_Item(useFunc = cast_lightning, value=(damage, maxRange))

    returnObject = obj_Actor(x, y,
                             nameObject='Lightning Scroll',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_SCROLL_01",
                             item=item_com)

    return returnObject

def gen_scroll_fireball(T_coords):

    x, y = T_coords

    damage = libtcod.random_get_int(0, 2, 4)
    maxRange = libtcod.random_get_int(0, 5, 8)
    radius = 1

    item_com = com_Item(useFunc = cast_fireball, value=(damage, radius, maxRange))

    returnObject = obj_Actor(x, y,
                             nameObject='Fireball Scroll',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_SCROLL_02",
                             item=item_com)

    return returnObject

def gen_scroll_confusion(T_coords):

    x, y = T_coords

    numTurns = libtcod.random_get_int(0, 2, 8)

    item_com = com_Item(useFunc = cast_confusion, value=numTurns)

    returnObject = obj_Actor(x, y,
                             nameObject='Confusion Scroll',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_SCROLL_03",
                             item=item_com)

    return returnObject

# gen enemies

def gen_enemy(T_coords):
    ranNum = libtcod.random_get_int(0, 1, 100)

    if ranNum <= 15:
        newEnemy = gen_snake_cobra(T_coords)
    else:
        newEnemy = gen_snake_anaconda(T_coords)

    GAME.currentObj.append(newEnemy)

def gen_snake_anaconda(T_coords):
    ranNum = libtcod.random_get_int(0, 1, 100)

    if ranNum <= 25:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 3, 5)
        baseAttack = libtcod.random_get_int(0 , 1, 1)
        nutrition = libtcod.random_get_int(0, 1, 2)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    faction = 'neonates',
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_anaconda = obj_Actor(x, y, "neonates anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_01",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)
    elif ranNum >= 26 and ranNum <= 75:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 7, 10)
        baseAttack = libtcod.random_get_int(0 , 3, 4)
        nutrition = libtcod.random_get_int(0, 3, 4)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_anaconda = obj_Actor(x, y, "snakelet anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)
    else:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 10, 15)
        baseAttack = libtcod.random_get_int(0 , 4, 5)
        nutrition = libtcod.random_get_int(0, 4, 6)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_anaconda = obj_Actor(x, y, "anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_03",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)

    return snake_anaconda

def gen_snake_cobra(T_coords):
    ranNum = libtcod.random_get_int(0, 1, 100)

    if ranNum <= 25:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 1, 3)
        baseAttack = libtcod.random_get_int(0 , 2, 3)
        nutrition = libtcod.random_get_int(0, 1, 1)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    faction = 'neonates',
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_cobra = obj_Actor(x, y, "neonates cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_01",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)
    elif ranNum >= 26 and ranNum <= 75:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 5, 8)
        baseAttack = libtcod.random_get_int(0 , 3, 5)
        nutrition = libtcod.random_get_int(0, 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_cobra = obj_Actor(x, y, "snakelet cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)
    else:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 8, 11)
        baseAttack = libtcod.random_get_int(0 , 4, 7)
        nutrition = libtcod.random_get_int(0, 3, 4)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake)
        aiCom = ai_chase()
        itemCom = com_Item(useFunc=cast_heal, value=nutrition)
        snake_cobra = obj_Actor(x, y, "cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_03",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom,
                                   item=itemCom)

    return snake_cobra












#    ggggggggg   ggggg aaaaaaaaaaaaa      mmmmmmm    mmmmmmm       eeeeeeeeeeee
#   g:::::::::ggg::::g a::::::::::::a   mm:::::::m  m:::::::mm   ee::::::::::::ee
#  g:::::::::::::::::g aaaaaaaaa:::::a m::::::::::mm::::::::::m e::::::eeeee:::::ee
# g::::::ggggg::::::gg          a::::a m::::::::::::::::::::::me::::::e     e:::::e
# g:::::g     g:::::g    aaaaaaa:::::a m:::::mmm::::::mmm:::::me:::::::eeeee::::::e
# g:::::g     g:::::g  aa::::::::::::a m::::m   m::::m   m::::me:::::::::::::::::e
# g:::::g     g:::::g a::::aaaa::::::a m::::m   m::::m   m::::me::::::eeeeeeeeeee
# g::::::g    g:::::ga::::a    a:::::a m::::m   m::::m   m::::me:::::::e
# g:::::::ggggg:::::ga::::a    a:::::a m::::m   m::::m   m::::me::::::::e
#  g::::::::::::::::ga:::::aaaa::::::a m::::m   m::::m   m::::m e::::::::eeeeeeee
#   gg::::::::::::::g a::::::::::aa:::am::::m   m::::m   m::::m  ee:::::::::::::e
#     gggggggg::::::g  aaaaaaaaaa  aaaammmmmm   mmmmmm   mmmmmm    eeeeeeeeeeeeee
#             g:::::g
# gggggg      g:::::g
# g:::::gg   gg:::::g
#  g::::::ggg:::::::g
#   gg:::::::::::::g
#     ggg::::::ggg
#        gggggg


def gameInit():
    # this function sets up the main window and pygame

    global SURFACE_MAIN, SURFACE_MAP
    global CLOCK, FOV_CALC, ENEMY, ASSETS, PREF, CAMERA, RANDOM_ENGINE

    # initialiaze pygame
    pygame.init()

    # allows us to hold a key down for rapid input
    pygame.key.set_repeat(200, 70)

    # initialize preferences
    try:
        prefLoad()
    except:
        PREF = struc_Preferences()
        prefSave()

    # SURFACE_MAIN is a speacial surface. It represents the game console. Anything
    # that appears in the game, must be displayed here
    SURFACE_MAIN = pygame.display.set_mode((constants.CAMERA_WIDTH,
                                           constants.CAMERA_HEIGHT))
    # sets up our map surface and camera
    SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))
    CAMERA = obj_Camera()

    # initialize the RANDOM number ENGINE
    RANDOM_ENGINE = random.SystemRandom()

    # load in all out namegen files
    libtcod.namegen_parse(constants.PATH + "data/namegen/jice_celtic.cfg")

    # load in our assets
    ASSETS = obj_Assets()

    # start the clock
    CLOCK = pygame.time.Clock()
    FOV_CALC = True

def gameStart(new=True):
    if not new:
        gameLoad()
    else:
        # start a new game
        gameNew()
    gameLoop()

def gameNew():
    global GAME
    # starts a new game and map
    pygame.mixer.music.load(ASSETS.musicBkg)
    pygame.mixer.music.play(-1)

    GAME = obj_Game()
    gen_player((0, 0))
    mapPlaceObjects(GAME.roomList)

def gameLoad():
    global GAME, PLAYER

    with gzip.open(constants.PATH + 'data/savegame', 'rb') as file:
        GAME, PLAYER = pickle.load(file)

    for obj in GAME.currentObj:
        obj.animationInit()

    mapMakeFOV(GAME.currentMap)

def gameSave(save = True):

    if save:
        for obj in GAME.currentObj:
            obj.animationDestroy()
        # saves
        with gzip.open(constants.PATH + 'data/savegame', 'wb') as file:
            pickle.dump([GAME, PLAYER],file)
    else:
        pass

def prefSave():
    with open(constants.PATH + 'data/pref', 'wb') as file:
        pickle.dump([PREF], file)


def prefLoad():
    global PREF

    with open(constants.PATH + 'data/pref', 'rb') as file:
        temp = pickle.load(file)
        PREF = temp[0]

def gameExit(save = True):

    gameSave(save)
    # out of the game loop
    pygame.quit()
    exit()

def gameHandleKeys():
    global FOV_CALC
    # TODO gets all player inputs and makes a list out of them
    eventsList = pygame.event.get()
    keysList = pygame.key.get_pressed()

    #check for mod key
    modKey = (keysList[pygame.K_RSHIFT] or
              keysList[pygame.K_LSHIFT])

    for event in eventsList:
        if event.type == pygame.QUIT:
            return 'QUIT'

        if event.type == pygame.KEYDOWN:

            # quick quit
            if event.key == pygame.K_q:
                gameExit()

            # movement keys (arrows)
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALC = True
                return 'player moved'
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALC = True
                return 'player moved'
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALC = True
                return 'player moved'
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALC = True
                return 'player moved'

            # movement keys (numpad)
            # up
            if event.key == pygame.K_p:
                PLAYER.creature.move(0, -1)
                FOV_CALC = True
                return 'player moved'
            # down
            if event.key == pygame.K_PERIOD:
                PLAYER.creature.move(0, 1)
                FOV_CALC = True
                return 'player moved'
            # left
            if event.key == pygame.K_l:
                PLAYER.creature.move(-1, 0)
                FOV_CALC = True
                return 'player moved'
            # right
            if event.key == pygame.K_QUOTE:
                PLAYER.creature.move(1, 0)
                FOV_CALC = True
                return 'player moved'
            # up-right
            if event.key == pygame.K_LEFTBRACKET:
                PLAYER.creature.move(1, -1)
                FOV_CALC = True
                return 'player moved'
            # down-right
            if event.key == pygame.K_SLASH:
                PLAYER.creature.move(1, 1)
                FOV_CALC = True
                return 'player moved'
            # down-left
            if event.key == pygame.K_COMMA:
                PLAYER.creature.move(-1, 1)
                FOV_CALC = True
                return 'player moved'
            # up-left
            if event.key == pygame.K_o:
                PLAYER.creature.move(-1, -1)
                FOV_CALC = True
                return 'player moved'
            # wait
            if not modKey and event.key == pygame.K_SEMICOLON:
                objectsAtPlayer = mapAtCoords(PLAYER.x, PLAYER.y)

                for obj in objectsAtPlayer:
                    if obj.item:
                        obj.item.pickUp(PLAYER)
                return 'player picked-up'
            # item interaction keys
            # key 'g' -> "get" (pick-up item)
            if event.key == pygame.K_g:
                objectsAtPlayer = mapAtCoords(PLAYER.x, PLAYER.y)

                for obj in objectsAtPlayer:
                    if obj.item:
                        obj.item.pickUp(PLAYER)
                return 'player picked-up'
            # key 'd' -> "drop" (drop item)
            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)
            # hard-coded magic
            if event.key == pygame.K_BACKQUOTE:
                cast_look()
            if event.key == pygame.K_1:
                cast_lightning((PLAYER.x, PLAYER.y))
            if event.key == pygame.K_2:
                cast_fireball((PLAYER.x, PLAYER.y))
            if event.key == pygame.K_3:
                cast_confusion()
            # map testing
            if event.key == pygame.K_4:
                GAME.transitionNextMap()
            if event.key == pygame.K_5:
                GAME.transitionPreviousMap()
            if modKey and event.key == pygame.K_SEMICOLON:
                objectsAtPlayer = mapAtCoords(PLAYER.x, PLAYER.y)

                for obj in objectsAtPlayer:
                    if obj.stairs:
                        obj.stairs.use()

            # menu keys
            if event.key == pygame.K_TAB:
                menu_pause()
            # key 'c' -> "cast"
            if event.key == pygame.K_c:
                playerAction = menu_magic()
                return playerAction
            if event.key == pygame.K_i:
                playerAction = menu_inventory()
                return playerAction

    return 'no action'

def gameMessage(gameMsg, msgColor=constants.COLOR_GREY):
    GAME.msgHistory.append((gameMsg, msgColor))

def gameLoop():
    # now for the game loop, each iteration of which is a turn. If we were real-time, it would be a frame
    gameQuit = False

    # 'no action' means we are afk
    playerAction = 'no action'

    # the Game Loop
    while not gameQuit:

        # the loop constantly listens for key strokes
        playerAction = gameHandleKeys()

        mapCalcFOV()

        # if we 'x-out' the window, quit
        if playerAction == 'QUIT':
            gameQuit = True

        # if we have taken our turn (NOT do nothing), everything else takes it's turn
        elif playerAction != 'no action':
            for obj in GAME.currentObj:
                if obj.ai:
                    obj.ai.takeTurn()

        # Update our display to reflect what has changed
        drawGame()

        # tick the clock
        CLOCK.tick(constants.GAME_FPS)


if __name__ == '__main__':
    menu_main()
