import pygame

from constants import GAME_WIDTH, GAME_HEIGHT, StatsName

class GameDebugger:
    draw_enemy_radius = False
    draw_obstacles = True
    draw_enemy_hitbox = True
    draw_player_hitbox = True
    draw_particle_hitbox = True

    @classmethod
    def get_offset(cls, sprite, player, topleft=True):
        if topleft:
            return sprite.hitbox.topleft[0] - (player.hitbox.centerx - (GAME_WIDTH // 2)), sprite.hitbox.topleft[1] - (player.hitbox.centery - (GAME_HEIGHT // 2))
        return sprite.hitbox.centerx - (player.hitbox.centerx - (GAME_WIDTH // 2)), sprite.hitbox.centery - (player.hitbox.centery - (GAME_HEIGHT // 2))

    @classmethod
    def hitbox_debug(cls, visible_sprites, obstacle_sprite, player):

        for sprite in visible_sprites:
            if (sprite.sprite_type == "particle" or sprite.sprite_type == "attack_signature") and cls.draw_particle_hitbox:
                x, y = cls.get_offset(sprite, player)
                pygame.draw.rect(pygame.display.get_surface(), (0, 255, 255), pygame.Rect(x, y, sprite.hitbox.width, sprite.hitbox.height), 2)

            if (sprite.sprite_type == "enemy" and cls.draw_enemy_hitbox) or (sprite.sprite_type == "player" and cls.draw_player_hitbox):
                offset_x, offset_y  = cls.get_offset(sprite, player)
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)

            if cls.draw_enemy_radius:
                if sprite.sprite_type == "enemy":
                    offset_x, offset_y = cls.get_offset(sprite, player, False)
                    pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), (offset_x, offset_y), sprite.current_stats[StatsName.ATTACK_RADIUS.value], 2)
                    pygame.draw.circle(pygame.display.get_surface(), (0, 0, 255), (offset_x, offset_y), sprite.current_stats[StatsName.NOTICE_RADIUS.value], 2)

        if cls.draw_obstacles:
            for sprite in obstacle_sprite:
                offset_x, offset_y = cls.get_offset(sprite, player)
                pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), pygame.Rect(offset_x, offset_y, sprite.hitbox.width, sprite.hitbox.height), 2)

    @classmethod
    def draw_attack_hitbox(cls, attack, player_hitbox):
        ...