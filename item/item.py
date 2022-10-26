import pygame

class Item:

    def __init__(self, name: str, ability: dict, description: str):
        self.name = name
        self.ability = ability
        self.description = description
    
    def check_equals(self, other_item):
        return self.name == other_item.name and self.ability == other_item.ability
    
    def import_image(self):
        ...