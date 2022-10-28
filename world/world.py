import pygame 
from constants import *
from characters.player.player import Player
from sprites.sprites import GenericSprites

class RoomView(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() 

    def draw_room(self):
        for layer in GAME_LAYERS.values():
            for sprite in self.sprites():
                if sprite.z_index == layer:
                    self.display_surface.blit(sprite.image, sprite.rect)

class World:
    def __init__(self) -> None:
        """World initialization and setup
        """
        # get the surface that is generated in game
        self.display_surface = pygame.display.get_surface() 
        # all objects in the game 
        self.all_sprites = RoomView()
        self.setup()

    def setup(self) -> None:
        """Create the world setup
        """
        self.player = Player((GAME_WIDTH//2, GAME_WIDTH//2), self.all_sprites, self.display_surface)
        
        # room 
        GenericSprites(
            pos=(0, 0), 
            surface=pygame.transform.scale(pygame.image.load('graphics/room/room1.png').convert_alpha(), (GAME_WIDTH, GAME_HEIGHT)),
            groups=self.all_sprites,
            z_index=GAME_LAYERS[GameLayerKeys.GROUND.value]
        )

    def run(self, delta_time: float) -> None:
        """generate the world sprites

        Args:
            delta_time (float): the game clock for independent fps
        """
        self.display_surface.fill(Color.BLACK.value)
        # self.all_sprites.draw(self.display_surface)
        self.all_sprites.draw_room()
        # calls the update method on all the children
        self.all_sprites.update(delta_time)