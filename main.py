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
        info = pygame.display.Info()
        w = info.current_w
        h = info.current_h

        self.display = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
        pygame.display.set_caption('Legend of Dylan')
        self.basic_font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()
        self.world = World(starting_terrain)
    
    def draw_fps(self):
        fps = f'FPS: {int(self.clock.get_fps())}'
        fps_text = self.basic_font.render(fps, 1, Color.BLACK.value)
        self.display.blit(fps_text, (10, 0))
        return fps_text

    def run(self) -> None:
        """
            Main game loop
        """
        Log.info("Game launched")
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Log.info("Exiting game")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Log.info("Exiting game")
                        pygame.quit()
                        sys.exit()
            
            # delta time needed to make everything frame rate independent 
            # so, regardless of the fps, the game will be executed at the same speed.
            delta_time = self.clock.tick() / 1000
            # print(delta_time)
            self.world.run(delta_time)
            self.draw_fps()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()