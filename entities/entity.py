import pygame
from constants import StatsName, CollisionName
from support_functions.support_functions import SupportFunctions
import abc
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group):
        super().__init__(groups)
        self.frame_index = 0
        self.direction = pygame.math.Vector2()
        self.animations = {}
    def move(self, delta_time: float):
        # default the vector so diagonal is the same
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal
        self.position.x += self.direction.x * self.current_stats[StatsName.SPEED.value] * delta_time
        self.hitbox.x = self.position.x
        self.collision(CollisionName.HORIZONTAL.value)

        # vertical
        self.position.y += self.direction.y * self.current_stats[StatsName.SPEED.value] * delta_time
        self.hitbox.y = self.position.y
        self.collision(CollisionName.VERTICAL.value)

        self.rect.center = self.hitbox.center

    def collision(self, direction: str):
        if direction == CollisionName.HORIZONTAL.value:
            for sprite in self.game_obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # check right
                    # move the overlap to the left side of the sprite
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # check left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.position.x = self.hitbox.x

        if direction == CollisionName.VERTICAL.value:
            for sprite in self.game_obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # check down
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # check up
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.position.y = self.hitbox.y

    @ abc.abstractmethod
    def animate_entity(self):
        return

    def import_graphics(self, general_path):
        for animation_key in self.animations.keys():
            animation_path = general_path + "/" + animation_key
            self.animations[animation_key] = SupportFunctions.import_entity_folder(animation_path, (64, 64))