import pygame

class Item(pygame.sprite.Sprite):

    def __init__(self, name, ability,  group):
        super().__init__(group)
        self.name = name
        self.ability = ability
    
    def display_description(self):
        ...