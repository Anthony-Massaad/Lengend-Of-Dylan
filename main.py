import pygame
from constants import *

pygame.init()
display = pygame.display.set_mode((GAME_WIDTH + 1, GAME_HEIGHT + 1))
pygame.display.set_caption('Legend of Dylan')

def draw_grid():
    square_distance = GAME_WIDTH // 17
    for i in range(square_distance):
        pygame.draw.line(display, (0, 0, 0), (1, i * square_distance),  (GAME_WIDTH, i * square_distance), 3)
        pygame.draw.line(display, (0, 0, 0), (i*square_distance, 1), (i*square_distance, GAME_HEIGHT), 3)

def draw():
    display.fill((255, 255, 255))
    draw_grid()
    pygame.display.update()
    pygame.time.delay(30)


def main():
    run = True 
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw()

    pygame.quit()

if __name__ == "__main__":
    main() 