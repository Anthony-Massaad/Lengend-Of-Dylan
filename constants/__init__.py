from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 595

INVEN_ITEM_BASE_X = 75 
INVEN_ITEM_BASE_Y = 75
TILE_SIZE = 64

# SQUARE_DISTANCE = GAME_WIDTH // 17

class ItemName(Enum):
    BEER = 'beer'
    WATER = 'water'

class Font(Enum):
    ARIAL = 'Arial'

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREY = (168, 168, 168)

class CharacterInfo(Enum):
    HEALTH = 'health'
    STAMINA = 'stamina'
    DEFENSE = 'defense'
    ATTACK = 'attack' 

class CollisionName(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'