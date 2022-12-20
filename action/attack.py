import pygame
from enum import Enum
from constants import TILE_SIZE
class Direction(Enum):
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'
    LEFT = 'left'

class Attack:

    def __init__(self, animations):
        self.animations = animations

    def basic_attack(self, entity, groups):
        direction = entity.movement_status.split("_")[0]
        attack_direction = None
        if direction == Direction.RIGHT.value:
            attack_direction = pygame.math.Vector2(1, 0)
        elif direction == Direction.LEFT.value:
            attack_direction = pygame.math.Vector2(-1, 0)
        elif direction == Direction.DOWN.value:
            attack_direction = pygame.math.Vector2(0, 1)
        elif direction == Direction.UP.value:
            attack_direction = pygame.math.Vector2(0, -1)

        if attack_direction.x:
            offset_x = attack_direction.x * TILE_SIZE // 2
            x = entity.hitbox.centerx + offset_x
            y = entity.hitbox.centery
        else:
            offset_y = attack_direction.y * TILE_SIZE // 2
            x = entity.hitbox.centerx
            y = entity.hitbox.centery + offset_y
        attack = entity.image.get_rect(topleft=(x, y))
        self.animations.create_attack_animation('slash', (attack.x, attack.y), groups)
        entity.attack(attack)
