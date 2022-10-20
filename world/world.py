import pygame 
from constants import *

class World:

    def __init__(self):
        # get the surface that is generated in game
        self.display_surface = pygame.display.get_surface() 

        # all objects in the game 
        self.all_sprites = pygame.sprite.Group()

    def run(self, delta_time):
        self.display_surface.fill(Color.BLACK.value)
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()