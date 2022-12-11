import pygame
from enum import Enum

from constants import  enemy_data, SpriteType, FilePath
from entities.entity import Entity
from logger.log import Log

class Movement(Enum):
    IDLE = 'idle'
    ATTACK = 'attack'
    MOVE = 'move'

class Enemy(Entity):

    def __init__(self, monster_name, pos, groups: pygame.sprite.Group, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = SpriteType.ENEMY
        self.current_stats = enemy_data[monster_name]

        for movement in Movement:
            self.animations[movement.value] = []
        Log.debug(f"{monster_name} Animations dictionary is {self.animations}")
        self.import_graphics(FilePath.monsters.value + "/" + monster_name)

        self.movement_status = Movement.IDLE.value
        # graphic_setup
        self.image = self.animations[self.movement_status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.game_obstacle_sprites = obstacle_sprites

    def animate_entity(self):
        pass

    def update(self, delta_time: float):
        self.move(delta_time)

