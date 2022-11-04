import pygame
import sys
from constants import *
from constants.game_data import starting_terrain
from world.world import World
from logger.log import Log

class Game:

    def __init__(self) -> None:
        """Game initialization and setup
        """
        pygame.init()
        self.display = pygame.display.set_mode((GAME_WIDTH + 1, GAME_HEIGHT + 1))
        pygame.display.set_caption('Legend of Dylan')
        self.clock = pygame.time.Clock()
        self.world = World(starting_terrain)
    
    def run(self) -> None:
        """
            Main game loop
        """
        Log.info("Game launched")
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # delta time needed to make everything frame rate independent 
            # so, regardless of the fps, the game will be executed at the same speed.
            delta_time = self.clock.tick() / 1000
            # print(delta_time)
            self.world.run(delta_time)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()