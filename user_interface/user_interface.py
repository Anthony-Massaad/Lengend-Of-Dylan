from enum import Enum

import pygame

from constants import StatsName, Font, FontSize, Color, GAME_WIDTH, GAME_HEIGHT, weapon_images_path, PlayerWeapons, magic_path, PlayerMagics, PlayerUtilNames


class UISettings(Enum):
    BAR_HEIGHT = 15
    HEALTH_WIDTH = 200

    ENEMY_HEALTH_WIDTH = 50
    ENEMY_BAR_HEIGHT = 5

    MANA_WIDTH = 180
    SELECTION_BOX_SIZE = 80
    UI_BACKGROUND_COLOR = (34, 34, 34)
    UI_BORDER_COLOR = (17, 17, 17)
    HEALTH_BAR_Y = 10
    UTIL_BOX_SIZE = 80


class UserInterface:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        # change to pygame.font.Font when finding font
        self.font = pygame.font.SysFont(Font.ARIAL.value, FontSize.size_18.value)

        # player bars
        self.health_bar = pygame.Rect(10, UISettings.HEALTH_BAR_Y.value, UISettings.HEALTH_WIDTH.value,
                                      UISettings.BAR_HEIGHT.value)
        self.mana_bar = pygame.Rect(10, UISettings.HEALTH_BAR_Y.value + UISettings.BAR_HEIGHT.value + 1,
                                    UISettings.MANA_WIDTH.value, UISettings.BAR_HEIGHT.value)

        # graphics for the player weapons
        self.weapon_images = []
        for weapon_name in PlayerWeapons:
            full_path = f"{weapon_images_path}/{weapon_name.value}.png"
            self.weapon_images.append(pygame.image.load(full_path).convert_alpha())

        # gaphics for player magics
        self.magic_images = []
        for magic_name in PlayerMagics:
            full_path = f"{magic_path}/{magic_name.value}/{magic_name.value}.png"
            self.magic_images.append(pygame.image.load(full_path).convert_alpha())

    def draw_bar(self, current_value, max_value, rect, color, is_health_bar, is_player):
        # Drawing background of the bar Might delete
        pygame.draw.rect(self.screen, UISettings.UI_BACKGROUND_COLOR.value, rect)

        # converting the values to pixel relative to the width of the bar
        value_ratio = current_value / max_value
        rect_width = rect.width * value_ratio
        bar_rect = rect.copy()
        bar_rect.width = rect_width

        # changing the color relative to the stats of the bar for health
        if is_health_bar:
            health_percentage = value_ratio * 100
            color = Color.GREEN.value if health_percentage > 75 else Color.ORANGE.value if health_percentage >= 45 else Color.RED.value if health_percentage >= 20 else Color.DARK_RED.value

        # drawing the bar
        pygame.draw.rect(self.screen, color, bar_rect)
        # drawing the border
        border_width = 3 if is_player else 1
        pygame.draw.rect(self.screen, UISettings.UI_BORDER_COLOR.value, rect, border_width)

    def draw_utils_rect(self, x, y, is_switching_utils):
        rect = pygame.Rect(x, y, UISettings.UTIL_BOX_SIZE.value, UISettings.UTIL_BOX_SIZE.value)
        # Background
        pygame.draw.rect(self.screen, UISettings.UI_BACKGROUND_COLOR.value, rect, 0, UISettings.UTIL_BOX_SIZE.value)
        # Border
        border_color = Color.GOLD.value if is_switching_utils else UISettings.UI_BORDER_COLOR.value
        pygame.draw.rect(self.screen, border_color, rect, 3, UISettings.UTIL_BOX_SIZE.value)
        return rect

    def weapon_ui(self, weapon_index, is_switching_utils):
        rect = self.draw_utils_rect(10, GAME_HEIGHT - 90, is_switching_utils)
        weapon_image = self.weapon_images[weapon_index]
        self.screen.blit(weapon_image, weapon_image.get_rect(center=rect.center))

    def magic_ui(self, magic_index, is_switching_utils):
        rect = self.draw_utils_rect(75, GAME_HEIGHT - 90, is_switching_utils)
        magic_image = self.magic_images[magic_index]
        self.screen.blit(magic_image, magic_image.get_rect(center=rect.center))

    def draw(self, player, enemies):
        for enemy in enemies:
            # Health bar offset is respective to the player
            health_bar_offset_x = enemy.rect.topleft[0] - (player.rect.centerx - (GAME_WIDTH // 2)) + 7
            health_bar_offset_y = enemy.rect.topleft[1] - (player.rect.centery - (GAME_WIDTH // 2)) - 5
            self.draw_bar(enemy.current_stats[StatsName.HEALTH.value], enemy.current_stats[StatsName.MAX_HEALTH.value],
                          pygame.Rect(health_bar_offset_x, health_bar_offset_y, UISettings.ENEMY_HEALTH_WIDTH.value,
                                      UISettings.ENEMY_BAR_HEIGHT.value), Color.GREEN.value, True, False)

        self.draw_bar(player.current_stats[StatsName.HEALTH.value], player.max_stats[StatsName.HEALTH.value],
                      self.health_bar, Color.GREEN.value, True, True)
        self.draw_bar(player.current_stats[StatsName.MANA.value], player.max_stats[StatsName.MANA.value],
                      self.mana_bar, Color.BLUE.value, False, True)

        if player.last_util_switch == PlayerUtilNames.MAGIC:
            self.weapon_ui(player.weapon_index, player.weapon_switch_timer.active)
            self.magic_ui(player.magic_index, player.magic_switch_timer.active)
        elif player.last_util_switch == PlayerUtilNames.WEAPON:
            self.magic_ui(player.magic_index, player.magic_switch_timer.active)
            self.weapon_ui(player.weapon_index, player.weapon_switch_timer.active)


