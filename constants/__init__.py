from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 595 

INVEN_ITEM_BASE_X = 75 
INVEN_ITEM_BASE_Y = 75

# SQUARE_DISTANCE = GAME_WIDTH // 17

class ItemName(Enum):
    BEER = 'beer'
    WATER = 'water'

class Scaling(Enum):
    PLAYER_WIDTH = 24
    PLAYER_HEIGHT = 40
    ITEM_WIDTH = 32
    ITEM_HEIGHT = 32

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class CharacterInfo(Enum):
    HEALTH = 'health'
    STAMINA = 'stamina'
    DEFENSE = 'defense'
    ATTACK = 'attack' 

class GameLayerKeys(Enum):
    GROUND = 'ground'
    PLANT = 'plant'
    MAIN = 'main'

GAME_LAYERS = {
    GameLayerKeys.GROUND.value: 1,
    GameLayerKeys.PLANT.value: 6,
    GameLayerKeys.MAIN.value: 7,
}