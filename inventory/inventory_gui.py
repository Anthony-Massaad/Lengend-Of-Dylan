from turtle import width
import pygame
from inventory.inventory import Inventory
from constants import GAME_WIDTH, GAME_HEIGHT, Color, Scaling, INVEN_ITEM_BASE_X, INVEN_ITEM_BASE_Y, CharacterInfo

class InventoryImpl:
    INVENTORY_WINDOW_DIFF = 100
    INVENTORY_WINDOW_WIDTH = INVENTORY_WINDOW_HEIGHT = GAME_WIDTH - INVENTORY_WINDOW_DIFF 

    @classmethod
    def get_item_pos(cls, col, row, line_width):
        col += 1
        if (col * INVEN_ITEM_BASE_X) + Scaling.ITEM_WIDTH.value >= line_width:
            row += 1
            col = 1

        return (INVEN_ITEM_BASE_X + 7) * col, INVEN_ITEM_BASE_Y * row, col, row

    @classmethod
    def render_item_info(cls, item_info, rect, font):
        text = font.render(item_info, True, Color.BLACK.value)
        text_rect = text.get_rect()
        text_rect.center = rect.center
        return text, text_rect

    @classmethod
    def display_item_info(cls, screen, item, mouse_x, mouse_y):
        rect = pygame.Rect(mouse_x, mouse_y, 200, 100)
        pygame.draw.rect(screen, Color.GREY.value, rect)
        font = pygame.font.SysFont('Arial', 20)

        health_value = item.get_ability_attr(CharacterInfo.HEALTH.value)
        defense_value = item.get_ability_attr(CharacterInfo.DEFENSE.value)
        stamina_value = item.get_ability_attr(CharacterInfo.STAMINA.value)
        attack_value = item.get_ability_attr(CharacterInfo.ATTACK.value)

        name, name_rect = cls.render_item_info(item.name, rect, font)
        health, health_rect = cls.render_item_info(f'{CharacterInfo.HEALTH.value}: {health_value}', rect, font)

        screen.blit(name, name_rect)
        screen.blit(health, health_rect)

    @classmethod
    def display_inventory(cls, screen, inventory: Inventory, delta_time):
        cls.inventory_triggered = True
        # TEMP, HAVE IT ALREADY DRAWN IN THE INVENTORY IMAGE THAT IS GOING TO BE DESIGNED
        # This is just general deisgn, add more styles to it. Border..etc
        pygame.draw.rect(screen, Color.WHITE.value, pygame.Rect(50,50, cls.INVENTORY_WINDOW_WIDTH, cls.INVENTORY_WINDOW_HEIGHT), 0, 2, 2, 2)
        line_width = cls.INVENTORY_WINDOW_WIDTH - cls.INVENTORY_WINDOW_DIFF
        pygame.draw.line(screen, Color.BLACK.value,
                        (line_width, cls.INVENTORY_WINDOW_DIFF//2), 
                        (line_width, cls.INVENTORY_WINDOW_HEIGHT + cls.INVENTORY_WINDOW_DIFF), 3)
        
        pygame.draw.line(screen, Color.BLACK.value, 
                        (line_width, cls.INVENTORY_WINDOW_DIFF*2), 
                        (cls.INVENTORY_WINDOW_WIDTH + cls.INVENTORY_WINDOW_DIFF // 2, cls.INVENTORY_WINDOW_DIFF*2), 3)

        inventory_keys = inventory.get_keys()
        # Draw the items
        col, row = 0, 1
        for item in inventory_keys:
            item_x, item_y, col, row = cls.get_item_pos(col, row, line_width)
            item.draw_item(screen, delta_time, item_x, item_y)
            # print(f"name: {keys.name} ability: {keys.ability}  description: {keys.description} image: {keys.image}")

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for item in inventory_keys:
            if item.check_hover(mouse_x, mouse_y):
                cls.display_item_info(screen, item, mouse_x, mouse_y)
        


class InventoryGUI:
    inventory_triggered = False

    @classmethod
    def display_inventory(cls, screen, inventory: Inventory, delta_time):
        InventoryImpl.display_inventory(screen, inventory, delta_time)

