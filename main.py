import pygame
import sys
from constants import *
from world.world import World

pygame.init()
display = pygame.display.set_mode((GAME_WIDTH + 1, GAME_HEIGHT + 1))
pygame.display.set_caption('Legend of Dylan')

class Game:

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((GAME_WIDTH + 1, GAME_HEIGHT + 1))
        pygame.display.set_caption('Legend of Dylan')
        self.clock = pygame.time.Clock()
        self.world = World()
    
    def run(self):
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