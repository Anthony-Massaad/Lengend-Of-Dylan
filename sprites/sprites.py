import pygame
from constants import GAME_LAYERS

class GameObjects(pygame.sprite.Sprite):

    def __init__(self, pos, surface, groups, z_index=GAME_LAYERS['main']):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.z_index = z_index