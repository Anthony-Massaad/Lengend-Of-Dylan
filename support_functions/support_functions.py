from csv import reader
from os import walk

import pygame

from constants import TILE_SIZE


class SupportFunctions:
    """Class for all support functions used around the game
    """

    @classmethod
    def import_csv_layout(cls, path: str) -> list:
        """Given the path of a csv file, import the layout into a list and return it.
        The layout consist of integers, where anything that is not -1 is the object. 

        Args:
            path (str): path of the csv file

        Returns:
            list: list of the csv layout
        """
        layout_map = []
        # -1 no tile, any other number there is something
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
            img_files = sorted(img_files)
            # print(img_files)
            for image in img_files:
                full_path = path + "/" + image
                image_surface = pygame.image.load(full_path).convert_alpha()
                # image_surface = pygame.transform.scale(image_surface, (TILE_SIZE, TILE_SIZE))
                image_surface_list.append(image_surface)

        return image_surface_list

    @classmethod
    def import_entity_folder(cls, path: str, scale: tuple) -> list:
        """collect all the images given a directory path, add them to a pygame surface and return a list

        Args:
            path (str): the file path where all the images for a given movement is located
            scale (tuple): image scale

        Returns:
            list: list of the image surface for a given movement of the character
        """
        image_surface_list = []
        # print(path)
        for folder in walk(path):
            img_files = folder[2]
            img_files = sorted(img_files)
            # print(img_files)
            for image in img_files:
                full_path = path + "/" + image
                image_surface = pygame.image.load(full_path).convert_alpha()
                image_surface = pygame.transform.scale(image_surface, scale)
                image_surface_list.append(image_surface)

        return image_surface_list
