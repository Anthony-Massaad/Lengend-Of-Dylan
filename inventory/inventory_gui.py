import pygame

from constants import GAME_WIDTH, Color, INVEN_ITEM_BASE_X, INVEN_ITEM_BASE_Y
from inventory.inventory import Inventory


class InventoryImpl:
    INVENTORY_WINDOW_DIFF = 100
    INVENTORY_WINDOW_WIDTH = INVENTORY_WINDOW_HEIGHT = GAME_WIDTH - INVENTORY_WINDOW_DIFF

    @classmethod
    def get_item_pos(cls, col, row, line_width):
        col += 1
        if (col * INVEN_ITEM_BASE_X) + 32 >= line_width:
            row += 1
            col = 1

        return (INVEN_ITEM_BASE_X + 7) * col, INVEN_ITEM_BASE_Y * row, col, row

    @classmethod
    def display_inventory(cls, screen, inventory: Inventory, delta_time):
        cls.inventory_triggered = True

        # TEMP, HAVE IT ALREADY DRAWN IN THE INVENTORY IMAGE THAT IS GOING TO BE DESIGNED
        # This is just general deisgn, add more styles to it. Border..etc
        pygame.draw.rect(screen, Color.WHITE.value,
                         pygame.Rect(50, 50, cls.INVENTORY_WINDOW_WIDTH, cls.INVENTORY_WINDOW_HEIGHT), 0, 2, 2, 2)
        line_width = cls.INVENTORY_WINDOW_WIDTH - cls.INVENTORY_WINDOW_DIFF
        pygame.draw.line(screen, Color.BLACK.value,
                         (line_width, cls.INVENTORY_WINDOW_DIFF // 2),
                         (line_width, cls.INVENTORY_WINDOW_HEIGHT + cls.INVENTORY_WINDOW_DIFF), 3)

        pygame.draw.line(screen, Color.BLACK.value,
                         (line_width, cls.INVENTORY_WINDOW_DIFF * 2),
                         (cls.INVENTORY_WINDOW_WIDTH + cls.INVENTORY_WINDOW_DIFF // 2, cls.INVENTORY_WINDOW_DIFF * 2),
                         3)

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
                item.draw_hover_info(screen, mouse_x, mouse_y)


class InventoryGUI:
    inventory_triggered = False

    @classmethod
    def display_inventory(cls, screen, inventory: Inventory, delta_time):
        InventoryImpl.display_inventory(screen, inventory, delta_time)
