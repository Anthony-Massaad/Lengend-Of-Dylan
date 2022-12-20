import pygame
from enum import Enum

from constants import FilePath, StatsName
from entities.entity import Entity


class Movement(Enum):
    IDLE = 'idle'
    ATTACK = 'attack'
    MOVE = 'move'


class Enemy(Entity):

    def __init__(self, sprite_name, pos, groups: pygame.sprite.Group, visible_sprites, obstacle_sprites, attackable_sprites: pygame.sprite.Group, particle_animations, attack_sig_animations):
        super().__init__(groups, visible_sprites, obstacle_sprites, attackable_sprites, pos, Movement, FilePath.monsters.value + "/" + sprite_name, sprite_name, particle_animations, attack_sig_animations)
        self.sprite_type = "enemy"

    def update_timers(self):
        self.attack_cooldown.cooldown()

    def animate_entity(self, delta_time: float):
        self.frame_index += 4 * delta_time
        if self.frame_index >= len(self.animations[self.movement_status]):
            if self.is_attacking:
                self.attack()
                self.is_attacking = False
                self.attack_cooldown.start_timer()
            self.frame_index = 0
        self.image = self.animations[self.movement_status][int(self.frame_index)]

    def status(self, player):

        if self.movement_status == Movement.ATTACK.value and not self.attack_cooldown.active:
            self.is_attacking = True
            self.direction = pygame.math.Vector2()
        elif self.movement_status == Movement.MOVE.value:
            self.direction = self.get_direction_to_player(player)
        else:
            self.movement_status = Movement.MOVE.value
            self.direction = pygame.math.Vector2()

    def get_distance_to_player(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        return (player_vec - enemy_vector).magnitude()  # Convert vector to distance

    def get_direction_to_player(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)

        distance = self.get_distance_to_player(player)
        # direction is 0,0 by default unless movement is needed
        direction = pygame.math.Vector2()
        if distance > 0:
            # converts vector to 1 or -1 depending on the direction of the vector
            direction = (player_vec - enemy_vector).normalize()

        return direction

    def update_movement_status(self, player):
        distance_to_player = self.get_distance_to_player(player)

        if distance_to_player <= self.current_stats[StatsName.ATTACK_RADIUS.value] and not self.attack_cooldown.active:
            self.movement_status = Movement.ATTACK.value
        elif distance_to_player <= self.current_stats[StatsName.NOTICE_RADIUS.value] and not self.attack_cooldown.active:
            self.movement_status = Movement.MOVE.value
        else:
            self.movement_status = Movement.IDLE.value

    def attack(self):
        for attackable_sprite in self.attackable_sprites:
            attackable_sprite.is_attacked(self.current_stats[StatsName.ATTACK.value])
            self.particle_animations.create_particle(self.current_stats[StatsName.ATTACK_TYPE.value],
                                                     attackable_sprite.rect.center, [self.visible_sprites])

    def update(self, delta_time: float):
        self.move(delta_time)
        self.animate_entity(delta_time)
        self.update_timers()

    def enemy_update(self, player):
        self.update_movement_status(player)
        self.status(player)

