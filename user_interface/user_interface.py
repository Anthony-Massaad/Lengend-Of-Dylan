import pygame
from constants import CharacterInfo, Font, FontSize, Color
from enum import Enum


class UISettings(Enum):
    BAR_HEIGHT = 15
    HEALTH_WIDTH = 200
    MANA_WIDTH = 180
    SELECTION_BOX_SIZE = 80
    UI_BACKGROUND_COLOR = (34, 34, 34)
    UI_BORDER_COLOR = (17, 17, 17)
    HEALTH_BAR_Y = 10


class UserInterface:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        # change to pygame.font.Font when finding font
        self.font = pygame.font.SysFont(Font.ARIAL.value, FontSize.size_18.value)

        # bars
        self.health_bar = pygame.Rect(10, UISettings.HEALTH_BAR_Y.value, UISettings.HEALTH_WIDTH.value, UISettings.BAR_HEIGHT.value)
        self.mana_bar = pygame.Rect(10, UISettings.HEALTH_BAR_Y.value + UISettings.BAR_HEIGHT.value + 1, UISettings.MANA_WIDTH.value, UISettings.BAR_HEIGHT.value)

    def draw_bar(self, current_value, max_value, rect, color, is_health_bar):
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
        pygame.draw.rect(self.screen, UISettings.UI_BORDER_COLOR.value, rect, 3)

    def draw(self, player):
        self.draw_bar(player.current_stats[CharacterInfo.HEALTH.value], player.max_stats[CharacterInfo.HEALTH.value], self.health_bar, Color.GREEN.value, True)
        self.draw_bar(player.current_stats[CharacterInfo.MANA.value], player.max_stats[CharacterInfo.MANA.value], self.mana_bar, Color.BLUE.value, False)
        # pygame.draw.rect(self.screen, Color.RED.value, self.health_bar)
        # pygame.draw.rect(self.screen, Color.BLUE.value, self.mana_bar)