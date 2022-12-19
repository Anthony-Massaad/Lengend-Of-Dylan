import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, StatsName
from particles.particle import Particle
from entities.enemy.enemy import Enemy

class GameDebugger:

    @classmethod
    def get_offset(cls, sprite, player, topleft=True):
        if topleft:
            return sprite.hitbox.topleft[0] - (player.hitbox.centerx - (GAME_WIDTH // 2)), sprite.hitbox.topleft[1] - (player.hitbox.centery - (GAME_HEIGHT // 2))
        return sprite.hitbox.centerx - (player.hitbox.centerx - (GAME_WIDTH // 2)), sprite.hitbox.centery - (player.hitbox.centery - (GAME_HEIGHT // 2))

    @classmethod
    def hitbox_debug(cls, visible_sprites, obstacle_sprite, player):

        for sprite in visible_sprites:
            if isinstance(sprite, Particle):
                continue
            offset_x, offset_y = cls.get_offset(sprite, player)
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)

            if isinstance(sprite, Enemy):
                offset_x, offset_y = cls.get_offset(sprite, player, False)
                pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), (offset_x, offset_y), sprite.current_stats[StatsName.ATTACK_RADIUS.value], 2)
                pygame.draw.circle(pygame.display.get_surface(), (0, 0, 255), (offset_x, offset_y), sprite.current_stats[StatsName.NOTICE_RADIUS.value], 2)

        for sprite in obstacle_sprite:
            offset_x, offset_y = cls.get_offset(sprite, player)
            pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)
