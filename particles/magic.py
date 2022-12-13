import pygame
from random import randint
from particles.particle import Animation
from constants import StatsName

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
