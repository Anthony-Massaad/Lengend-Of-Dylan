import pygame
from enum import Enum

from constants import  entity_data, SpriteType, FilePath
from entities.entity import Entity
from logger.log import Log

class Movement(Enum):
    IDLE = 'idle'
    ATTACK = 'attack'
    MOVE = 'move'

class Enemy(Entity):

    def __init__(self, sprite_name, pos, groups: pygame.sprite.Group, obstacle_sprites):
        super().__init__(groups, obstacle_sprites, pos, Movement, FilePath.monsters.value + "/" + sprite_name, sprite_name)


    def animate_entity(self):
        pass

    def update(self, delta_time: float):
        self.move(delta_time)

