from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 595

INVEN_ITEM_BASE_X = 75 
INVEN_ITEM_BASE_Y = 75
TILE_SIZE = 64
weapon_images_path = 'graphics/character/weapons'
# SQUARE_DISTANCE = GAME_WIDTH // 17


class PlayerWeapons(Enum):
    SWORD = 'sword'
    SPEAR = "spear"
    SAI = "sai"
    AXE = "axe"


class ItemName(Enum):
    BEER = 'beer'
    WATER = 'water'


class Font(Enum):
    ARIAL = 'Arial'


class FontSize(Enum):
    size_18 = 18


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_RED = (84, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    ORANGE = (252, 163, 0)
    GREY = (168, 168, 168)
    GOLD = "gold"


class CharacterInfo(Enum):
    HEALTH = 'health'
    MANA = 'mana'
    DEFENSE = 'defense'
    ATTACK = 'attack' 


class CollisionName(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'