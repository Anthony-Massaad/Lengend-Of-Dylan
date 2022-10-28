from turtle import Screen
import pygame
from inventory.inventory import Inventory
from constants import GAME_WIDTH, GAME_HEIGHT, Color


class InventoryGUI:
    inventory_triggered = False
    INVENTORY_WINDOW_WIDTH = INVENTORY_WINDOW_HEIGHT = GAME_WIDTH - 100 

    @classmethod
    def display_inventory(cls, SCREEN, inventory: Inventory, delta_time):
        cls.inventory_triggered = True
        window = pygame.draw.rect(SCREEN, Color.WHITE.value, pygame.Rect(50,50, cls.INVENTORY_WINDOW_WIDTH, cls.INVENTORY_WINDOW_HEIGHT), 0, 2, 2, 2)

        inventory_keys = inventory.get_keys()
        for item in inventory_keys:
            item.draw_item(SCREEN, delta_time)
            # print(f"name: {keys.name} ability: {keys.ability}  description: {keys.description} image: {keys.image}")

