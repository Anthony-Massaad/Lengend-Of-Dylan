import pygame

from constants import StatsName, CollisionName, entity_data, FilePath
from support_functions.support_functions import SupportFunctions
from logger.log import Log
from timer.timer import Timer

import abc


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.Group, visible_sprites, obstacle_sprites, attackable_sprites, pos, movement, folder_path, sprite_name, particle_animations):
        super().__init__(groups)
        self.current_stats = entity_data[sprite_name]
        self.sprite_name = sprite_name
        Log.debug(f"{sprite_name} stats dictionary is {self.current_stats}")
        self.frame_index = 0

        # import animation for relative sprite
        self.animations = {}
        for movement_name in movement:
            self.animations[movement_name.value] = []
        Log.debug(f"{sprite_name} Animations dictionary is {self.animations}")
        self.import_graphics(folder_path)

        # set default status for enemy or player
        if sprite_name == "player":
            self.movement_status = movement.DOWN_IDLE.value
        else:
            self.movement_status = movement.IDLE.value

        # graphic_setup
        self.image = self.animations[self.movement_status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)

        self.position = pygame.math.Vector2(self.rect.topleft)
        self.game_obstacle_sprites = obstacle_sprites
        self.attackable_sprites = attackable_sprites
        self.visible_sprites = visible_sprites
        self.direction = pygame.math.Vector2()

        self.is_attacking = False
        self.attack_cooldown = Timer(self.current_stats[StatsName.ATTACK_COOLDOWN.value])
        self.particle_animations = particle_animations


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

    @abc.abstractmethod
    def animate_entity(self, delta_time: float):
        return

    @abc.abstractmethod
    def update(self, delta_time: float):
        return

    @abc.abstractmethod
    def update_timers(self):
        return

    @abc.abstractmethod
    def attack(self):
        return

    def is_attacked(self, entity_attack):
        self.current_stats[StatsName.HEALTH.value] -= entity_attack
        if self.current_stats[StatsName.HEALTH.value] <= 0:
            if self.sprite_name != "player":
                self.particle_animations.create_particle(self.sprite_name, self.rect.center, [self.visible_sprites])
                self.kill()

    def import_graphics(self, general_path):
        for animation_key in self.animations.keys():
            animation_path = general_path + "/" + animation_key
            self.animations[animation_key] = SupportFunctions.import_entity_folder(animation_path, (64, 64))
