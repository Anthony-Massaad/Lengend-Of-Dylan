import pygame
from support_functions.support_functions import SupportFunctions

class Player(pygame.sprite.Sprite):
    
    def __init__(self, position, group):
        super().__init__(group)
        # get the graphics of the character
        self.import_graphics()
        self.movement_status = 'up'
        self.player_frame = 0 
        # image of the sprite (width, height)
        self.image = self.animations[self.movement_status][self.player_frame]
        self.rect = self.image.get_rect(center = position)

        # vector direction as x = 0, y = 0
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def _controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else: 
            self.direction.x = 0

    def _move(self, delta_time):
        # default the vector so diagonal is the same
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal
        self.position.x += self.direction.x * self.speed * delta_time
        self.rect.centerx = self.position.x

        # vertical
        self.position.y += self.direction.y * self.speed * delta_time
        self.rect.centery = self.position.y
    
    def import_graphics(self):
        # dict key matches folder name
        self.animations = {'up': []}
        general_path = 'graphics/character/'
        for animation_key in self.animations.keys():
            animation_path = general_path + animation_key
            self.animations[animation_key] = SupportFunctions.import_folder(animation_path)
        print(self.animations)


    def update(self, delta_time):
        self._controls()
        self._move(delta_time)

