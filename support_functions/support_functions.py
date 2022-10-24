from os import walk
import pygame
from constants import Scaling

class SupportFunctions:

    @classmethod
    def import_folder(cls, path):
        image_surface_list = []
        for folder in walk(path):
            img_files = folder[2]
            for image in img_files:
                full_path = path + "/" + image
                image_surface = pygame.image.load(full_path)
                image_surface = pygame.transform.scale(image_surface, (Scaling.PLAYER_WIDTH.value, Scaling.PLAYER_HEIGHT.value))
                image_surface_list.append(image_surface)

        return image_surface_list