import pygame

from constants import TILE_SIZE, SpriteType


class GameObjects(pygame.sprite.Sprite):
    """The Game Sprites class that inherits from pygame Sprite
    """

    def __init__(self, pos: tuple, groups: pygame.sprite.Group, sprite_type: SpriteType,
                 surface: pygame.surface.Surface = pygame.Surface((TILE_SIZE, TILE_SIZE))) -> None:
        """initialize the game sprites given the following parameters

        Args:
            pos (tuple): position of sprite
            groups (pygame.sprite.Group): the sprite group the sprite belongs to
            sprite_type (str): the type of this sprite (ex: invisible, objects..etc)
            surface (pygame.surface.Surface, optional): the sprite image. Defaults to pygame.Surface((TILE_SIZE, TILE_SIZE)) which shows nothing.
        """

        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        # takes a pygame rect and change the size of it
        if self.sprite_type == SpriteType.OBJECT:
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILE_SIZE))
            self.hitbox = self.rect.inflate(-10, -TILE_SIZE)
        elif self.sprite_type == SpriteType.GRASS:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, -15)
        else:
            self.rect = self.image.get_rect(topleft=pos)
            self.hitbox = self.rect.inflate(0, 0)



    def update(self, delta_time):
        ...
        # pygame.draw.rect(pygame.display.get_surface(), (255,0, 0), pygame.Rect(self.hitbox.x, self.hitbox.y, self.hitbox.width, self.hitbox.height), 2)
