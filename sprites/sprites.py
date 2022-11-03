import pygame
from constants import TILE_SIZE

class GameObjects(pygame.sprite.Sprite):

    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE)) ):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        # takes a pygame rect and change the size of it
        if self.sprite_type == 'objects':
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILE_SIZE))
        else: 
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
    
    def update(self, delta_time):
        ...
        # pygame.draw.rect(pygame.display.get_surface(), (255,0, 0), pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)
