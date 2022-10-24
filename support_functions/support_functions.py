from os import walk
import pygame
from constants import Scaling

class SupportFunctions:

    @classmethod
    def import_folder(cls, path: str) -> list:
        """collect all the images given a directory path, add them to a pygame surface and return a list

        Args:
            path (str): the file path where all the images for a given movement is located

        Returns:
            list: list of the image surface for a given movement of the character
        """
        image_surface_list = []
        for folder in walk(path):
            img_files = folder[2]
            for image in img_files:
                full_path = path + "/" + image
                image_surface = pygame.image.load(full_path)
                image_surface = pygame.transform.scale(image_surface, (Scaling.PLAYER_WIDTH.value, Scaling.PLAYER_HEIGHT.value))
                image_surface_list.append(image_surface)

        return image_surface_list