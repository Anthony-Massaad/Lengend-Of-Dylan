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

    def _draw_grid(self):
        for i in range(SQUARE_DISTANCE):
            pygame.draw.line(display, (0, 0, 0), (1, i * SQUARE_DISTANCE),  (GAME_WIDTH, i * SQUARE_DISTANCE), 3)
            pygame.draw.line(display, (0, 0, 0), (i*SQUARE_DISTANCE, 1), (i*SQUARE_DISTANCE, GAME_HEIGHT), 3)
    
    def run(self):
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # delta time needed to make everything frame rate independent 
            # so, regardless of the fps, the game will be executed at the same speed.
            delta_time = self.clock.tick() / 1000
            self.world.run(delta_time)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()