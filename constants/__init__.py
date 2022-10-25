from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 595 

# SQUARE_DISTANCE = GAME_WIDTH // 17

class Scaling(Enum):
    PLAYER_WIDTH = 24
    PLAYER_HEIGHT = 40

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

class CharacterInfo(Enum):
    HEALTH = 'health'
    STAMINA = 'stamina'
    DEFENSE = 'defense'
    ATTACK = 'attack' 