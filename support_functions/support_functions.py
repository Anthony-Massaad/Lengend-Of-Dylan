from os import walk
import pygame
from constants import TILE_SIZE
from csv import reader

class SupportFunctions:

    @classmethod
    def import_csv_layout(cls, path):
        layout_map = []
        # -1 no tile, 395 there is a bound for the player
        with open(path) as map:
            layout = reader(map, delimiter=',')
            for row in layout:
                layout_map.append(list(row))
        return layout_map

    @classmethod
    def import_folder(cls, path: str) -> list:
        """collect all the images given a directory path, add them to a pygame surface and return a list

        Args:
            path (str): the file path where all the images for a given movement is located

        Returns:
            list: list of the image surface for a given movement of the character
        """
        image_surface_list = []
        # print(path)
        for folder in walk(path):
            img_files = folder[2]
            # print(img_files)
            for image in img_files:
                full_path = path + "/" + image
                image_surface = pygame.image.load(full_path).convert_alpha()
                image_surface = pygame.transform.scale(image_surface, (TILE_SIZE, TILE_SIZE))
                image_surface_list.append(image_surface)

        return image_surface_list