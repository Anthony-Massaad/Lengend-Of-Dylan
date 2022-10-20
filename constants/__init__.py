from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 595 

SQUARE_DISTANCE = GAME_WIDTH // 17

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)