import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, StatsName
from particles.particle import Particle
from entities.enemy.enemy import Enemy
from entities.player.player import Player

class GameDebugger:
    draw_enemy_radius = True
    draw_obstacles = True
    draw_enemy_hitbox = True
    draw_player_hitbox = True

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

            if (isinstance(sprite, Enemy) and cls.draw_enemy_hitbox) or (isinstance(sprite, Player) and cls.draw_player_hitbox):
                offset_x, offset_y = cls.get_offset(sprite, player)
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)

            if cls.draw_enemy_radius:
                if isinstance(sprite, Enemy):
                    offset_x, offset_y = cls.get_offset(sprite, player, False)
                    pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), (offset_x, offset_y), sprite.current_stats[StatsName.ATTACK_RADIUS.value], 2)
                    pygame.draw.circle(pygame.display.get_surface(), (0, 0, 255), (offset_x, offset_y), sprite.current_stats[StatsName.NOTICE_RADIUS.value], 2)

        if cls.draw_obstacles:
            for sprite in obstacle_sprite:
                offset_x, offset_y = cls.get_offset(sprite, player)
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)
