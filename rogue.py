# 3rd party moduals

import pygame
import tcod as libtcod
import math
import pickle
import gzip
import random
import datetime
import os
from queue import PriorityQueue

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
        self.explorable = False
        self.assignment = 0

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
                 state = None,
                 animationSpeed=None,
                 scentStrength = None,
                 creature=None,
                 ai=None,
                 container=None,
                 item=None,
                 spellBook=None,
                 equipment=None,
                 stairs = None,
                 exitPortal = None,
                 info = 'no info available'):

        self.x = x  # map address
        self.y = y  # map address
        self.nameObject = nameObject  # instance name
        self.animationKey = animationKey
        self.animation = ASSETS.animationDict[self.animationKey]  # list of images
        self.depth = depth # where in the draw order
        self.state = state # state of actor (ex, STATUS_DEAD)
        self.animationSpeed = animationSpeed  # in seconds
        self.spriteImage = 0  # index number of self.animation
        self.scentStrength = scentStrength

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

        self.exitPortal = exitPortal
        if self.exitPortal:
            self.exitPortal.owner = self

        self.info = info

    @property
    def relX(self):
        x = self.x * constants.CELL_WIDTH
        return x

    @property
    def relY(self):
        y = self.y * constants.CELL_HEIGHT
        return y

    def draw(self):

        isVisible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if isVisible:

            # if self.animation is just 1 image, blit it. No animation code
            if self.animationSpeed == None and self.animation != 'None':
                SURFACE_MAP.blit(
                    self.animation, (self.x * constants.CELL_WIDTH,
                                     self.y * constants.CELL_HEIGHT))

            # if self.animation is multiple images, animate them
            elif len(self.animation) > 1 and self.animation != 'None':

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

            # if health is not full, draw the HP bar
            HPfillBarX = constants.CELL_WIDTH * .1
            HPfillBarY = constants.CELL_HEIGHT * .9
            HPfillBarWidth = constants.CELL_WIDTH * .9
            HPfillBarHeight = 3
            MPfillBarX = HPfillBarX
            MPfillBarY = HPfillBarY + HPfillBarHeight + 2
            MPfillBarWidth = HPfillBarWidth
            MPfillBarHeight = HPfillBarHeight

            if self.creature:
                if self.creature.currentHP != self.creature.maxHP:
                    healthBar = ui_FillBar(SURFACE_MAP,
                                           (self.relX + HPfillBarX, self.relY + HPfillBarY),
                                           self.creature.currentHP,
                                           self.creature.maxHP,
                                           HPfillBarWidth,
                                           HPfillBarHeight)
                    healthBar.draw(healthBar.T_coords)

                # if health is not full, draw the MP bar
                if self.creature.currentMP != self.creature.maxMP:

                    magicBar = ui_FillBar(SURFACE_MAP,
                                           (self.relX + MPfillBarX, self.relY + MPfillBarY),
                                           self.creature.currentMP,
                                           self.creature.maxMP,
                                           MPfillBarWidth,
                                           MPfillBarHeight,
                                           fillColor = constants.COLOR_CYAN,
                                           emptyColor = constants.COLOR_DARK_BLUE)
                    magicBar.draw(magicBar.T_coords)

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

        # this uses some of dijkstra's shortest path algorithim, but not all of it
        # we only find the best move adjacent to the actor
        # my main foucus here was preventing the MOBs from getting stuck on walls

        # make a list of all possible adjacent moves (9, including not moving)
        adjacencyList = []
        for x in range(1, 4):
            for y in range(1, 4):
                adjacencyList.append((x - 2, y - 2))

        # initialiaze the priority Queue
        pq = PriorityQueue()

        # calculate the distance for everything in adjacencyList
        for neighbor in adjacencyList:
            # seperate out the neighbor's tuple values
            nx, ny = neighbor

            ## calculate the euclidian distance ( Z = hypotenuse of a right triangle)
            # length of 1 side of our right triangle (side X)
            dx = other.x - (self.x + nx)

            # length of the other side (side Y)
            dy = other.y - (self.y + ny)

            # X^2 + Y^2 = Z^2 -->
            # the square root of Z^2 is the distance from self to other
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # If the neighboring tile is a wall, dont add it to PQ
            if not GAME.currentMap[self.x + nx][self.y + ny].blockPath:
                pq.put((distance, neighbor))

        # seperate out the tuple .get gives us
        priority, move = pq.get_nowait()

        # seperate out the tuple for our coords
        mx, my = move

        # now the creature moves
        self.creature.move(mx, my)

    def animationDestroy(self):
        self.animation = None

    def animationInit(self):
        self.animation = ASSETS.animationDict[self.animationKey]

    def decay(self):
        self.scentStrength -= 1
        if self.scentStrength <= 0:
            GAME.currentObj.remove(self)

class obj_Game:
    # this class is used to consolidate global game variables
    def __init__(self):
        self.msgHistory = []
        self.currentObj = []
        self.previousMaps = []
        self.nextMaps = []

        self.currentMap = "currentMap"
        self.roomList = "roomList"

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
                         'm': 13, 'n': 14, 'o': 15, 'p': 16,
                         'q': 17, 'r': 18, 's': 19, 't': 20,
                         'u': 21, 'v': 22, 'w': 23, 'x': 24,
                         'y': 25, 'z': 26, '0': 0}
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
        # this centers the camera on the center of the player
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
        # player
        self.player = obj_Spritesheet(constants.PATH + 'data/graphics/Characters/Player.png')
        # creatures
        self.humanoid = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Humanoid.png")
        self.pest = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Pest.png")
        self.rodent = obj_Spritesheet(constants.PATH + 'data/graphics/Characters/Rodent.png')
        self.reptile = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Reptile.png")
        self.aquatic = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Aquatic.png")
        self.flesh = obj_Spritesheet(constants.PATH + "data/graphics/Items/Flesh.png")
        self.plant = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Plant.png")
        self.undead = obj_Spritesheet(constants.PATH + "data/graphics/Characters/Undead.png")
        #walls and floors
        self.wall = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Wall.png")
        self.floor = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Floor.png")
        self.tile = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Tile.png")
        self.door = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Door.png")
        #decor
        self.decor = obj_Spritesheet(constants.PATH + "data/graphics/Objects/Decor.png")
        #equipment
        self.shortWep = obj_Spritesheet(constants.PATH + "data/graphics/Items/ShortWep.png")
        self.mediumWep = obj_Spritesheet(constants.PATH + "data/graphics/Items/MedWep.png")
        self.longWep = obj_Spritesheet(constants.PATH + "data/graphics/Items/LongWep.png")
        self.shield = obj_Spritesheet(constants.PATH + "data/graphics/Items/Shield.png")
        #items
        self.scroll = obj_Spritesheet(constants.PATH + "data/graphics/Items/Scroll.png")
        self.tool = obj_Spritesheet(constants.PATH + "data/graphics/Items/Tool.png")
        self.amulet = obj_Spritesheet(constants.PATH + "data/graphics/Items/Amulet.png")
        self.potion = obj_Spritesheet(constants.PATH + "data/graphics/Items/Potion.png")
        # GUI
        self.gui = obj_Spritesheet(constants.PATH + "data/graphics/GUI/GUI.png")


        ################
        ## ANIMATIONS ##
        ################

        # title
        # image.blit(self.spriteSheet, (0, 0),
        #            (self.tileDict[column] * width, row * height, width, height))
        self.S_TITLE = self.title.getImage('0', 0, 260, 260)[0]

        self.A_PLAYER = self.player.getAnimation('a', 4, 16, 16, 2, (32, 32))

        # reptiles
        self.A_SNAKE_GREEN_01 = self.reptile.getAnimation('m', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_GREEN_02 = self.reptile.getAnimation('o', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_ANACONDA_01 = self.reptile.getAnimation('a', 5, 16, 16, 2, (16, 16))
        self.A_SNAKE_ANACONDA_02 = self.reptile.getAnimation('c', 5, 16, 16, 2, (24, 24))
        self.A_SNAKE_ANACONDA_03 = self.reptile.getAnimation('e', 5, 16, 16, 2, (32, 32))
        self.A_SNAKE_COBRA_01 = self.reptile.getAnimation('g', 5, 16, 16, 2, (16, 16))
        self.A_SNAKE_COBRA_02 = self.reptile.getAnimation('i', 5, 16, 16, 2, (24, 24))
        self.A_SNAKE_COBRA_03 = self.reptile.getAnimation('k', 5, 16, 16, 2, (32, 32))

        # insect
        self.A_SPIDER_TARANTULA = self.pest.getAnimation('c', 3, 16, 16, 2, (32, 32))
        self.A_SPIDER_TARANTULA_GIANT_ZOMBIE = self.pest.getAnimation('e', 3, 16, 16, 2, (32, 32))
        self.A_SNAIL = self.pest.getAnimation('g', 8, 16, 16, 2, (32, 32))

        # humanoids
        self.A_ALCHEMIST = self.humanoid.getAnimation('a', 16, 16, 16, 2, (32, 32))

        # undead
        self.A_DEATH_CRACK = self.undead.getAnimation('g', 5, 16, 16, 2, (32, 32))

        # rodent
        self.A_MOUSE = self.rodent.getAnimation('a', 2, 16, 16, 2, (32, 32))
        self.A_RAT = self.rodent.getAnimation('c', 2, 16, 16, 2, (32, 32))
        self.A_GIANT_RAT = self.rodent.getAnimation('e', 2, 16, 16, 2, (32, 32))
        self.A_UNDEAD_RAT = self.rodent.getAnimation('g', 2, 16, 16, 2, (32, 32))
        self.A_POISON_RAT = self.rodent.getAnimation('a', 3, 16, 16, 2, (32, 32))
        self.A_HUNTER_RAT = self.rodent.getAnimation('c', 3, 16, 16, 2, (32, 32))

        # plants
        self.A_FERNOID = self.plant.getAnimation('a', 6, 16, 16, 2, (32, 32))

        # corpse
        self.S_FLESH_TAIL = self.flesh.getImage('b', 4, 16, 16, (32, 32))[0]
        self.S_FLESH_TAIL_SMALL = self.flesh.getImage('b', 4, 16, 16, (16, 16))[0]
        # flesh
        self.S_FLESH_CORPSE_DEFAULT_01 = self.flesh.getImage('d', 1, 16, 16, (24, 24))[0]
        self.S_FLESH_CORPSE_DEFAULT_02 = self.flesh.getImage('d', 5, 16, 16, (24, 24))[0]
        # bones
        self.S_FLESH_CORPSE_DEFAULT_03 = self.decor.getImage('c', 13, 16, 16, (24, 24))[0]
        self.S_FLESH_CORPSE_DEFAULT_04 = self.decor.getImage('c', 14, 16, 16, (24, 24))[0]
        # human skull
        self.S_FLESH_CORPSE_DEFAULT_05 = self.decor.getImage('a', 13, 16, 16, (24, 24))[0]


        self.S_FLOOR = self.floor.getImage('b', 8, 16, 16, (32, 32))[0]
        self.S_FLOOR_EXPLORED = self.floor.getImage('b', 14, 16, 16, (32, 32))[0]

        self.S_DOOR_CLOSED = self.door.getImage('a', 1, 16, 16, (32, 32))[0]
        self.S_DOOR_OPEN = self.door.getImage('b', 1, 16, 16, (32, 32))[0]
        self.A_PORTAL_OPEN = self.door.getAnimation('k', 6, 16, 16, 2, (32, 32))
        self.A_PORTAL_CLOSED = self.door.getAnimation('i', 6, 16, 16, 2, (32, 32))

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
        #wincon Amulet
        self.A_WINCON = self.amulet.getAnimation('a', 3, 16, 16, 2, (32, 32))
        # mana potion
        self.S_MANA_POTION = self.potion.getImage('g', 1, 16, 16, (32, 32))[0]
        # health potion
        self.S_HEALTH_POTION = self.potion.getImage('a', 1, 16, 16, (32, 32))[0]


        # SPECIAL
        self.S_STAIRS_DOWN = self.tile.getImage('h', 4, 16, 16, (32, 32))[0]
        self.S_STAIRS_UP = self.tile.getImage('e', 4, 16, 16, (32, 32))[0]

        # GUI
        self.S_UP_ARROW_LARGE = self.gui.getImage('c', 7, 16, 16, (32, 32))[0]
        self.S_UP_ARROW_SMALL = self.gui.getImage('d', 7, 16, 16, (32, 32))[0]
        self.BLACK_WINDOW_BOX_1_SINGLE = self.gui.getImage('q', 8, 16, 16, (48, 48))[0]
        self.BLACK_WINDOW_BOX_2_SINGLE = self.gui.getImage('q', 11, 16, 16, (48, 48))[0]
        self.BLACK_WINDOW_BOX_3_SINGLE = self.gui.getImage('q', 14, 16, 16, (48, 48))[0]
        self.BLACK_WINDOW_BOX_4_SINGLE = self.gui.getImage('q', 17, 16, 16, (48, 48))[0]
        self.ATTACK_ICON = self.mediumWep.getImage('a', 1, 16, 16, (16, 16))[0]
        self.DEFENSE_ICON = self.shield.getImage('a', 1, 16, 16, (16, 16))[0]

        self.animationDict = {

            "A_PLAYER" : self.A_PLAYER,
            "None" : "None",
            "A_SNAKE_GREEN_01" : self.A_SNAKE_GREEN_01,
            "A_SNAKE_GREEN_02" : self.A_SNAKE_GREEN_02,
            "A_SNAKE_ANACONDA_01" : self.A_SNAKE_ANACONDA_01,
            "A_SNAKE_ANACONDA_02" : self.A_SNAKE_ANACONDA_02,
            "A_SNAKE_ANACONDA_03" : self.A_SNAKE_ANACONDA_03,
            "A_SNAKE_COBRA_01" : self.A_SNAKE_COBRA_01,
            "A_SNAKE_COBRA_02" : self.A_SNAKE_COBRA_02,
            "A_SNAKE_COBRA_03" : self.A_SNAKE_COBRA_03,
            #humanoids
            "A_ALCHEMIST" : self.A_ALCHEMIST,
            # rodent
            "A_MOUSE" : self.A_MOUSE,
            "A_RAT" : self.A_RAT,
            "A_GIANT_RAT" : self.A_GIANT_RAT,
            "A_UNDEAD_RAT" : self.A_UNDEAD_RAT,
            "A_POISON_RAT" : self.A_POISON_RAT,
            "A_HUNTER_RAT" : self.A_HUNTER_RAT,
            # insect
            "A_SPIDER_TARANTULA" : self.A_SPIDER_TARANTULA,
            "A_SPIDER_TARANTULA_GIANT_ZOMBIE" : self.A_SPIDER_TARANTULA_GIANT_ZOMBIE,
            "A_SNAIL" : self.A_SNAIL,
            # plant
            "A_FERNOID" : self.A_FERNOID,
            # undead
            "A_DEATH_CRACK" : self.A_DEATH_CRACK,

            # corpse
            "S_FLESH_TAIL" : self.S_FLESH_TAIL,
            "S_FLESH_TAIL_SMALL" : self.S_FLESH_TAIL_SMALL,
            "S_FLESH_CORPSE_DEFAULT_01" : self.S_FLESH_CORPSE_DEFAULT_01,
            "S_FLESH_CORPSE_DEFAULT_02" : self.S_FLESH_CORPSE_DEFAULT_02,
            "S_FLESH_CORPSE_DEFAULT_03" : self.S_FLESH_CORPSE_DEFAULT_03,
            "S_FLESH_CORPSE_DEFAULT_04" : self.S_FLESH_CORPSE_DEFAULT_04,
            "S_FLESH_CORPSE_DEFAULT_05" : self.S_FLESH_CORPSE_DEFAULT_05,

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
            #wincon amulet
            "A_WINCON" : self.A_WINCON,
            "S_MANA_POTION" : self.S_MANA_POTION,
            "S_HEALTH_POTION" : self.S_HEALTH_POTION,

            # GUI
            "S_UP_ARROW_LARGE" : self.S_UP_ARROW_LARGE,
            "S_UP_ARROW_SMALL" : self.S_UP_ARROW_SMALL,
            "black window box 1 single" : self.BLACK_WINDOW_BOX_1_SINGLE,
            "black window box 2 single" : self.BLACK_WINDOW_BOX_2_SINGLE,
            "black window box 3 single" : self.BLACK_WINDOW_BOX_3_SINGLE,
            "black window box 4 single" : self.BLACK_WINDOW_BOX_4_SINGLE,
            "ATTACK_ICON" : self.ATTACK_ICON,
            "DEFENSE_ICON" : self.DEFENSE_ICON,

            # SPECIAL
            "S_STAIRS_DOWN" : self.S_STAIRS_DOWN,
            "S_STAIRS_UP" : self.S_STAIRS_UP,
            "A_PORTAL_OPEN" : self.A_PORTAL_OPEN,
            "A_PORTAL_CLOSED" : self.A_PORTAL_CLOSED
        }

        ##############
        ## BITMASKS ##
        ##############

        # blue brick wall
        self.S_WALL = self.wall.getImage('d', 10, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED = self.wall.getImage('d', 13, 16, 16, (32, 32))[0]

        # blue brick Wall bitmask
        self.S_WALL_00 = self.wall.getImage('b', 11, 16, 16, (32, 32))[0]
        self.S_WALL_01 = self.wall.getImage('b', 11, 16, 16, (32, 32))[0]
        self.S_WALL_02 = self.wall.getImage('b', 10, 16, 16, (32, 32))[0]
        self.S_WALL_03 = self.wall.getImage('a', 12, 16, 16, (32, 32))[0]
        self.S_WALL_04 = self.wall.getImage('a', 11, 16, 16, (32, 32))[0]
        self.S_WALL_05 = self.wall.getImage('a', 11, 16, 16, (32, 32))[0]
        self.S_WALL_06 = self.wall.getImage('a', 10, 16, 16, (32, 32))[0]
        self.S_WALL_07 = self.wall.getImage('d', 11, 16, 16, (32, 32))[0]
        self.S_WALL_08 = self.wall.getImage('b', 10, 16, 16, (32, 32))[0]
        self.S_WALL_09 = self.wall.getImage('c', 12, 16, 16, (32, 32))[0]
        self.S_WALL_10 = self.wall.getImage('b', 10, 16, 16, (32, 32))[0]
        self.S_WALL_11 = self.wall.getImage('e', 12, 16, 16, (32, 32))[0]
        self.S_WALL_12 = self.wall.getImage('c', 10, 16, 16, (32, 32))[0]
        self.S_WALL_13 = self.wall.getImage('f', 11, 16, 16, (32, 32))[0]
        self.S_WALL_14 = self.wall.getImage('e', 10, 16, 16, (32, 32))[0]
        self.S_WALL_15 = self.wall.getImage('e', 11, 16, 16, (32, 32))[0]

        # blue brick wall explored
        self.S_WALL_EXPLORED_00 = self.wall.getImage('b', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_01 = self.wall.getImage('b', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_02 = self.wall.getImage('b', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_03 = self.wall.getImage('a', 15, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_04 = self.wall.getImage('a', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_05 = self.wall.getImage('a', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_06 = self.wall.getImage('a', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_07 = self.wall.getImage('d', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_08 = self.wall.getImage('b', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_09 = self.wall.getImage('c', 15, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_10 = self.wall.getImage('b', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_11 = self.wall.getImage('e', 15, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_12 = self.wall.getImage('c', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_13 = self.wall.getImage('f', 14, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_14 = self.wall.getImage('e', 13, 16, 16, (32, 32))[0]
        self.S_WALL_EXPLORED_15 = self.wall.getImage('e', 14, 16, 16, (32, 32))[0]

        ########################
        ## BITMASK DICTIONARY ##
        ########################

        self.blueBrickDict = {
            0 : self.S_WALL_00,
            1 : self.S_WALL_01,
            2 : self.S_WALL_02,
            3 : self.S_WALL_03,
            4 : self.S_WALL_04,
            5 : self.S_WALL_05,
            5 : self.S_WALL_05,
            6 : self.S_WALL_06,
            7 : self.S_WALL_07,
            8 : self.S_WALL_08,
            9 : self.S_WALL_09,
            10 : self.S_WALL_10,
            11 : self.S_WALL_11,
            12 : self.S_WALL_12,
            13 : self.S_WALL_13,
            14 : self.S_WALL_14,
            15 : self.S_WALL_15
        }

        self.blueBrickExploredDict = {
            0 : self.S_WALL_EXPLORED_00,
            1 : self.S_WALL_EXPLORED_01,
            2 : self.S_WALL_EXPLORED_02,
            3 : self.S_WALL_EXPLORED_03,
            4 : self.S_WALL_EXPLORED_04,
            5 : self.S_WALL_EXPLORED_05,
            5 : self.S_WALL_EXPLORED_05,
            6 : self.S_WALL_EXPLORED_06,
            7 : self.S_WALL_EXPLORED_07,
            8 : self.S_WALL_EXPLORED_08,
            9 : self.S_WALL_EXPLORED_09,
            10 : self.S_WALL_EXPLORED_10,
            11 : self.S_WALL_EXPLORED_11,
            12 : self.S_WALL_EXPLORED_12,
            13 : self.S_WALL_EXPLORED_13,
            14 : self.S_WALL_EXPLORED_14,
            15 : self.S_WALL_EXPLORED_15
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
    def __init__(self,
                 nameInstance,
                 baseAtk=2,
                 baseDef=0,
                 faction='monster',
                 maxHP=10,
                 maxMP=1,
                 deathFunc=None,
                 dungeonLevel=1,
                 scent = None):
        self.nameInstance = nameInstance
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.faction = faction
        self.maxHP = maxHP
        self.currentHP = maxHP
        self.maxMP = maxMP
        self.currentMP = maxMP
        self.deathFunc = deathFunc
        self.dungeonLevel = dungeonLevel

        self.scent = scent
        if self.scent:
            self.scent.owner = self

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

        if damageDelt > 0:
            hitSound = RANDOM_ENGINE.choice(ASSETS.snd_hitList)
            length = ((hitSound.get_length()) * 1000) // 1
            pygame.mixer.Sound.play(hitSound)
            pygame.time.delay(int(length))


        target.creature.takeDamage(damageDelt)



    def takeDamage(self, damage):
        self.currentHP -= damage
        gameMessage(self.nameInstance + "'s health is " + str(self.currentHP) +
                    '/' + str(self.maxHP), constants.COLOR_RED)

        if self.currentHP <= 0:
            if self.deathFunc is not None:
                self.deathFunc(self.owner)

    def heal(self, value):

        self.currentHP += value

        if self.currentHP > self.maxHP:
            self.currentHP = self.maxHP

    def healMP(self, value):

        self.currentMP += value

        if self.currentMP > self.maxMP:
            self.currentMP = self.maxMP

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

class com_Scent:
    # scent is a sub-component for the creature component
    # PLAYER leaves a scent behind for monsters to hunt
    def __init__(self, strength):

        # how long the scent will last
        self.strength = strength

    def trail(self):

        scentName = 'scent: ' + self.owner.owner.nameObject
        trailExists = False
        # drops scent obj to create a trail
        for obj in GAME.currentObj:
            if obj.nameObject == scentName:
                if obj.x == self.owner.owner.x and obj.y == self.owner.owner.y:
                    obj.scentStrength = self.strength
                    trailExists = True

        if not trailExists:
            scentObj = obj_Actor(nameObject = scentName,
                                 animationKey = 'None',
                                 x = self.owner.owner.x,
                                 y = self.owner.owner.y,
                                 scentStrength = self.strength)
            GAME.currentObj.append(scentObj)

class com_Container:

    def __init__(self, volume=10, inventory=[]):
        self.inventory = inventory
        self.maxVol = volume

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
    def __init__(self,
                 weight = 0,
                 volume = 0,
                 useFunc = None,
                 value = None):

        self.weight = weight
        self.volume = volume
        self.useFunc = useFunc
        self.value = value

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
        if self.owner.equipment and self.owner.equipment.equipped:
            self.owner.equipment.toggleEquip()
        self.owner.x = newX
        self.owner.y = newY
        gameMessage(self.owner.displayName + ' dropped')

    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggleEquip()
            return

        if self.useFunc:
            result = self.useFunc(self.container.owner, self.value)
            gameMessage(str(result))
            if result != 'canceled':
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
                    item.equipment.equipped = False
                    gameMessage(item.displayName + " is unequipped")

        self.equipped = True
        PLAYER.container.inventory.remove(self.owner)
        PLAYER.container.inventory.insert(0, self.owner)


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

class com_Exitportal:
    def __init__(self):
        self.openAnimation = "A_PORTAL_OPEN"
        self.closedAnimation = "A_PORTAL_CLOSED"

    def update(self):


        # initialize
        foundWincon = False

        # check conditions
        portalOpen = (self.owner.state == "OPEN")

        foundWinconCheck = False
        for obj in PLAYER.container.inventory:
            if obj.nameObject == 'Amulet of Nocniw':
                foundWinconCheck = True


        foundWincon = foundWinconCheck

        if foundWincon and not portalOpen:
            self.owner.state = "OPEN"
            self.owner.animationKey = self.openAnimation
            self.owner.animationInit()

        if not foundWincon and portalOpen:
            self.owner.state = "CLOSED"
            self.owner.animationKey = self.closedAnimation
            self.owner.animationInit()

    def use(self):

        if self.owner.state == "OPEN":
            # remove any save file
            try:
                os.remove(constants.PATH + "data/savegame")
            except:
                pass
            # win screen loop
            wincon = True

            while wincon:

                # get player inputs
                eventsList = pygame.event.get()
                menuInput = (eventsList)

                for event in eventsList:
                    if event.type == pygame.QUIT:
                        gameExit(save = False)

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            wincon = False
                            PLAYER.state = "STATUS_VICTORY"

                #clear screen
                SURFACE_MAIN.fill(constants.COLOR_WHITE)

                # get window center
                screenCenter = (constants.WINDOW_WIDTH //2 , constants.WINDOW_HEIGHT // 2)
                belowCenter = (constants.WINDOW_WIDTH //2 , constants.WINDOW_HEIGHT // 1.5)

                # text
                drawText(SURFACE_MAIN,
                         'You Win!',
                         screenCenter,
                         constants.COLOR_BLACK,
                         constants.FONT_TITLE_TEXT,
                         backColor = constants.COLOR_WHITE,
                         centered = True)

                drawText(SURFACE_MAIN,
                         'press Enter',
                         belowCenter,
                         constants.COLOR_BLACK,
                         constants.FONT_MESSAGE_TEXT,
                         backColor = constants.COLOR_WHITE,
                         centered = True)

                #update display
                pygame.display.update()
        else:
            gameMessage("A sense of home eminates from the gate.", constants.COLOR_WHITE)
            gameMessage("You pass through but are still in the dungeon.", constants.COLOR_WHITE)


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
    def __init__(self):
        self.alert = 0

    ''' A simple AI that just runs down the enemy and tries to attack'''

    def takeTurn(self):

        monster = self.owner
        faction = self.owner.creature.faction
        if libtcod.map_is_in_fov(FOV_MAP, monster.x, monster.y):
            # set alert staus
            self.alert = 5

            # move towards enemy if too far away
            if monster.distanceTo(PLAYER) >= 2:
                if PLAYER.creature.currentHP > 0:
                    self.owner.moveTowards(PLAYER)
                else:
                    self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                             libtcod.random_get_int(0, -1, 1))
            elif PLAYER.creature.currentHP > 0:
                monster.creature.attack(PLAYER)
        else:
            leadScent = False
            if self.alert > 0:

                # magic number for senseOf Smell
                senseOfSmell = 3

                ## get a list of tiles in a square around the creature
                # initialize out smellRadius Array
                smellRadius = []

                # fill the array with tiles around the actor
                for x in range(0, (senseOfSmell * 2) + 1):
                    tile = ((monster.x - senseOfSmell) + x, monster.y - senseOfSmell)
                    smellRadius.append(tile)
                    tile = ((monster.x - senseOfSmell) + x, monster.y + senseOfSmell)
                    smellRadius.append(tile)
                for y in range(0, (senseOfSmell * 2) - 1):
                    tile = ((monster.x - senseOfSmell), monster.y - (senseOfSmell + 1) + y)
                    smellRadius.append(tile)
                    tile = ((monster.x + senseOfSmell), monster.y - (senseOfSmell + 1) + y)
                    smellRadius.append(tile)

                # raycast through set of tiles
                for ray in smellRadius:

                    # list of tiles in range
                    smellLine = mapFindLine((monster.x, monster.y),(ray))

                    # go check all the tiles in the ray
                    for tile in smellLine:

                        #seperate out the tuple values
                        tileX, tileY = tile

                        #if you hit a wall, stop
                        if GAME.currentMap[tileX][tileY].blockPath == True:
                            break

                        # check game objects for smell objects
                        for obj in GAME.currentObj:
                            # if you find a smell object...
                            if obj.nameObject == 'scent: ' + PLAYER.nameObject:
                                # and it has the same address as out tile...
                                if (obj.x, obj.y) == tile:
                                    # and we haven't designated a leadScent...
                                    if not leadScent:
                                        #then this obj is our leadScent
                                        leadScent = obj

                                    # unless there is a stronger scent...
                                    elif obj.scentStrength > leadScent.scentStrength:
                                        # then this obj is our leadScent
                                        leadScent = obj


            # if there is no leadScent, lower alert status
            if not leadScent:
                if self.alert > 0:
                    self.alert -= 1
            # if there is a leadScent, track it (move towards it)
            else:
                self.owner.moveTowards(leadScent)


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
    mob.depth = constants.DEPTH_CORPSE
    mob.creature = None
    mob.ai = None

    rand = libtcod.random_get_int(0, 1,5)

    if rand == 1:
        mob.animationKey = "S_FLESH_CORPSE_DEFAULT_01"
        mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT_01
    elif rand == 2:
        mob.animationKey = "S_FLESH_CORPSE_DEFAULT_02"
        mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT_02
    elif rand == 3:
        mob.animationKey = "S_FLESH_CORPSE_DEFAULT_03"
        mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT_03
    elif rand == 4:
        mob.animationKey = "S_FLESH_CORPSE_DEFAULT_04"
        mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT_04
    else:
        mob.animationKey = "S_FLESH_CORPSE_DEFAULT_05"
        mob.animation = ASSETS.S_FLESH_CORPSE_DEFAULT_05

    if mob.container:
        for item in mob.container.inventory:
            GAME.currentObj.append(item)
            item.animationInit()
            mob.container.inventory.remove(item)
            item.x = mob.x
            item.y = mob.y



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

def death_Player(player):

    # remove any save file
    try:
        os.remove(constants.PATH + "data/savegame")
    except:
        pass

    # initialize dead
    dead = True
    player.state = "STATUS_DEAD"

    #get timestamp
    d = datetime.datetime.now()

    #create file name for legacy records (player name month, day year time)
    filename = ('repos/roguelike/first/data/legacy/legacy_' + PLAYER.creature.nameInstance + '.' +
                datetime.date.today().strftime('%B, %d %Y ') + str(d.hour) + ':' + str(d.minute) + '.txt')

    # create a legacy file
    legacyFile = open(filename, 'a+')

    # write to file (color is dumped, we dont use it)
    for message, color in GAME.msgHistory:
        legacyFile.write(message + '\n')

    # death screen loop
    while dead:

        # get player inputs
        eventsList = pygame.event.get()
        menuInput = (eventsList)

        for event in eventsList:
            if event.type == pygame.QUIT:
                gameExit(save = False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dead = False

        #clear screen
        SURFACE_MAIN.fill(constants.COLOR_BLACK)

        # get window center
        screenCenter = (constants.WINDOW_WIDTH //2 , constants.WINDOW_HEIGHT // 2)
        belowCenter = (constants.WINDOW_WIDTH //2 , constants.WINDOW_HEIGHT // 1.5)

        # text
        drawText(SURFACE_MAIN,
                 'You died!',
                 screenCenter,
                 constants.COLOR_WHITE,
                 constants.FONT_TITLE_TEXT,
                 backColor = constants.COLOR_BLACK,
                 centered = True)

        drawText(SURFACE_MAIN,
                 'press Enter',
                 belowCenter,
                 constants.COLOR_WHITE,
                 constants.FONT_MESSAGE_TEXT,
                 backColor = constants.COLOR_BLACK,
                 centered = True)

        #update display
        pygame.display.update()







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

            # if this the first room of the first level:
            if CURRENT_DUNGEON_LEVEL == 1 and len(roomList) == 0:

                # give it a standardized dimension
                firstX = constants.MAP_WIDTH // 2
                firstY = constants.MAP_HEIGHT // 2
                newRoom = obj_Room((firstX, firstY), (5, 5))

                # place the room
                mapCreateRoom(newMap, newRoom)
                currentCenter = newRoom.center

            else:
                mapCreateRoom(newMap, newRoom)
                currentCenter = newRoom.center

                # if this isn't the first room, tunnle from our previous room, to the new one
                if len(roomList) != 0:
                    previousCenter = roomList[-1].center
                    mapCreateTunnels(previousCenter, currentCenter, newMap)

            # add room to roomlist
            roomList.append(newRoom)



    GAME.currentMap = newMap

    # create a roomlist
    GAME.roomList = roomList

    # mark explorable tiles
    mapExplorable(newMap)

    # update the FOV map
    mapMakeFOV(newMap)

    # bitmask all the tiles
    mapAssignTiles(newMap)

    return (newMap, roomList)

def mapAssignTiles(map):

    for x in range(constants.MAP_WIDTH):
        for y in range(constants.MAP_HEIGHT):
            #see if (x, y) is a wall
            tileIsWall = mapCheckForWall(x, y)
            tileIsExplorable = mapIsExplorable(x, y)

            if tileIsWall and tileIsExplorable:

                # initialize assign
                bitmask = 0

                # add bitmask value

                #tile above
                if mapCheckForWall(x, y-1) and mapIsExplorable(x, y-1): bitmask += 1
                #tile to the right
                if mapCheckForWall(x+1, y) and mapIsExplorable(x+1, y): bitmask += 2
                #tile below
                if mapCheckForWall(x, y+1) and mapIsExplorable(x, y+1): bitmask += 4
                #tile to the left
                if mapCheckForWall(x-1, y) and mapIsExplorable(x-1, y): bitmask += 8

                # if bitmask == 15: bitmask = 0
                map[x][y].assignment = bitmask

def mapPlaceObjects(roomList):
    currentLevel = len(GAME.previousMaps) + 1
    topLevel = (len(GAME.previousMaps) == 0)
    bottomLevel = (currentLevel == constants.MAP_NUM_LEVELS)

    # list of mobs generated this floor
    mobList = []

    # iterator for what floor we are on
    i = 0

    for room in roomList:

        # our first and last room
        firstRoom = (room == roomList[0])
        lastRoom = (room == roomList[-1])

        if firstRoom and topLevel and not bottomLevel:
            gen_exitPortal(room.center)

        if firstRoom: PLAYER.x, PLAYER.y = room.center

        if firstRoom and not topLevel: gen_stairs((PLAYER.x, PLAYER.y),
                                                  downwards = False)
        if lastRoom:
            if bottomLevel:
                gen_wincon(room.center)

            else:
                gen_stairs(room.center)

        if i == 0:
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)
            gen_item((x, y), True)
        else:
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)

            # get the mob
            mob = gen_enemy((x, y))


            # populate the map with the mob if it gen'd
            if mob != 'gen fail':
                GAME.currentObj.append(mob)

            # add the mobs name to the mob list
            if mob != 'gen fail': mobList.append(mob.nameObject)

            # if this is the last room, print the list (for testing)
            if lastRoom:
                print(str(len(mobList)) + " mobs gen'd in " + str(len(roomList)) + " rooms for dungeon level: " + str(CURRENT_DUNGEON_LEVEL))
                print("-------------------------------------")
                print()
                for monster in mobList:
                    print(monster)

            # generate (x, y) for new item
            x = libtcod.random_get_int(0, room.ULx + 1, room.LRx - 1)
            y = libtcod.random_get_int(0, room.ULy + 1, room.LRy - 1)

            # gen an new item
            gen_item((x, y))

        # increment what room we are on
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

def mapExplorable(map):
    for x in range(constants.MAP_WIDTH):
        for y in range(constants.MAP_WIDTH):
            # if there is a floor, all its surronding tiles are explorable
            if map[x][y].blockPath == False:


                map[x - 1][y - 1].explorable = True
                map[x - 1][y].explorable = True
                map[x - 1][y + 1].explorable = True

                map[x][y - 1].explorable = True
                map[x][y].explorable = True
                map[x][y + 1].explorable = True

                map[x + 1][y - 1].explorable = True
                map[x + 1][y].explorable = True
                map[x + 1][y + 1].explorable = True

def mapIsExplorable(x, y):
    if GAME.currentMap[x][y].explorable:
        return True
    else:
        return False

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

def mapIsExplored(x, y):
    global GAME

    try:
        isExplored = GAME.currentMap[x][y].explored
    except:
        isExplored = False

    return isExplored

def mapCheckForWall(x, y):
    '''This function checks to see if [x][y] is a wall or not

    ARGS:
    x = x you want to check
    y = y you want to check

    returns True if wall, False if not a wall
    '''

    global GAME

    try:
        isWall = GAME.currentMap[x][y].blockPath
    except:
        isWall = True

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
def drawGUI():

    # blit BOX_MAP
    SURFACE_MAIN.blit(FRAME_MAP.surface, (0,0))
    FRAME_MAP.surface.blit(BOX_MAP, (FRAME_MAP.border, FRAME_MAP.border))
    BOX_MAP.blit(SURFACE_MAP, (0, 0), CAMERA.rectangle)


    # blit PLAYER stats
    SURFACE_MAIN.blit(FRAME_CONSOLE.surface, (0,FRAME_MAP.height))

    # blit PLAYER inventory
    SURFACE_MAIN.blit(FRAME_INV.surface, (FRAME_MAP.width, 0))

    # blit FRAME_STATUS
    SURFACE_MAIN.blit(FRAME_STATUS.surface, (FRAME_MAP.width, FRAME_MAP.height))

def drawCharGUI():
    # FRAME_INV is the GUI object that holds everything on the right part of the screen
    # box refers to the surface that contains all the character info

    # dimensions of inventory frame
    frameWidth = FRAME_INV.width
    frameHeight = FRAME_INV.height
    frameBorder = FRAME_INV.border

    # dimensions of our box surface
    boxWidth = int(frameWidth - (frameBorder * 2))
    boxHeight = int(frameHeight // 2 - (frameBorder * 2) )
    boxCenterX = boxWidth // 2
    boxCenterY = boxHeight // 2

    # margins
    boxHeaderMargin = 32
    boxFooterMargin = 16
    boxBody = boxHeight - boxHeaderMargin
    boxLeftMargin = 0
    boxRightMargin = 0

    # box X, Y
    boxX = frameBorder
    boxY = frameBorder

    # boxSurf hold all the character GUI
    boxSurf = pygame.Surface((boxWidth, boxHeight))

    ##TESTING##
    # boxSurf.fill(constants.COLOR_LIGHT_BLUE)


    ############
    ## HEADER ## the title of the box will be the characters name and race
    ############

    # get height and font of character text so we can center it
    nameFont = constants.FONT_TITLE_NAME_TEXT
    nameHeight = helperTextHeight(nameFont)
    nameX = (boxWidth // 2)
    nameY = (nameHeight // 2) + 10

    # get height and font of race text so we can center it
    raceFont = constants.FONT_TITLE_RACE_TEXT
    raceHeight = helperTextHeight(nameFont)
    raceY = (nameY + nameHeight)

    # get the total height of these texts for further drawing
    headerHeight = raceY + raceHeight

    # write the char's name as the header
    drawText(boxSurf,
             PLAYER.creature.nameInstance,
             ( nameX, nameY),
             constants.COLOR_WHITE,
             nameFont, centered = True)

    # write the char's race as the sub-header
    drawText(boxSurf,
             'the ' + PLAYER.nameObject,
             ( nameX, raceY),
             constants.COLOR_WHITE,
             raceFont, centered = True)



    ##############
    ## EQUIPPED ##  two boxes show what weapon and sheild are equipped
    ##############  along with the character's sprite

    # equipment box sprite
    equipmentBoxSprite = ASSETS.animationDict['black window box 2 single']

    # char box sprite
    charBoxSprite = ASSETS.animationDict['black window box 1 single']

    # dimensions of the equipment boxes
    equipmentBoxDim = 48
    # x and y of the sprite within the equipment box
    spriteX = 8
    spriteY = 8

    # get our equipment list
    equippedItems = PLAYER.container.equippedItems

    # what are our weapons
    weapon = None
    shield = None
    for item in equippedItems:
        if item.equipment.slot == 'right_hand':
            weapon = item
        if item.equipment.slot == 'left_hand':
            shield = item

    # get our weapon and shield sprite
    weaponSprite = ASSETS.animationDict['None']
    shieldSprite = ASSETS.animationDict['None']

    # be sure we have something equipped
    if weapon:
        weaponSprite = ASSETS.animationDict[weapon.animationKey]

    if shield:
        shieldSprite = ASSETS.animationDict[shield.animationKey]

    # get our char sprite
    charSprite = ASSETS.animationDict[PLAYER.animationKey]



    # x and y of our equiment and char boxes
    shieldBoxX = (boxCenterX // 2) -  (equipmentBoxDim // 2)
    weaponBoxX = (boxCenterX + (boxCenterX // 2)) - (equipmentBoxDim // 2)
    charBoxX = boxCenterX - (equipmentBoxDim // 2)
    equipmentBoxY = headerHeight

    # equipment boxes surfaces
    weaponBoxSurf = pygame.Surface((equipmentBoxDim, equipmentBoxDim))
    shieldBoxSurf = pygame.Surface((equipmentBoxDim, equipmentBoxDim))
    # char sprite surface
    charBoxSurf = pygame.Surface((equipmentBoxDim, equipmentBoxDim))


    #################
    ## STATUS BARS ##   show the HP and MP bars for the character
    #################

    # dimensions of the surface we will put all these status bars on
    statusSurfWidth     = int(boxWidth * .9)
    statusSurfHeight    = int(boxHeight * .3)

    # statusSurf is the surface that holds all these GUI elements
    statusSurf = pygame.Surface((statusSurfWidth, statusSurfHeight))

    # the x and y for our statusSurf
    statusSurfX = (boxWidth - statusSurfWidth) // 2
    statusSurfY = headerHeight + equipmentBoxDim + 10

    # bar surface dimensions
    barSurfWidth = statusSurfWidth
    barSurfHeight = statusSurfHeight * .4


    # surfaces for our HP and MP bars
    HPsurf = pygame.Surface(( barSurfWidth, barSurfHeight))
    MPsurf = pygame.Surface(( barSurfWidth, barSurfHeight))
    HPsurfY = 5

    ###TEST###
    # statusSurf.fill(constants.COLOR_GREEN)
    # HPsurf.fill(constants.COLOR_PINK)
    # MPsurf.fill(constants.COLOR_PURPLE)

    # font for HP/ MP
    HPMPfont = constants.FONT_DEBUG_MESSAGE
    HPMPcurrentFont = constants.FONT_HPMP_TEXT

    # width of 'HP:' ('MP:' is the same)
    HPMPwidth = helperTextWidth(HPMPfont, 'HP: ')
    HPMPheight = helperTextWidth(HPMPfont)

    # current/ max HP height
    HPMPcurrentHeight = helperTextWidth(HPMPcurrentFont)

    # status bar dimensions
    statusBarWidth = barSurfWidth - (HPMPwidth * 2)
    statusBarHeight = 8

    # where in the box the status bars starts
    textX = 2
    textY = 2
    statusBarX = HPMPwidth + 4
    statusBarY = 4

    # current/ max HP read out
    currentMaxX = statusBarX
    currentMaxY = (statusBarY + statusBarHeight) + 2


    # HP BOX #

    # draw 'HP:'
    drawText(HPsurf,
             'HP:',
             (textX, textY),
             constants.COLOR_STATS, HPMPfont)

    # draw 'MP:'
    drawText(MPsurf,
             'MP:',
             (textX, textY),
             constants.COLOR_STATS, HPMPfont)



    # HP bar
    healthBar = ui_FillBar(HPsurf,
                           (statusBarX, statusBarY),
                           PLAYER.creature.currentHP,
                           PLAYER.creature.maxHP,
                           statusBarWidth,
                           statusBarHeight)

    # draw the current/ max HP under the bar
    drawText(HPsurf,
             str(PLAYER.creature.currentHP) + ' / ' + str(PLAYER.creature.maxHP),
             (currentMaxX, currentMaxY),
             constants.COLOR_STATS,
             HPMPcurrentFont)

    # MP bar
    magicBar = ui_FillBar(MPsurf,
                         (statusBarX, statusBarY),
                         PLAYER.creature.currentMP,
                         PLAYER.creature.maxMP,
                         statusBarWidth,
                         statusBarHeight,
                         fillColor = constants.COLOR_HEAL_MP,
                         emptyColor = constants.COLOR_DAMAGE_MP)

    # draw the current/ max HP under the bar
    drawText(MPsurf,
             str(PLAYER.creature.currentMP) + ' / ' + str(PLAYER.creature.maxMP),
             (currentMaxX, currentMaxY),
             constants.COLOR_STATS,
             HPMPcurrentFont)

    ###########
    ## STATS ##  this is where the attack and def stats are drawn
    ###########

    # margin above statsSurf
    topMargin = 8

    # dimensions for our statsSurf
    statsSurfWidth = int(boxWidth * .9)
    statsSurfHeight = (boxHeight - (statusSurfY + statusSurfHeight)) - (topMargin * 2)

    # surface that holds all the stats
    statsSurf = pygame.Surface((statsSurfWidth, statsSurfHeight))

    # X and Y of our statsSurf
    statsSurfX = (boxWidth - statusSurfWidth) // 2
    statsSurfY = (statusSurfY + statusSurfHeight) + topMargin

    # dimensions for our attack and defense surfs
    attributeSurfWidth = int(statsSurfWidth // 2) - 2
    attributeSurfHeight = statsSurfHeight - 2

    # surfaces that hold out attack and defense stats and status effects
    ATKDEFSurf = pygame.Surface((attributeSurfWidth, attributeSurfHeight))
    effectSurf = pygame.Surface((attributeSurfWidth, attributeSurfHeight))

    ###TESTING###
    # ATKDEFSurf.fill(constants.COLOR_CYAN)
    # effectSurf.fill(constants.COLOR_ORANGE)

    # X and Y for our attack and defense surfs
    ATKDEFSurfX = 1
    ATKDEFSurfY = 1
    # all the ones represent 1 pixel margins
    effectSurfX = 1 + attributeSurfWidth + 1 + 1
    effectSurfY = 1

    # sprites for our stats icons
    attackIcon = ASSETS.animationDict["ATTACK_ICON"]
    defenseIcon = ASSETS.animationDict["DEFENSE_ICON"]

    # text for stats
    attackText = ':' + str(PLAYER.creature.power)
    defenseText = ':' + str(PLAYER.creature.defense)

    # blit out attack and def icons onto the surf
    ATKDEFSurf.blit(attackIcon, (0, 0))
    ATKDEFSurf.blit(defenseIcon, (0, 16))

    # draw the text for our stats
    drawText(ATKDEFSurf,
             attackText,
             ( 16, 4),
             constants.COLOR_ATTRIBUTE,
             constants.FONT_ATTRIBUTE_TEXT)

    # draw the text for our stats
    drawText(ATKDEFSurf,
             defenseText,
             ( 16, 20),
             constants.COLOR_ATTRIBUTE,
             constants.FONT_ATTRIBUTE_TEXT)

    ###TESTING###
    # statsSurf.fill(constants.COLOR_YELLOW)


    #############
    ## DRAWING ##  get it all on the screen
    #############



    # blit the GUI sprite onto the equipment boxes
    weaponBoxSurf.blit(equipmentBoxSprite, (0, 0))
    shieldBoxSurf.blit(equipmentBoxSprite, (0, 0))

    # draw the equipment sprites onto the equipmentBoxSurfs
    if weapon:
        weaponBoxSurf.blit(weaponSprite, (spriteX, spriteY))
    if shield:
        shieldBoxSurf.blit(shieldSprite, (spriteX, spriteY))

    # dram the charBox sprite onthe the charBoxSurf
    charBoxSurf.blit(charBoxSprite, (0, 0))

    # draw the char sprite onto the charBoxSurf
    charBoxSurf.blit(charSprite[0], (spriteX, spriteY))

    # draw the equipment boxes onto the boxSurf
    boxSurf.blit(weaponBoxSurf, (weaponBoxX, equipmentBoxY))
    boxSurf.blit(shieldBoxSurf, (shieldBoxX, equipmentBoxY))

    # draw the charBoxSurf onto the boxSurf
    boxSurf.blit(charBoxSurf, (charBoxX, equipmentBoxY))

    # draw the HP and MP bars onto the boxSurf
    healthBar.draw(healthBar.T_coords)
    magicBar.draw(magicBar.T_coords)

    # blit the HP and MP surfaces onto the status surface
    statusSurf.blit(HPsurf, ( 0, HPsurfY))
    statusSurf.blit(MPsurf, ( 0, HPsurfY + barSurfHeight + 5))

    # blit the statusSurf onto the boxSurf
    boxSurf.blit(statusSurf, (statusSurfX, statusSurfY))

    # blit the attribute surfs onto the statsSurf
    statsSurf.blit(ATKDEFSurf, (ATKDEFSurfX, ATKDEFSurfY))
    statsSurf.blit(effectSurf, (effectSurfX, effectSurfY))

    # blit the stats surface onto the boxSurf
    boxSurf.blit(statsSurf, ( statsSurfX, statsSurfY))



    #draw the boxSurf onto the FRAME_INV
    FRAME_INV.surface.blit(boxSurf, ( boxX, boxY))

def drawInventory():

    # FRAME_INV is the GUI object that holds everything on the right part of the screen
    # box refers to the surface that contains all the inventory stuff
    # inventoryWindow is the inventory list

    # INV_SCROLL_INDEX represents how many items we are scrolled down in the inventory
    # IS_DROPPING is a boolean representing whether the drop button is switched on
    global INV_SCROLL_INDEX, IS_DROPPING

    # generate a list of whats in the players inventory
    printList = [obj.displayName for obj in PLAYER.container.inventory]
    # length of that list
    invNum = len(printList)

    # font...
    inventoryFont = constants.FONT_DEBUG_MESSAGE
    inventoryTextHeight = helperTextHeight(inventoryFont) # 13 if font size is 10
    titleFont = constants.FONT_INV_TITLE
    titleHeight = helperTextHeight(titleFont)
    inventoryTextColor = constants.COLOR_WHITE
    infoFont = constants.FONT_INV_INFO
    infoTextHeight = helperTextHeight(infoFont)

    # dimensions of inventory frame
    frameWidth = FRAME_INV.width
    frameHeight = FRAME_INV.height
    frameBorder = FRAME_INV.border

    # dimensions of box surface
    boxWidth = frameWidth - (frameBorder * 2)
    boxHeight = FRAME_INV.height // 2
    boxX = frameBorder
    boxY = FRAME_INV.height // 2 - (frameBorder)

    # margins
    boxHeaderMargin = 32
    boxFooterMargin = 16
    boxBody = boxHeight - boxHeaderMargin
    boxLeftMargin = 0
    boxRightMargin = 0

    # dimensions of the infoWindow
    infoWindowMargin = 1
    infoWindowWidth = frameWidth - (frameBorder * 2) - (infoWindowMargin * 4)
    infoWindowHeight = infoTextHeight * 6
    infoWindowHeight -= (infoWindowHeight % ((infoWindowHeight // infoTextHeight) * infoTextHeight))

    # dimensions of inventory window surface
    inventoryWindowWidth = boxWidth - boxRightMargin - boxLeftMargin
    inventoryWindowHeight = inventoryTextHeight * 10

    # placement of inventory surface in box surface
    inventoryWindowX = 0 + boxLeftMargin
    inventoryWindowY = 0 + boxHeaderMargin

    # Surface to draw onto
    boxSurf = pygame.Surface((boxWidth, boxHeight))
    inventoryWindow = pygame.Surface((inventoryWindowWidth, inventoryWindowHeight))
    localInventorySurf = pygame.Surface((inventoryWindowWidth, (invNum * inventoryTextHeight)))
    infoWindowSurf = pygame.Surface((infoWindowWidth, infoWindowHeight))

    pygame.draw.rect(infoWindowSurf, constants.COLOR_BORDER2, (0, 0, infoWindowWidth, infoWindowHeight), 1)

    # inventory title placement
    titleX = 0
    titleY = ((boxHeaderMargin - titleHeight) // 2)
    drawText(boxSurf, "Inventory:", (titleX, titleY), constants.COLOR_TITLE, font = titleFont)

    #############
    ## buttons ##
    #############
    # size of the scroll buttons
    scrollDim = 10
    dropDimX = 36
    dropDimY = 11

    dropButton = ui_Button(destSurface = boxSurf,
                           buttonText = 'Drop',
                           size = (dropDimX, dropDimY),
                           T_coordsCenter = ( dropDimX // 2,
                                            ( boxHeaderMargin + inventoryWindowHeight) + dropDimY - 5),
                           Xoffset = (FRAME_INV.x + boxX),
                           Yoffset = (FRAME_INV.y + boxY),
                           box_colorDefault = constants.COLOR_BUTTON,
                           text_mouseOverColor = constants.COLOR_BUTTON_TEXT_MOUSEOVER,
                           text_colorDefault = constants.COLOR_BUTTON_TEXT,
                           disabled = False,
                           visibleWhenDisabled = False)

    scrollUp = ui_Button(destSurface = boxSurf,
                         buttonText = '',
                         size = (scrollDim, scrollDim),
                         T_coordsCenter = (boxWidth - (scrollDim),
                                          boxHeaderMargin  - (scrollDim)),
                         Xoffset = (FRAME_INV.x + boxX),
                         Yoffset = (FRAME_INV.y + boxY + 4),
                         box_mouseOverColor = constants.COLOR_FRAME,
                         box_colorDefault = constants.COLOR_FRAME,
                         text_mouseOverColor = constants.COLOR_FRAME,
                         text_colorDefault = constants.COLOR_FRAME,
                         disabled = False,
                         visibleWhenDisabled = False,
                         polyWidth = 1)

    scrollDown = ui_Button(destSurface = boxSurf,
                           buttonText = '',
                           size = (scrollDim,scrollDim),
                           T_coordsCenter = (boxWidth - (scrollDim),
                                            (boxHeaderMargin + inventoryWindowHeight) + (scrollDim) - 4),
                           Xoffset = (FRAME_INV.x + boxX),
                           Yoffset = (FRAME_INV.y + boxY),
                           box_mouseOverColor = constants.COLOR_FRAME,
                           box_colorDefault = constants.COLOR_FRAME,
                           text_mouseOverColor = constants.COLOR_FRAME,
                           text_colorDefault = constants.COLOR_FRAME,
                           disabled = False,
                           visibleWhenDisabled = False,
                           pointlist = [],
                           polyWidth = 1)

    # placement of infoWindow in the box surface
    infoWindowX = inventoryWindowX + (infoWindowMargin * 2)
    infoWindowY = (boxHeaderMargin + inventoryWindowHeight) + dropDimY + (infoWindowMargin * 2)

    ###################################
    ## pointlist for polygon drawing ##
    ###################################

    # scrollUp's x and y offset
    Xoff = (boxWidth - scrollDim - 4)
    Yoff = (boxHeaderMargin - scrollDim - 1)

    # scrollUp's pointlist makes its triangle shape
    scrollUpArrowPointlist = [ (Xoff + scrollDim // 2     , 0         + Yoff),
                               (Xoff + scrollDim          , scrollDim + Yoff),
                               (Xoff + 0                  , scrollDim + Yoff)]
    # scroll down's Y offset
    Yoff = (boxHeaderMargin + inventoryWindowHeight)

    # scrollDown's pointlist makes its triangle shape
    scrollDownArrowPointlist = [ (Xoff + 0              , 0         + Yoff),
                                 (Xoff + scrollDim      , 0         + Yoff),
                                 (Xoff + scrollDim // 2 , scrollDim + Yoff)]

    scrollUp.pointlist = scrollUpArrowPointlist
    scrollDown.pointlist = scrollDownArrowPointlist

    ####################
    ## button pushing ##
    ####################

    # return true when pressed
    scrollUpPressed = scrollUp.update(MASTER_EVENTS)
    scrollDownPressed = scrollDown.update(MASTER_EVENTS)

    dropButtonPressed = dropButton.update(MASTER_EVENTS)

    # drop button toggles IS_DROPPING
    if dropButtonPressed:
        if IS_DROPPING == False: IS_DROPPING = True
        else: IS_DROPPING = False

    # change color of drop button to indicate switch
    if IS_DROPPING == True:
        dropButton.box_currentColor = constants.COLOR_SWITCH
        dropButton.box_colorDefault = constants.COLOR_SWITCH
    else:
        dropButton.box_currentColor = constants.COLOR_BUTTON

    # Clear the inventoryWindow
    localInventorySurf.fill(constants.COLOR_MENU)

    #########################
    ## inventory selection ##
    #########################

    # get mouse x, y
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseX_rel = (mouseX - FRAME_INV.x) - boxX - inventoryWindowX
    mouseY_rel = (mouseY - FRAME_INV.y) - boxY - inventoryWindowY

    mouseInventory = (mouseX_rel >= 0 and
                   mouseY_rel >= 0 and
                   mouseX_rel <= inventoryWindowWidth and
                   mouseY_rel <= inventoryWindowHeight)

    mouseLineSelect = int((mouseY_rel // inventoryTextHeight) + INV_SCROLL_INDEX)

    # iterate over the events list
    for event in MASTER_EVENTS:
        result = 'menu open'
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                if (mouseInventory and
                    mouseLineSelect <= len(printList) - 1):
                    if IS_DROPPING:
                        result = PLAYER.container.inventory[mouseLineSelect].item.drop(PLAYER.x, PLAYER.y)
                    else:
                        result = PLAYER.container.inventory[mouseLineSelect].item.use()

        if result == 'canceled' or not result:
            return 'no action'
        elif result == 'menu open':
            pass
        else:
            return 'result'

    # iterate and draw the inventory list
    line = 0
    for obj in PLAYER.container.inventory:
        if line == mouseLineSelect and mouseInventory:
            if IS_DROPPING:
                if obj.equipment:
                    if obj.equipment.equipped:
                        drawText(localInventorySurf,
                                 obj.displayName,
                                 font=constants.FONT_MESSAGE_TEXT,
                                 T_coords=(0, (0 + (line * inventoryTextHeight))),
                                 textColor=constants.COLOR_EQUIPPED,
                                 backColor=constants.COLOR_DROPPING_HIGHLIGHT)
                    else:
                        drawText(localInventorySurf,
                                 obj.displayName,
                                 font=constants.FONT_MESSAGE_TEXT,
                                 T_coords=(0, (0 + (line * inventoryTextHeight))),
                                 textColor=inventoryTextColor,
                                 backColor=constants.COLOR_DROPPING_HIGHLIGHT)
                else:
                    drawText(localInventorySurf,
                             obj.displayName,
                             font=constants.FONT_MESSAGE_TEXT,
                             T_coords=(0, (0 + (line * inventoryTextHeight))),
                             textColor=constants.COLOR_DROPPING_TEXT,
                             backColor=constants.COLOR_DROPPING_HIGHLIGHT)
            else:
                if obj.equipment:
                    if obj.equipment.equipped:
                        drawText(localInventorySurf,
                                 obj.displayName,
                                 font=constants.FONT_MESSAGE_TEXT,
                                 T_coords=(0, (0 + (line * inventoryTextHeight))),
                                 textColor=constants.COLOR_EQUIPPED,
                                 backColor=constants.COLOR_GREY)
                    else:
                        drawText(localInventorySurf,
                                 obj.displayName,
                                 font=constants.FONT_MESSAGE_TEXT,
                                 T_coords=(0, (0 + (line * inventoryTextHeight))),
                                 textColor=inventoryTextColor,
                                 backColor=constants.COLOR_GREY)
                else:
                    drawText(localInventorySurf,
                             obj.displayName,
                             font=constants.FONT_MESSAGE_TEXT,
                             T_coords=(0, (0 + (line * inventoryTextHeight))),
                             textColor=inventoryTextColor,
                             backColor=constants.COLOR_GREY)
        else:
            if obj.equipment:
                if obj.equipment.equipped:
                    drawText(localInventorySurf,
                             obj.displayName,
                             font=constants.FONT_MESSAGE_TEXT,
                             T_coords=(0, (0 + (line * inventoryTextHeight))),
                             textColor=constants.COLOR_EQUIPPED)
                else:
                    drawText(localInventorySurf,
                             obj.displayName,
                             font=constants.FONT_MESSAGE_TEXT,
                             T_coords=(0, (0 + (line * inventoryTextHeight))),
                             textColor=inventoryTextColor)
            else:
                drawText(localInventorySurf,
                         obj.displayName,
                         font=constants.FONT_MESSAGE_TEXT,
                         T_coords=(0, (0 + (line * inventoryTextHeight))),
                         textColor=inventoryTextColor)
        line += 1

    ###############################
    ## inventoryWindow scrolling ##
    ###############################

    #Current Y coord of localInventorySurf
    currentInvY = (INV_SCROLL_INDEX * (-1)) * inventoryTextHeight

    # how many items in the player's inventory
    invNum = len(printList)


    # if the scroll buttons are pressed, INV_SCROLL_INDEX is incremented
    if scrollUpPressed and INV_SCROLL_INDEX != 0:
        INV_SCROLL_INDEX -= 1
    if scrollDownPressed and INV_SCROLL_INDEX != ((inventoryWindowHeight // inventoryTextHeight) - invNum) * (-1):
        INV_SCROLL_INDEX += 1


    # scroll buttons only visible when inventory exceeds localInventorySurf's height
    #  if there are more items in the inventory then we can see

    if invNum > inventoryWindowHeight // inventoryTextHeight:
        scrollUp.visibleWhenDisabled = True
        scrollDown.visibleWhenDisabled = True
        # if we are at the top of the list
        if INV_SCROLL_INDEX == 0:
            # grey-out the scroll up button
            scrollUp.disabled = True
            # enable the scroll down button
            scrollDown.disabled = False
            scrollDown.box_colorDefault = constants.COLOR_BUTTON
            scrollDown.box_mouseOverColor = constants.COLOR_BUTTON
        elif INV_SCROLL_INDEX >= ((inventoryWindowHeight // inventoryTextHeight) - invNum) * (-1):
            # enable the scroll up button
            scrollUp.disabled = False
            scrollUp.box_colorDefault = constants.COLOR_BUTTON
            scrollUp.box_mouseOverColor = constants.COLOR_BUTTON
            # grey-out the scroll down button
            scrollDown.disabled = True
        else:
            scrollUp.disabled = False
            scrollDown.disabled = False
            scrollUp.box_colorDefault = constants.COLOR_BUTTON
            scrollUp.box_mouseOverColor = constants.COLOR_BUTTON
            scrollDown.box_colorDefault = constants.COLOR_BUTTON
            scrollDown.box_mouseOverColor = constants.COLOR_BUTTON
    else:
        # make all the scroll buttons invisible and disabled
        scrollUp.disabled = True
        scrollUp.visibleWhenDisabled = False
        scrollDown.disabled = True
        scrollDown.visibleWhenDisabled = False

    #################
    ## info window ##
    #################

    # margins
    textStartX = infoWindowMargin * 2
    textStartY = infoWindowMargin
    lineMaxWidth = (infoWindowWidth - (infoWindowMargin * 2))

    # get item info
    if (mouseInventory and
        mouseLineSelect <= len(printList) - 1):
        itemInfo = PLAYER.container.inventory[mouseLineSelect].info + ' '
    else:
        itemInfo = ''

    # word wrap vars
    word = ''
    lastLineWidth = 0
    iter = 0
    i = 0
    isTag = False
    tag = ''
    textColor = constants.COLOR_TEXT_INV_INFO
    textColorIndex = { 'white'      : constants.COLOR_TEXT_WHITE,
                       'pink'       : constants.COLOR_TEXT_PINK,
                       'red'        : constants.COLOR_TEXT_RED,
                       'drkRed'     : constants.COLOR_TEXT_DARK_RED,
                       'orange'     : constants.COLOR_TEXT_ORANGE,
                       'yellow'     : constants.COLOR_TEXT_YELLOW,
                       'liGreen'    : constants.COLOR_TEXT_LIGHT_GREEN,
                       'green'      : constants.COLOR_TEXT_GREEN,
                       'drkGreen'   : constants.COLOR_TEXT_DARK_GREEN,
                       'cyan'       : constants.COLOR_TEXT_CYAN,
                       'liBlue'     : constants.COLOR_TEXT_LIGHT_BLUE,
                       'blue'       : constants.COLOR_TEXT_BLUE,
                       'drkBlue'    : constants.COLOR_TEXT_DARK_BLUE,
                       'purple'     : constants.COLOR_TEXT_PURPLE,
                       'liGrey'     : constants.COLOR_TEXT_LIGHT_GREY,
                       'grey'       : constants.COLOR_TEXT_GREY,
                       'drkGrey'    : constants.COLOR_TEXT_DARK_GREY,
                       'dmgHP'      : constants.COLOR_DAMAGE_HP,
                       'dmgMP'      : constants.COLOR_DAMAGE_MP,
                       'healHP'      : constants.COLOR_HEAL_HP,
                       'healMP'      : constants.COLOR_HEAL_MP,
                       'stats'      : constants.COLOR_STATS,}


    # go through every letter of itemInfo
    for letter in itemInfo:

        # starts new lines after the margin
        if lastLineWidth == 0:
            lastLineWidth = textStartX

        # if a tag is starting...
        if letter == '<':

            # toggle isTag to true
            isTag = True

            # clear word
            word = ''


        # end the tag and assign the color from the dictionary
        elif letter == '>':

            # tag is over, toggle isTag off
            isTag = False

            # look up our tag in the color dictionary and assign textColor
            textColor = textColorIndex[tag]

            # reset tag
            tag = ''

        # get what the tag is
        elif isTag:

            # letter will spell out our tag
            tag += letter

        # letters seperated by spaces are 'words'
        elif letter != ' ' and isTag == False:

            # if the letter is not a space, add it to the word
            word += letter

        # when we hit a space, see if we can add it to the line
        else:

            # add a space to the end of the word
            word += ' '

            # get width of word in pixels
            wordWidth = helperTextWidth(infoFont, word)

            # does this word fit on the line?
            if lastLineWidth + wordWidth < lineMaxWidth:

                # print on same line
                drawText(infoWindowSurf, word,
                        (lastLineWidth, (textStartY + (i * infoTextHeight))),
                        textColor,
                        font=constants.FONT_INV_INFO,
                        backColor=constants.COLOR_BLACK)

                # remember how far across the text window we are
                lastLineWidth += wordWidth

                # reset word
                word = ''

                # reset color
                textColor = constants.COLOR_TEXT_INV_INFO

            # word doesn't fit on the line
            else:

                # start a new line
                i += 1

                # start at the beginning of the window
                lastLineWidth = textStartX

                #print word to new line
                drawText(infoWindowSurf, word,
                        (lastLineWidth, (textStartY + (i * infoTextHeight))),
                        constants.COLOR_TEXT_INV_INFO,
                        font=constants.FONT_INV_INFO,
                        backColor=constants.COLOR_BLACK)

                # remembe how far across the text window we are
                lastLineWidth += wordWidth

                # reset word
                word = ''

                # reset color
                textColor = constants.COLOR_TEXT_INV_INFO


    #############
    ## drawing ##
    #############

    # blit our inventoryWindow onto the main window and position it (center it)
    inventoryWindow.fill(constants.COLOR_MENU)
    inventoryWindow.blit(localInventorySurf, (0, currentInvY))
    scrollUp.draw()
    scrollDown.draw()
    dropButton.draw()
    boxSurf.blit(inventoryWindow, (inventoryWindowX, inventoryWindowY))
    boxSurf.blit(infoWindowSurf, (infoWindowX, infoWindowY))

    FRAME_INV.surface.blit(boxSurf, (boxX, boxY))

def drawCurrentDungeonMessage():

    # this prints what dungeon level the player is currently on
    # onto the upper-right corner of the BOX_MAP

    # the message that the player will see
    dungeonText = 'Dungeon Level: ' + str(CURRENT_DUNGEON_LEVEL)
    dungeonTextFont = constants.FONT_MESSAGE_TEXT

    # width of that text
    dungeonTextWidth = helperTextWidth(dungeonTextFont, dungeonText)
    dungeonTextHeight = helperTextHeight(dungeonTextFont)

    # dungeonLevelSurf
    dungeonLevelSurf = pygame.Surface((dungeonTextWidth, dungeonTextHeight))

    # clear the dungeonLevel Surf
    dungeonLevelSurf.fill(constants.COLOR_MAP_FOG)

    # draw the dungeon level on the upper-right of the map
    drawText(dungeonLevelSurf,
             dungeonText,
             (0, 0),
             constants.COLOR_WHITE,
             dungeonTextFont)

    # blit the dungeon message surface onto the box_map
    FRAME_MAP.surface.blit(dungeonLevelSurf, ((FRAME_MAP.width) - (dungeonTextWidth + FRAME_MAP.border), FRAME_MAP.border))


def drawGame():

    SURFACE_MAP.fill(constants.COLOR_MAP_FOG)

    # update possition of camera
    CAMERA.update()

    # draw map
    drawMap(GAME.currentMap)

    drawCurrentDungeonMessage()

    # draw actors
    for obj in sorted(GAME.currentObj, key = lambda obj: obj.depth, reverse = True):
        obj.draw()

    # draw the gui
    drawGUI()

    # update Inventory window
    drawInventory()

    # update character GUI
    drawCharGUI()

    # draw the frame rate
    drawDebug()

    # draw the messages console
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

            tileAssignment = mapToDraw[x][y].assignment

            isVisible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if isVisible:

                # the player will remember this tile when not seen
                mapToDraw[x][y].explored = True

                if mapToDraw[x][y].blockPath == True:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.blueBrickDict[tileAssignment], (x * constants.CELL_WIDTH,
                                                      y * constants.CELL_HEIGHT))
                else:
                    # draw floor
                    SURFACE_MAP.blit(ASSETS.S_FLOOR, (x * constants.CELL_WIDTH,
                                                       y * constants.CELL_HEIGHT))

            #if not visible, but is explored
            elif mapToDraw[x][y].explored:

                if mapToDraw[x][y].blockPath == True:
                    # draw wall
                    SURFACE_MAP.blit(ASSETS.blueBrickExploredDict[tileAssignment],
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

    FRAME_CONSOLE.surface.fill(FRAME_CONSOLE.color)
    FRAME_CONSOLE.drawBorder()
    if len(GAME.msgHistory) <= constants.NUM_MESSAGES:
        toDraw = GAME.msgHistory
    else:
        toDraw = GAME.msgHistory[-constants.NUM_MESSAGES:]

    textHeight = helperTextHeight(constants.FONT_DEBUG_MESSAGE)

    startX, startY = FRAME_CONSOLE.topleft

    i = 0

    for message, color in toDraw:
        # drawText(surface, message, x, y)
        drawText(FRAME_CONSOLE.surface, message,
                 (startX, (startY + (i * textHeight))), color, font=constants.FONT_MESSAGE_TEXT,
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
        r, g, b, a = rectColor
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


def helperTextWidth(font, text = 'A'):
    fontObj = font.render(text, False, (0, 0, 0))
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
        for obj in GAME.currentObj:
            if obj.x == mapCoordsX and obj.y == mapCoordsY:
                if obj.scentStrength:
                    gameMessage(obj.nameObject + 'strength :' + str(obj.scentStrength))
                if obj == target:
                    gameMessage(target.displayName, constants.COLOR_WHITE)
                    gameMessage('HP: ' + str(target.creature.currentHP) + '/' +
                                str(target.creature.maxHP), constants.COLOR_RED)
                    gameMessage('MP: ' + str(target.creature.currentMP) + '/' +
                                str(target.creature.maxMP), constants.COLOR_CYAN)
                gameMessage(str(obj.nameObject), constants.COLOR_WHITE)

        gameMessage('Map Address: (' + str(mapCoordsX) + ',' +
                    str(mapCoordsY) + ')', constants.COLOR_LIGHT_GREY)



def cast_heal(target, value, cost = -100):
    if target.creature.currentMP < cost:
        gameMessage("Not enough MP!", constants.COLOR_CYAN)
        return 'canceled'
    elif target.creature.currentHP == target.creature.maxHP:
        gameMessage(target.displayName + ' is at full health!', constants.COLOR_WHITE)
        return 'canceled'
    else:
        if cost > 0:
            target.creature.currentMP -= cost
        gameMessage(target.displayName + ' is healed for ' + str(value), constants.COLOR_GREEN)
        target.creature.heal(value)
        gameMessage(target.displayName + ' health is now ' +
                    str(target.creature.currentHP) + '/' + str(target.creature.maxHP), constants.COLOR_WHITE)
        return 'cast heal'

def cast_heal_mana(target, value, cost = -100):
    if target.creature.currentMP < cost:
        gameMessage("Not enough MP!", constants.COLOR_CYAN)
        return 'canceled'
    elif target.creature.currentMP == target.creature.maxMP:
        gameMessage(target.displayName + ' is at full mana!', constants.COLOR_WHITE)
        return 'canceled'
    else:
        if cost > 0:
            target.creature.currentMP -= cost
        gameMessage(target.displayName + "'s mana is healed for " + str(value), constants.COLOR_CYAN)
        target.creature.healMP(value)
        gameMessage(target.displayName + ' MP is now ' +
                    str(target.creature.currentMP) + '/' + str(target.creature.maxMP), constants.COLOR_WHITE)
        return 'cast heal mana'


def cast_lightning(caster,
                   T_damage_maxRange = (5, 5),
                   cost = -100,
                   local_penetrateWalls=False,
                   penetrateCreatures=True,
                   local_lineColor=constants.COLOR_WHITE,
                   local_lineAlpha=100):

    if caster.creature.currentMP < cost:
            gameMessage("Not enough MP!", constants.COLOR_CYAN)
            return 'canceled'

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
        # deduct mp cost
        if cost > 0:
            caster.creature.currentMP -= cost
        # apply damage to everything in the list
        for i, (x, y) in enumerate(listOfTiles):
            target = mapCheckForCreature(x, y)
            # if there is a target its not the caster
            if target:
                gameMessage(target.displayName + ' is hit by the lightning!', constants.COLOR_WHITE)
                target.creature.takeDamage(damage)
        return 'cast lightning'


def cast_fireball(caster,
                  T_damage_radius_maxRange=(6, 1, 5),
                  cost = -100):

    # check if enough MP
    if caster.creature.currentMP < cost:
        gameMessage("Not enough MP!", constants.COLOR_CYAN)
        return 'canceled'

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


    # cast fireball
    else:
        if cost > 0:
            caster.creature.currentMP -= cost
        for x, y in listOfRadiusTiles:

            target = mapCheckForCreature(x, y)
            # damage everything in radius
            if target:
                gameMessage(target.displayName + ' is hit by the fireball!', constants.COLOR_ORANGE)
                target.creature.takeDamage(damage)
        return 'cast fireball'


def cast_confusion(caster=None,
                   spellDuration=5,
                   cost = -100):

    # check for enough MP
    if caster.creature.currentMP < cost:
        gameMessage("Not enough MP!", constants.COLOR_CYAN)
        return 'canceled'

    # select tile
    selectedTile = menu_tileSelect(tileColor=constants.COLOR_PURPLE,)
    if selectedTile == 'canceled':
        return 'canceled'
    else:
        x, y = selectedTile
        # get target
        target = mapCheckForCreature(x, y)


    # cast confusion
    if target:
        if cost > 0:
            caster.creature.currentMP -= cost
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

class ui_frame:
    def __init__(self,
                 width,
                 height,
                 T_coords,
                 border = 10,
                 color = constants.COLOR_BLACK):
        self.width = width
        self.height = height
        self.T_coords = T_coords
        self.innerBorderRect = pygame.Rect((4,4), (self.width -7, self.height -7))
        self.borderRect = pygame.Rect((1,1), (self.width -2, self.height -2))
        self.border = border
        self.color = color
        self.x, self.y = self.T_coords

        # these are reference only, only altering topleft will move the surface

        # of the surface
        self.surfTopleft = T_coords
        self.surfTopright = (self.x + self.width, self.y)
        self.surfBottomleft = (self.x, self.y + self.height)
        self.surfBottomright = (self.x + self.width, self.y + self.height)
        self.surface = pygame.Surface((self.width, self.height))

        # workable coords (inside the border)
        self.topleft = (self.border, self.border)
        self.topright = ((self.width - self.border), self.border)
        self.bottomleft = (self.border, (self.height - self.border))
        self.bottomright = ((self.width - self.border), (self.height - self.border))
        self.surface = pygame.Surface((self.width, self.height))
    def drawBorder(self):
        pygame.draw.rect(self.surface, constants.COLOR_LIGHT_GREY, self.borderRect, 2)
        pygame.draw.rect(self.surface, constants.COLOR_GREY, self.innerBorderRect, 1)


class ui_Button:
    def __init__(self, destSurface, buttonText, size, T_coordsCenter,
                 Xoffset,
                 Yoffset,
                 spriteKey = None,
                 mouseOverSpriteKey = None,
                 box_mouseOverColor = None,
                 box_colorDefault = None,
                 box_clickColor = None,
                 text_mouseOverColor = None,
                 text_colorDefault = None,
                 text_clickColor = None,
                 disabled = False,
                 visibleWhenDisabled = True,
                 pointlist = None,
                 polyWidth = 0):

        self.destSurface = destSurface
        self.buttonText  = buttonText
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.T_coordsCenter = T_coordsCenter

        self.Xoffset = Xoffset
        self.Yoffset = Yoffset

        self.spriteKey = spriteKey
        if self.spriteKey:
            self.sprite = ASSETS.animationDict[self.spriteKey]
        self.mouseOverSpriteKey = mouseOverSpriteKey
        if self.mouseOverSpriteKey:
            self.mouseOverSprite = ASSETS.animationDict[self.mouseOverSpriteKey]

        self.box_mouseOverColor = box_mouseOverColor
        self.box_colorDefault = box_colorDefault
        self.box_clickColor = box_clickColor
        self.text_mouseOverColor = text_mouseOverColor
        self.text_colorDefault = text_colorDefault
        self.text_clickColor = text_clickColor

        # disabled behavior
        self.disabled = disabled
        self.visibleWhenDisabled = visibleWhenDisabled

        # polygonal button features
        self.pointlist = pointlist
        self.polyWidth = polyWidth
        self.polyWidthConst = self.polyWidth

        self.box_currentColor = box_colorDefault
        self.text_currentColor = text_colorDefault

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = T_coordsCenter

    @property
    def mouseInSurface(self):
        # dimensions of our window
        windowWidth = constants.WINDOW_WIDTH
        windowHeight = constants.WINDOW_HEIGHT

        # dimensions of our Button
        if self.spriteKey == None:
            surfaceX, surfaceY = self.rect.topleft
        else:
            surfaceX, surfaceY = self.T_coordsCenter

        surfaceWidth, surfaceHeight = self.size
        # get mouse x, y
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX_rel = mouseX - self.Xoffset - surfaceX
        mouseY_rel = mouseY - self.Yoffset - surfaceY
        mouseInSurface = (mouseX_rel >= 0 and
                          mouseY_rel >= 0 and
                          mouseX_rel <= surfaceWidth and
                          mouseY_rel <= surfaceHeight)
        return mouseInSurface

    def update(self, playerInput):
        buttonPressed = False
        if self.disabled == False:
            if self.mouseInSurface:
                for event in playerInput:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            buttonPressed = True
        else:
            buttonPressed = False

        return buttonPressed

    def draw(self):
        if self.spriteKey == None:
            if not self.disabled:
                if self.mouseInSurface:
                    if self.box_mouseOverColor:
                        self.box_currentColor = self.box_mouseOverColor
                        self.text_currentColor = self.text_mouseOverColor
                        self.polyWidth = 0
                    else:
                        self.box_currentColor += pygame.Color(100, 100, 100, 0)
                else:
                    self.box_currentColor = self.box_colorDefault
                    self.text_currentColor = self.text_colorDefault
                    self.polyWidth = self.polyWidthConst
            else:
                if self.visibleWhenDisabled:
                    self.box_currentColor = constants.COLOR_LIGHT_GREY
                    self.text_currentColor = constants.COLOR_WHITE

            if self.pointlist == None:
                pygame.draw.rect(self.destSurface, self.box_currentColor, self.rect)
            else:
                pygame.draw.polygon(self.destSurface, self.box_currentColor, self.pointlist, self.polyWidth)

            drawText(self.destSurface,
                     self.buttonText,
                     T_coords = self.T_coordsCenter,
                     textColor = self.text_currentColor,
                     centered = True)

        else:
            if self.mouseInSurface:
                self.surface.blit(self.mouseOverSprite, (-8, -8))
                self.destSurface.blit(self.surface, self.T_coordsCenter)
            else:
                self.surface.blit(self.sprite, (-8, -8))
                self.destSurface.blit(self.surface, self.T_coordsCenter)




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
        windowWidth = constants.WINDOW_WIDTH
        windowHeight = constants.WINDOW_HEIGHT

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

class ui_FillBar:
    def __init__(self,
                 destSurf,
                 T_coords,
                 currentValue,
                 maxValue,
                 width,
                 height,
                 fillColor = constants.COLOR_GREEN,
                 emptyColor = constants.COLOR_RED):

        # what surface this fill bar will be blitted to and it coords
        self.destSurf = destSurf
        self.T_coords = T_coords

        ## PARAMETERS
        # current value, (percentage of maxValue that currentValue is)
        self.currentValue = currentValue
        self.maxValue = maxValue

        # DIMENSIONS
        self.width = width
        self.height = height

        # COLORS
        self.fillColor = fillColor
        self.emptyColor = emptyColor

        # SURFS AND RECTS
        self.fillRect = pygame.Rect((0, 0), (self.width, self.height))
        self.fillRect.left = 0
        self.emptyRect = pygame.Rect((0, 0), (self.width, self.height))
        self.emptyRect.right = self.width
        self.fillBarSurf = pygame.Surface((width, height))

    @property
    def currentValueInX(self):
        value = self.currentValue / self.maxValue
        valueX = value * self.width
        return valueX

    def draw(self, T_coords):

        self.fillRect.right = self.currentValueInX
        self.emptyRect.left = self.currentValueInX

        pygame.draw.rect(self.fillBarSurf, self.fillColor, self.fillRect)
        pygame.draw.rect(self.fillBarSurf, self.emptyColor, self.emptyRect)

        self.destSurf.blit(self.fillBarSurf, (self.T_coords))





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

    global MASTER_EVENTS

    # Title surface dimentions
    titleSurfDimX = constants.WINDOW_WIDTH * 0.75
    titleSurfDimY = constants.WINDOW_HEIGHT * .5
    windowCenterX = constants.WINDOW_WIDTH * .5
    windowCenterY = constants.WINDOW_HEIGHT * .5
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
                           titleSurfBottomY + (buttonHeight * 1.5)),
                           0, 0,
                           box_mouseOverColor = constants.COLOR_RED,
                           box_colorDefault = constants.COLOR_BLUE,
                           text_mouseOverColor = constants.COLOR_WHITE,
                           text_colorDefault = constants.COLOR_WHITE)

    loadGameButton = ui_Button(SURFACE_MAIN,
                           'Continue',
                           (buttonWidth, buttonHeight),
                           (windowCenterX + (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 1.5)),
                           0, 0,
                           box_mouseOverColor = constants.COLOR_RED,
                           box_colorDefault = constants.COLOR_BLUE,
                           text_mouseOverColor = constants.COLOR_WHITE,
                           text_colorDefault = constants.COLOR_WHITE,
                           disabled = True)

    optionsButton = ui_Button(SURFACE_MAIN,
                           'Options',
                           (buttonWidth, buttonHeight),
                           (windowCenterX + (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 3)),
                           0, 0,
                           box_mouseOverColor = constants.COLOR_RED,
                           box_colorDefault = constants.COLOR_BLUE,
                           text_mouseOverColor = constants.COLOR_WHITE,
                           text_colorDefault = constants.COLOR_WHITE,)

    quitGameButton = ui_Button(SURFACE_MAIN,
                           'Quit',
                           (buttonWidth, buttonHeight),
                           (windowCenterX - (buttonWidth),
                           titleSurfBottomY + (buttonHeight * 3)),
                           0, 0,
                           box_mouseOverColor = constants.COLOR_RED,
                           box_colorDefault = constants.COLOR_BLUE,
                           text_mouseOverColor = constants.COLOR_WHITE,
                           text_colorDefault = constants.COLOR_WHITE,)
    while menuRunning:
        eventsList = pygame.event.get()
        mousePosX, mousePosY = pygame.mouse.get_pos()

        menuInput = (eventsList)

        for event in menuInput:
            if event.type == pygame.QUIT:
                gameExit(save = False)

            if event.type == pygame.KEYDOWN:

                # quick quit
                if event.key == pygame.K_q:
                    gameExit(save = False)

        # whether the continue button is disabled or not
        saveExists = os.path.isfile(constants.PATH + "/data/savegame")
        if saveExists:
            loadGameButton.disabled = False
        else:
            loadGameButton.disabled = True

        newGame = newGameButton.update(menuInput)
        loadGame = loadGameButton.update(menuInput)
        quit = quitGameButton.update(menuInput)
        options = optionsButton.update(menuInput)

        if newGame:
            pygame.mixer.music.stop()
            gameStart()


        if loadGame and loadGameButton.disabled == False:
            pygame.mixer.music.stop()
            gameStart(False)


        if quit:
            pygame.quit()
            exit()
            break
        if options:
            menu_mainOptions()

        # draw menu
        SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

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
    windowWidth = constants.WINDOW_WIDTH
    windowHeight = constants.WINDOW_HEIGHT

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

        SURFACE_MAIN.blit(optionsSurf,
                          (menuX, menuY))

        CLOCK.tick(constants.GAME_FPS)
        # actually draw everything
        pygame.display.update()

def menu_pause():

    # toggle variable
    menuClose = False

    # menu gui
    windowWidth = constants.WINDOW_WIDTH
    windowHeight = constants.WINDOW_HEIGHT
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


def menu_magic():

    # toggle the menu
    menuClose = False

    # dimensions of menu and main window
    windowWidth = constants.WINDOW_WIDTH
    windowHeight = constants.WINDOW_HEIGHT

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
                            result = cast_lightning(PLAYER, cost=5)
                        if printList[mouseLineSelect] == 'Fireball':
                            result = cast_fireball(PLAYER, cost=5)
                        if printList[mouseLineSelect] == 'Confuse':
                            result = cast_confusion(PLAYER, cost=5)

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


        drawGUI()
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
                    return ('canceled', None)

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

        drawGUI()
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

    containerCom = com_Container(inventory = [])

    scentCom = com_Scent(strength = 5)
    creatureCom = com_Creature("greg", maxMP = 11, baseAtk=4, faction='player', deathFunc = death_Player, scent = scentCom)

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
        stairs = obj_Actor(x, y, 'descending stairs',
                  animationKey = "S_STAIRS_DOWN",
                  stairs = stairs_com,
                  depth = constants.DEPTH_DECOR)

    else:
        stairs_com = com_Stairs(downwards = False)
        stairs = obj_Actor(x, y, 'ascending stairs',
                           animationKey = "S_STAIRS_UP",
                           stairs = stairs_com,
                           depth = constants.DEPTH_DECOR)


    GAME.currentObj.append(stairs)

def gen_exitPortal(T_coords):
    x, y = T_coords

    exitPortal_com = com_Exitportal()
    exitPortal = obj_Actor(x, y, 'Exit Portal',
                           animationKey = "A_PORTAL_CLOSED",
                           animationSpeed = 2,
                           exitPortal = exitPortal_com,
                           depth = constants.DEPTH_DECOR)

    GAME.currentObj.append(exitPortal)

def gen_wincon(T_coords):
    x, y = T_coords

    item_com = com_Item()

    wincon = obj_Actor(x, y,
                             nameObject='Amulet of Nocniw',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "A_WINCON",
                             animationSpeed=2,
                             item=item_com)

    GAME.currentObj.append(wincon)

###########
## ITEMS ##
###########

# master generators
def gen_item(T_coords, mustGen = False):

    newItem = None

    if mustGen:
        while newItem == None:
            randNum = libtcod.random_get_int(0, 1, 10)
            if randNum == 1:
                newItem = gen_scroll(T_coords)
                GAME.currentObj.append(newItem)
            elif randNum == 2:
                newItem = gen_weapon(T_coords)
                GAME.currentObj.append(newItem)
            elif randNum == 3:
                newItem = gen_armor_shield(T_coords)
                GAME.currentObj.append(newItem)
            elif randNum == 4:
                coin = libtcod.random_get_int(0, 0, 1)
                if coin == 0:
                    newItem = gen_potion_health_minor(T_coords)
                    GAME.currentObj.append(newItem)
                else:
                    newItem = gen_potion_mana_minor(T_coords)
                    GAME.currentObj.append(newItem)
    else:
        randNum = libtcod.random_get_int(0, 1, 10)
        if randNum == 1:
            newItem = gen_scroll(T_coords)
            GAME.currentObj.append(newItem)
        elif randNum == 2:
            newItem = gen_weapon(T_coords)
            GAME.currentObj.append(newItem)
        elif randNum == 3:
            newItem = gen_armor_shield(T_coords)
            GAME.currentObj.append(newItem)
        elif randNum == 4:
            coin = libtcod.random_get_int(0, 0, 1)
            if coin == 0:
                newItem = gen_potion_health_minor(T_coords)
                GAME.currentObj.append(newItem)
            else:
                newItem = gen_potion_mana_minor(T_coords)
                GAME.currentObj.append(newItem)

def gen_scroll(T_coords):
    randNum = libtcod.random_get_int(0, 1, 3)

    if randNum == 1: newItem = gen_scroll_lightning(T_coords)
    elif randNum == 2: newItem = gen_scroll_fireball(T_coords)
    else: newItem = gen_scroll_confusion(T_coords)

    return newItem

# specific

def gen_weapon(T_coords):

    # where in the room the item will generate
    x, y = T_coords

    # a 1:5 chance of a bonus beyond current level
    extraBonus = libtcod.random_get_int(0, 1, 20)
    if extraBonus == 10:
        extraBonus = 1
    else:
        extraBonus = 0

    # bonus appropriate for the dungeon level
    ranBonus = libtcod.random_get_int(0, 1, CURRENT_DUNGEON_LEVEL)

    # actual total bonus
    totalBonus = ranBonus + extraBonus

    # name with bonus
    name = '+' + str(totalBonus) + ' Sword'

    # equipment component
    equipmentCom = com_Equipment(attackBonus=ranBonus, slot = "right_hand")

    # generate the actual item
    returnObj = obj_Actor(x, y,
                          name,
                          depth = constants.DEPTH_ITEM,
                          animationKey = "S_SWORD",
                          equipment = equipmentCom,
                          info = "Increase your attack, <stats>+" + str(totalBonus) + " damage!")
    return returnObj

def gen_armor_shield(T_coords):

    # where in the room the item will generate
    x, y = T_coords

    # a 1:5 chance of a bonus beyond current level
    extraBonus = libtcod.random_get_int(0, 1, 20)
    if extraBonus == 10:
        extraBonus = 1
    else:
        extraBonus = 0

    # bonus appropriate for the dungeon level
    ranBonus = libtcod.random_get_int(0, 1, int(CURRENT_DUNGEON_LEVEL // 2))
    if ranBonus < 1: ranBonus = 1

    # actual total bonus
    totalBonus = ranBonus + extraBonus

    # name with bonus
    name = '+' + str(totalBonus) + ' Shield'

    # equipment component
    equipmentCom = com_Equipment(defenseBonus=ranBonus, slot = "left_hand")

    # generate the actual item
    returnObj = obj_Actor(x, y,
                          name,
                          depth = constants.DEPTH_ITEM,
                          animationKey = "S_SHIELD",
                          equipment = equipmentCom,
                          info = "Protects the wielder, <stats>+" + str(totalBonus) + " def!")
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
                             item=item_com,
                             info = "Electrocute all enemies in a line <stats>" + str(maxRange) +
                                    " tiles long from the player for <stats>" + str(damage) + " damage!")

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
                             item=item_com,
                             info = "Hurl a fireball up to <stats>" + str(maxRange) +
                                    " tiles away. Fireball explodes, damaging everything for <stats>" + str(damage) +
                                    " points in a radius of <stats>" + str(radius) + " tile(s)!")

    return returnObject

def gen_scroll_confusion(T_coords):

    x, y = T_coords

    numTurns = libtcod.random_get_int(0, 2, 8)

    item_com = com_Item(useFunc = cast_confusion, value=numTurns)

    returnObject = obj_Actor(x, y,
                             nameObject='Confusion Scroll',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_SCROLL_03",
                             item=item_com,
                             info = "Enemy wanders around confused for <stats>" + str(numTurns) + " turns!")

    return returnObject

def gen_potion_health_minor(T_coords):

    x, y = T_coords

    healVal = libtcod.random_get_int(0, 5, 8)

    item_com = com_Item(useFunc = cast_heal, value=healVal)

    returnObject = obj_Actor(x, y,
                             nameObject='Minor Heal Potion',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_HEALTH_POTION",
                             item=item_com,
                             info = "Heal HP by <healHP>" + str(healVal) + " points!")

    return returnObject

def gen_potion_mana_minor(T_coords):

    x, y = T_coords

    healVal = libtcod.random_get_int(0, 5, 8)

    item_com = com_Item(useFunc = cast_heal_mana, value=healVal)

    returnObject = obj_Actor(x, y,
                             nameObject='Minor Mana Potion',
                             depth = constants.DEPTH_ITEM,
                             animationKey= "S_MANA_POTION",
                             item=item_com,
                             info = "Heal MP by <healMP>" + str(healVal) + " points!")

    return returnObject

# gen enemies

def gen_enemy(T_coords):

    enemyDict = {
    1 : gen_snake(T_coords),
    2 : gen_alchemist(T_coords),
    3 : gen_spider_tarantula(T_coords),
    4 : gen_spider_tarantula_giant_zombie(T_coords),
    5 : gen_snail(T_coords),
    6 : gen_fernoid(T_coords),
    7 : gen_death_crack(T_coords),
    8 : gen_rodent(T_coords)
    }

    bestiaryLen = len(enemyDict)
    randNum = libtcod.random_get_int(0, 1, 100)

    currentLevel = CURRENT_DUNGEON_LEVEL

    success = False
    i = 0
    while True:

        if randNum <= 80:
            randMob = libtcod.random_get_int(0, 1, bestiaryLen)

            potentialEnemy = enemyDict[randMob]

            if potentialEnemy.creature.dungeonLevel - currentLevel <= 1:
                newEnemy = potentialEnemy
                return newEnemy
        i += 1

        if i > 1000:
            gameMessage("Failed to gen mob")
            return 'gen fail'

############
## SNAKES ##
############

def gen_snake(T_coords):
    # generate an appropriate snake for the current dungeon level

    # what our alog spits out, before we confirm it
    potentialMob = None

    # our confirmed mob
    mob = None

    # dict of all snakes
    snakeDict = { 1 : gen_snake_neonates(T_coords),
                   2 : gen_snake_snakelet(T_coords),
                   3 : gen_snake_adult(T_coords) }

    #iterator
    i = len(snakeDict)

    # loop through rodents untill we get an appropriate one
    while True:
        # gen a mob from highest level to lowest
        potentialMob = snakeDict[i]

        # if that mobs level is == or +1 the current dungeon level, keep it
        if potentialMob.creature.dungeonLevel - CURRENT_DUNGEON_LEVEL < 2:
            # use the mob
            return potentialMob
        # else, check the next lowest level mob
        else:
            i -= 1
        # if we have run out of mobs
        if i == 0:
            gameMessage('failed to gen snake')
            # fail
            return

def gen_snake_neonates(T_coords):
    # choose what kind of snakelet
    ranNum = libtcod.random_get_int(0, 1, 3)

    # anaconda
    if ranNum == 1:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 4, 5)
        baseAttack = libtcod.random_get_int(0 , 1, 2)
        nutrition = libtcod.random_get_int(0, 2, 4)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=1)
        aiCom = ai_chase()
        neonates = obj_Actor(x, y, "neonates anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)


        return neonates

    # cobra
    elif ranNum == 2:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 3, 4)
        baseAttack = libtcod.random_get_int(0 , 3, 3)
        nutrition = libtcod.random_get_int(0, 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=1)
        aiCom = ai_chase()
        neonates = obj_Actor(x, y, "neonates cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)


        return neonates

    #green snake
    else:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 4, 4)
        baseAttack = libtcod.random_get_int(0 , 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    faction = 'neonates',
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel = 1)
        aiCom = ai_chase()
        neonates = obj_Actor(x, y, "green neonates",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_GREEN_01",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)


        return neonates

def gen_snake_snakelet(T_coords):
    # choose what kind of snakelet
    ranNum = libtcod.random_get_int(0, 1, 3)

    # anaconda
    if ranNum == 1:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 7, 10)
        baseAttack = libtcod.random_get_int(0 , 3, 4)
        nutrition = libtcod.random_get_int(0, 2, 4)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=2)
        aiCom = ai_chase()
        snakelet = obj_Actor(x, y, "snakelet anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)


        return snakelet

    # cobra
    elif ranNum == 2:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 5, 8)
        baseAttack = libtcod.random_get_int(0 , 3, 5)
        nutrition = libtcod.random_get_int(0, 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=2)
        aiCom = ai_chase()
        snakelet = obj_Actor(x, y, "snakelet cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)


        return snakelet

    #green snake
    else:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 4, 5)
        baseAttack = libtcod.random_get_int(0 , 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    faction = 'snakelet',
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel = 2)
        aiCom = ai_chase()
        snakelet = obj_Actor(x, y, "green snakelet",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_GREEN_01",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)



        return snakelet

def gen_snake_adult(T_coords):
    # choose what kind of snakelet
    ranNum = libtcod.random_get_int(0, 1, 3)

    # anaconda
    if ranNum == 1:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 10, 15)
        baseAttack = libtcod.random_get_int(0 , 4, 5)
        nutrition = libtcod.random_get_int(0, 3, 6)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=4)
        aiCom = ai_chase()
        snake = obj_Actor(x, y, "anaconda",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_ANACONDA_03",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)
        return snake

    # cobra
    elif ranNum == 2:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 8, 11)
        baseAttack = libtcod.random_get_int(0 , 4, 7)
        nutrition = libtcod.random_get_int(0, 2, 4)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=5)
        aiCom = ai_chase()
        snake = obj_Actor(x, y, "cobra",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_COBRA_03",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)
        return snake

    #green snake
    else:
        x, y = T_coords
        maxHealth = libtcod.random_get_int(0 , 6, 9)
        baseAttack = libtcod.random_get_int(0 , 3, 4)
        nutrition = libtcod.random_get_int(0, 2, 3)
        creatureName = libtcod.namegen_generate("Celtic female")
        creatureCom = com_Creature(creatureName,
                                    baseAtk=baseAttack,
                                    maxHP = maxHealth,
                                    deathFunc=death_Snake,
                                    dungeonLevel=4)
        aiCom = ai_chase()
        snake = obj_Actor(x, y, "green snake",
                                   depth = constants.DEPTH_CREATURE,
                                   animationKey = "A_SNAKE_GREEN_02",
                                   animationSpeed=2,
                                   creature=creatureCom,
                                   ai=aiCom)

        return snake


#############
## RODENTS ##
#############

def gen_rodent(T_coords):
    # generate an appropriate rodent for the current dungeon level

    # what our alog spits out, before we confirm it
    potentialMob = None

    # our confirmed mob
    mob = None

    # dict of all rodents
    rodentDict = { 1 : gen_mouse(T_coords),
                   2 : gen_rat(T_coords),
                   3 : gen_giant_rat(T_coords),
                   4 : gen_undead_rat(T_coords),
                   5 : gen_poison_rat(T_coords),
                   6 : gen_hunter_rat(T_coords) }

    #iterator
    i = len(rodentDict)

    # loop through rodents untill we get an appropriate one
    while True:
        # gen a mob from highest level to lowest
        potentialMob = rodentDict[i]

        # if that mobs level is == or +1 the current dungeon level, keep it
        if potentialMob.creature.dungeonLevel - CURRENT_DUNGEON_LEVEL < 2:
            # use the mob
            return potentialMob
        # else, check the next lowest level mob
        else:
            i -= 1
        # if we have run out of mobs
        if i == 0:
            gameMessage('failed to gen rodent')
            # fail
            return

def gen_mouse(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 4, 5)
    baseAttack = libtcod.random_get_int(0, 2, 3)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=1)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_MOUSE",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return rat

def gen_rat(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 5, 7)
    baseAttack = libtcod.random_get_int(0, 4, 6)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=3)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_RAT",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)


    return rat

def gen_giant_rat(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 12, 16)
    baseAttack = libtcod.random_get_int(0, 5, 7)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=5)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "giant rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_GIANT_RAT",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return rat

def gen_undead_rat(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 16, 20)
    baseAttack = libtcod.random_get_int(0, 8, 10)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=7)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "undead rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_UNDEAD_RAT",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return rat

def gen_poison_rat(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 15, 17)
    baseAttack = libtcod.random_get_int(0, 6, 7)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=9)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "poison rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_POISON_RAT",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return rat

def gen_hunter_rat(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 20, 25)
    baseAttack = libtcod.random_get_int(0, 10, 10)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'rodent',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=9)
    aiCom = ai_chase()
    rat = obj_Actor(x, y, "hunter rat",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_HUNTER_RAT",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return rat

#############
## SPIDERS ##
#############

def gen_spider_tarantula(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 4, 5)
    baseAttack = libtcod.random_get_int(0, 6, 8)
    creatureName = libtcod.namegen_generate("Celtic female")
    creatureCom = com_Creature(creatureName,
                                faction = 'tarantula',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=3)
    aiCom = ai_chase()
    spider = obj_Actor(x, y, "tarantula",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_SPIDER_TARANTULA",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return spider

def gen_spider_tarantula_giant_zombie(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 5, 6)
    baseAttack = libtcod.random_get_int(0, 8, 10)
    creatureName = libtcod.namegen_generate("Celtic female")
    creatureCom = com_Creature(creatureName,
                                faction = 'tarantula zombie',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=5)
    aiCom = ai_chase()
    spider = obj_Actor(x, y, "giant zombie tarantula",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_SPIDER_TARANTULA_GIANT_ZOMBIE",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return spider

def gen_fernoid(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 10, 12)
    baseAttack = libtcod.random_get_int(0, 2, 3)
    creatureName = libtcod.namegen_generate("Celtic female")
    creatureCom = com_Creature(creatureName,
                                faction = 'fernoid',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=3)
    aiCom = ai_chase()
    fernoid = obj_Actor(x, y, "fernoid",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_FERNOID",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return fernoid

def gen_death_crack(T_coords):
    x, y = T_coords

    maxHealth = libtcod.random_get_int(0, 20, 25)
    baseAttack = libtcod.random_get_int(0, 3, 4)
    creatureName = libtcod.namegen_generate("Celtic female")
    creatureCom = com_Creature(creatureName,
                                faction = 'shade',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=4)
    aiCom = ai_chase()
    shade = obj_Actor(x, y, "death crack",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_DEATH_CRACK",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return shade

def gen_alchemist(T_coords):

    alchemist = None

    x, y = T_coords
    maxHealth = libtcod.random_get_int(0 , 4, 5)
    baseAttack = libtcod.random_get_int(0 , 2, 3)
    potionVal = libtcod.random_get_int(0, 3, 5)
    hasPotion = libtcod.random_get_int(0, 0, 2)
    creatureName = libtcod.namegen_generate("Celtic male")
    creatureCom = com_Creature(creatureName,
                                faction = 'alchemist',
                                baseAtk=baseAttack,
                                maxHP = maxHealth,
                                deathFunc=death_Mob,
                                dungeonLevel=3)
    containerCom = com_Container()
    containerCom.inventory = []
    aiCom = ai_chase()
    alchemist = obj_Actor(x, y, "alchemist",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_ALCHEMIST",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom,
                               container=containerCom)

    if hasPotion == 1:
        potion = gen_potion_health_minor(T_coords)
        potion.animationDestroy()
        alchemist.container.inventory.append(potion)
    elif hasPotion == 2:
        potion = gen_potion_mana_minor(T_coords)
        potion.animationDestroy()
        alchemist.container.inventory.append(potion)

    return alchemist

def gen_snail(T_coords):

    x, y = T_coords

    maxHealth = libtcod.random_get_int(0 , 5, 8)
    baseAttack = libtcod.random_get_int(0 , 1, 1)
    baseDefence = libtcod.random_get_int(0 , 2, 4)
    creatureName = libtcod.namegen_generate("Celtic female")
    creatureCom = com_Creature(creatureName,
                                faction = 'snail',
                                baseAtk=baseAttack,
                                baseDef = baseDefence,
                                maxHP = maxHealth,
                                deathFunc=death_Mob)
    aiCom = ai_chase()
    snail = obj_Actor(x, y, "snail",
                               depth = constants.DEPTH_CREATURE,
                               animationKey = "A_SNAIL",
                               animationSpeed=2,
                               creature=creatureCom,
                               ai=aiCom)

    return snail











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

    global SURFACE_MAIN, SURFACE_MAP, CURRENT_DUNGEON_LEVEL, GAME_LOOP_ITER
    global FRAME_MAP, BOX_MAP, FRAME_CONSOLE, FRAME_INV, FRAME_STATUS
    global CLOCK, FOV_CALC, FOV_MAP, ENEMY, ASSETS, PREF, CAMERA, RANDOM_ENGINE
    global INV_SCROLL_INDEX, IS_DROPPING

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
    SURFACE_MAIN = pygame.display.set_mode((constants.WINDOW_WIDTH,
                                           constants.WINDOW_HEIGHT))
    # sets up our map surface and camera
    SURFACE_MAP = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    # what dungeon level we are on
    CURRENT_DUNGEON_LEVEL = 1

    #################
    ## GUI GLOBALS ##
    #################

    # GUI frame for map
    FRAME_MAP = ui_frame(width = (constants.WINDOW_WIDTH * .75),
                         height = (constants.WINDOW_HEIGHT * .75),
                         T_coords = (0, 0),
                         color = constants.COLOR_PINK)
    #draw the border of the frame
    FRAME_MAP.drawBorder()

    # GUI frame for the console messages (lower right)
    FRAME_CONSOLE = ui_frame(width = (constants.WINDOW_WIDTH * .75),
                           height = (constants.WINDOW_HEIGHT - FRAME_MAP.height),
                           T_coords = (0, FRAME_MAP.height),
                           color = constants.COLOR_FRAME)
    FRAME_CONSOLE.drawBorder()

    # GUI frame for the PLAYER inventory (right side)
    FRAME_INV = ui_frame(width = (constants.WINDOW_WIDTH - FRAME_MAP.width),
                           height = (constants.WINDOW_HEIGHT * .75),
                           T_coords = (FRAME_MAP.width, 0),
                           color = constants.COLOR_FRAME)
    FRAME_INV.drawBorder()

    FRAME_STATUS = ui_frame(width = (constants.WINDOW_WIDTH - FRAME_MAP.width),
                           height = (constants.WINDOW_HEIGHT - FRAME_MAP.height),
                           T_coords = (FRAME_MAP.width, FRAME_MAP.height),
                           color = constants.COLOR_FRAME)
    FRAME_STATUS.drawBorder()

    # The GUI surface the map sits in
    BOX_MAP = pygame.Surface((FRAME_MAP.width - (FRAME_MAP.border * 2), FRAME_MAP.height - (FRAME_MAP.border * 2)))


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

    # this does nothing right now
    GAME_LOOP_ITER = 0

    # initializes what item we are scrolled to in the inventory window
    INV_SCROLL_INDEX = 0

    # if the user is selecting something to be dropped
    IS_DROPPING = False

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

    gameInit()
    GAME = obj_Game()
    currentMap, roomList = mapCreate()
    # GAME.currentMap = currentMap
    # GAME.roomList = roomList
    gen_player((0, 0))
    mapPlaceObjects(GAME.roomList)

def gameLoad():
    global GAME, PLAYER

    pygame.mixer.music.load(ASSETS.musicBkg)
    pygame.mixer.music.play(-1)

    with open(constants.PATH + 'data/savegame', 'rb') as file:
        GAME, PLAYER = pickle.load(file)

    for obj in GAME.currentObj:
        obj.animationInit()

    mapMakeFOV(GAME.currentMap)

def gameSave(save = True):

    if save:
        for obj in GAME.currentObj:
            obj.animationDestroy()
        # saves
        with open(constants.PATH + 'data/savegame', 'wb') as file:
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
    global FOV_CALC, MASTER_EVENTS
    # TODO gets all player inputs and makes a list out of them
    MASTER_EVENTS = pygame.event.get()
    keysList = pygame.key.get_pressed()

    #check for mod key
    modKey = (keysList[pygame.K_RSHIFT] or
              keysList[pygame.K_LSHIFT])

    for event in MASTER_EVENTS:
        if event.type == pygame.QUIT:
            return 'QUIT'

        if event.type == pygame.KEYDOWN:

            # quick quit
            if event.key == pygame.K_q:
                return 'QUIT'

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

            ###################
            ## TESTING MAGIC ##
            ###################

            if event.key == pygame.K_BACKQUOTE:
                cast_look()
            if event.key == pygame.K_1:
                cast_heal(PLAYER, 10, cost=0)
            if event.key == pygame.K_2:
                cast_heal_mana(PLAYER, 10, cost=0)
            if event.key == pygame.K_3:
                gen_item((PLAYER.x, PLAYER.y))

            # map testing
            if event.key == pygame.K_4:
                if CURRENT_DUNGEON_LEVEL < constants.MAP_NUM_LEVELS:
                    GAME.transitionNextMap()
            if event.key == pygame.K_5:
                GAME.transitionPreviousMap()

            if modKey and event.key == pygame.K_SEMICOLON:
                objectsAtPlayer = mapAtCoords(PLAYER.x, PLAYER.y)

                for obj in objectsAtPlayer:
                    if obj.stairs:
                        obj.stairs.use()
                    if obj.exitPortal:
                        obj.exitPortal.use()

            # menu keys
            if event.key == pygame.K_TAB:
                menu_pause()
            # key 'c' -> "cast"
            if event.key == pygame.K_c:
                playerAction = menu_magic()
                return playerAction

    return 'no action'

def gameMessage(gameMsg, msgColor=constants.COLOR_GREY):
    GAME.msgHistory.append((gameMsg, msgColor))

def gameLoop():

    global GAME_LOOP_ITER, IS_DROPPING, CURRENT_DUNGEON_LEVEL

    # now for the game loop, each iteration of which is a turn. If we were real-time, it would be a frame
    gameQuit = False

    # 'no action' means we are afk
    playerAction = 'no action'


    # the Game Loop
    while not gameQuit:

        # increment the number of loops
        GAME_LOOP_ITER += 1

        # what dungeon level we are on
        CURRENT_DUNGEON_LEVEL = len(GAME.previousMaps) + 1

        # the loop constantly listens for key strokes
        playerAction = gameHandleKeys()

        mapCalcFOV()

        # Update our display to reflect what has changed
        drawGame()

        # tick the clock
        CLOCK.tick(constants.GAME_FPS)

        # if we 'x-out' the window, quit
        if playerAction == 'QUIT':
            gameSave(True)
            gameQuit = True

        # if we have taken our turn (NOT do nothing), everything else takes it's turn
        for obj in GAME.currentObj:
            if playerAction != 'no action':
                if obj.ai:
                    obj.ai.takeTurn()
                if obj.creature:
                    if obj.creature.scent:
                        obj.creature.scent.trail()
                if obj.scentStrength:
                    obj.decay()
            if obj.exitPortal:
                obj.exitPortal.update()


        if PLAYER.state == 'STATUS_DEAD' or PLAYER.state == 'STATUS_VICTORY':
            gameQuit = True

        if playerAction != 'no action' and IS_DROPPING:
            IS_DROPPING = False

    pygame.mixer.music.load(ASSETS.musicMain)
    pygame.mixer.music.play(-1)



if __name__ == '__main__':
    menu_main()
