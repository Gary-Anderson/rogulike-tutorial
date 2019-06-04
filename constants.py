# Globals
import pygame
import tcod as libtcod

pygame.init()

# Game Sizes
CAMERA_WIDTH = 800
CAMERA_HEIGHT = 500
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
LIMIT_FPS = 20
CELL_WIDTH = 32
CELL_HEIGHT = 32

# FPS limit
GAME_FPS = 60

# Map vars
MAP_WIDTH = 20
MAP_HEIGHT = 20
MAP_MAX_ROOMS = 20
MAP_NUM_LEVELS = 5

#Rooms
ROOM_MAX_HEIGHT = 7
ROOM_MIN_HEIGHT = 3
ROOM_MAX_WIDTH = 5
ROOM_MIN_WIDTH = 2
# Color Definitions pygame.Color(red, blue, green, opacity)
COLOR_BLACK =       pygame.Color(  0,   0,   0, 255)
COLOR_LIGHT_GREY =  pygame.Color(175, 175, 175, 255)
COLOR_GREY =        pygame.Color(100, 100, 100, 255)
COLOR_DARK_GREY =   pygame.Color( 25,  25,  25, 255)
COLOR_WHITE =       pygame.Color(255, 255, 255, 255)
COLOR_PINK =        pygame.Color(255, 100, 147, 255)
COLOR_RED =         pygame.Color(255,   0,   0, 255)
COLOR_DARK_RED =    pygame.Color(128,   0,   0, 255)
COLOR_ORANGE =      pygame.Color(255, 165,   0, 255)
COLOR_YELLOW =      pygame.Color(255, 255,   0, 255)
COLOR_LIGHT_GREEN = pygame.Color(128, 255, 128, 255)
COLOR_GREEN =       pygame.Color(  0, 255,   0, 255)
COLOR_DARK_GREEN =  pygame.Color( 50, 100,  50, 255)
COLOR_CYAN =        pygame.Color(  0, 255, 255, 255)
COLOR_BLUE =        pygame.Color(  0,   0, 255, 255)
COLOR_LIGHT_BLUE =  pygame.Color(100, 100, 255, 255)
COLOR_DARK_BLUE =   pygame.Color(  0,   0, 128, 255)
COLOR_PURPLE =      pygame.Color(128,   0, 128, 255)


PATH = "/Users/garyanderson/Desktop/Education/Computer Science/Roguelike tutorial/Project/repos/roguelike/first/"

# Game colors
COLOR_DEFAULT_BG = COLOR_BLACK
COLOR_MAP_FOG = COLOR_BLACK
COLOR_MENU = COLOR_DARK_GREY
COLOR_FRAME = COLOR_BLACK
COLOR_BUTTON = COLOR_BLUE
COLOR_BUTTON_MOUSEOVER = COLOR_RED
COLOR_BUTTON_TEXT = COLOR_WHITE
COLOR_BUTTON_TEXT_MOUSEOVER = COLOR_WHITE
COLOR_SWITCH = COLOR_DARK_RED
COLOR_DROPPING_TEXT = COLOR_WHITE
COLOR_DROPPING_HIGHLIGHT = COLOR_DARK_RED
COLOR_EQUIPPED = COLOR_GREEN
COLOR_BORDER1 = COLOR_WHITE
COLOR_BORDER2 = COLOR_BLACK


# FONTS ##
FONT_DEBUG_MESSAGE = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', 10)
FONT_MESSAGE_TEXT = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', 12)
FONT_CURSOR_TEXT = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', CELL_HEIGHT)
FONT_TITLE_TEXT = pygame.font.Font(PATH + 'data/AGoblinAppears.otf', 24)
FONT_INV_TITLE = pygame.font.Font(PATH + 'data/AGoblinAppears.otf', 18)
FONT_INV_INFO = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', 10)

# FOV SETTINGS
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 7

#DEPTH
DEPTH_PLAYER = -100
DEPTH_DECOR = 101
DEPTH_CORPSE = 100
DEPTH_CREATURE = 0
DEPTH_ITEM = 10

# Message Defaults
NUM_MESSAGES = 12
