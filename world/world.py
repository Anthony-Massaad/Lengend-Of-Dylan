import pygame 
from constants import *
from characters.player.player import Player

class World:

    def __init__(self) -> None:
        """World initialization and setup
        """
        # get the surface that is generated in game
        self.display_surface = pygame.display.get_surface() 
        # all objects in the game 
        self.all_sprites = pygame.sprite.Group()
        self.setup()

    def setup(self) -> None:
        """Create the world setup
        """
        self.player = Player((GAME_WIDTH//2, GAME_WIDTH//2), self.all_sprites)

    def run(self, delta_time: float) -> None:
        """generate the world sprites

        Args:
            delta_time (float): the game clock for independent fps
        """
        self.display_surface.fill(Color.BLACK.value)
        self.all_sprites.draw(self.display_surface)
        # calls the update method on all the children
        self.all_sprites.update(delta_time)