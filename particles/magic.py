import pygame
from random import randint
from particles.particle import Animation
from constants import StatsName
from enum import Enum

class Direction(Enum):
    RIGHT = 'right'
    DOWN = 'down'
    UP = 'up'
    LEFT = 'left'


class Magic:

    def __init__(self, animation_player):
        self.animation_player = animation_player

    def reduce_mana(self, player, cost):
        player.current_stats[StatsName.MANA.value] -= cost
        if player.current_stats[StatsName.MANA.value] > player.max_stats[StatsName.MANA.value]:
            player.current_stats[StatsName.MANA.value] = player.max_stats[StatsName.MANA.value]

    def heal(self, player, strength, current_mana, cost, groups):
        if current_mana >= cost:
            player.current_stats[StatsName.HEALTH.value] += strength
            if player.current_stats[StatsName.HEALTH.value] > player.max_stats[StatsName.HEALTH.value]:
                player.current_stats[StatsName.HEALTH.value] = player.max_stats[StatsName.HEALTH.value]

            self.reduce_mana(player, cost)

            self.animation_player.create_particle('aura', player.rect.center, groups)
            self.animation_player.create_particle('heal', player.rect.center, groups)
    
    def flame_attack(self, player, strength, current_mana, cost, groups):
        if current_mana >= cost:
            self.reduce_mana(player, cost)
            direction = player.movement_status.split('_')[0]

            for i in range(5):
                attack = None
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
                    offset_x = (attack_direction.x * (i+1)) * 64
                    x = player.rect.centerx + offset_x + randint(-64//3, 64//3)
                    y = player.rect.centery  + randint(-64//3, 64//3)
                    attack =  player.image.get_rect(topleft=(x, y))
                    self.animation_player.create_particle("flame", (x,y), groups)
                else:
                    offset_y = (attack_direction.y * (i+1)) * 64
                    x = player.rect.centerx + randint(-64//3, 64//3)
                    y = player.rect.centery + offset_y  + randint(-64//3, 64//3)
                    attack =  player.image.get_rect(topleft=(x, y))
                    self.animation_player.create_particle("flame", (x,y), groups)
                attack = attack.inflate(-32, -32)
                player.hit_spell(attack, strength)
