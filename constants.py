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
# Color Definitions
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHT_GREY = (175, 175, 175)
COLOR_GREY = (100, 100, 100)
COLOR_DARK_GREY = (25, 25, 25)
COLOR_WHITE = (255, 255, 255)
COLOR_PINK = (255, 100, 147)
COLOR_RED = (255, 0, 0)
COLOR_ORANGE = (255, 165, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_BLUE = (0, 0, 255)
COLOR_DARK_BLUE = pygame.Color(0, 0, 128, 255)
COLOR_PURPLE = (128, 0, 128)


PATH = "/Users/garyanderson/Desktop/Education/Computer Science/Roguelike tutorial/Project/repos/roguelike/first/"

# Game colors
COLOR_DEFAULT_BG = COLOR_BLACK
COLOR_MAP_FOG = COLOR_BLACK
COLOR_MENU = COLOR_DARK_GREY

# FONTS ##
FONT_DEBUG_MESSAGE = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', 10)
FONT_MESSAGE_TEXT = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', 12)
FONT_CURSOR_TEXT = pygame.font.Font(PATH + 'data/joystixMonospace.ttf', CELL_HEIGHT)
FONT_TITLE_TEXT = pygame.font.Font(PATH + 'data/AGoblinAppears.otf', 24)
FONT_INV_TITLE = pygame.font.Font(PATH + 'data/AGoblinAppears.otf', 18)

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
