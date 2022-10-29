import pygame
from support_functions.support_functions import SupportFunctions
from constants import Color, Scaling, INVEN_ITEM_BASE_X, INVEN_ITEM_BASE_Y

class Item:

    def __init__(self, name: str, ability: dict, description: str):
        self.name = name
        self.ability = ability
        self.description = description
        self.scale = (Scaling.ITEM_WIDTH.value, Scaling.ITEM_HEIGHT.value)
        self.import_images()
        self.scale_images()
        self.animation_frame = 0
        self.image = self.animation[self.animation_frame]
        self.rect = self.image.get_rect(topleft = (INVEN_ITEM_BASE_X, INVEN_ITEM_BASE_Y)) 
    
    def check_equals(self, other_item):
        return self.name == other_item.name and self.ability == other_item.ability
    
    def import_images(self):
        folder_path = f'graphics/items/{self.name}'
        self.animation = SupportFunctions.import_folder(folder_path)
    
    def scale_images(self):
        for i, image in enumerate(self.animation):
            self.animation[i] = pygame.transform.scale(image, self.scale)
    
    def animate_item(self, delta_time):
        self.animation_frame += 4 * delta_time
        if self.animation_frame >= len(self.animation):
            self.animation_frame = 0
        self.image = self.animation[int(self.animation_frame)]

    def draw_item(self, screen, delta_time, x, y):
        self.animate_item(delta_time)
        self.rect.x, self.rect.y = x, y
        pygame.draw.rect(screen, Color.BLACK.value, pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2, 2, 2, 2)
        screen.blit(self.image, self.rect)

        