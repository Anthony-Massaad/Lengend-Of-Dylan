import pygame
from support_functions.support_functions import SupportFunctions
from enum import Enum

class Movement(Enum):
    UP = 'up'
    UP_IDLE = "up_idle"



class Player(pygame.sprite.Sprite):
    
    def __init__(self, position, group):
        super().__init__(group)
        # get the graphics of the character
        self.import_graphics()
        self.movement_status = Movement.UP.value
        self.player_frame = 0 
        # image of the sprite (width, height)
        self.image = self.animations[self.movement_status][self.player_frame]
        self.rect = self.image.get_rect(center = position)
        # vector direction as x = 0, y = 0
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = Movement.UP.value
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

    def move(self, delta_time):
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
        self.animations = {Movement.UP.value: [], Movement.UP_IDLE.value: []}
        general_path = 'graphics/character/'
        for animation_key in self.animations.keys():
            animation_path = general_path + animation_key
            self.animations[animation_key] = SupportFunctions.import_folder(animation_path)
        # print(self.animations)
    
    def animate_character(self, delta_time):
        self.player_frame += 4 * delta_time
        if self.player_frame >= len(self.animations[self.movement_status]):
            self.player_frame = 0
        self.image = self.animations[self.movement_status][int(self.player_frame)]
    
    def check_idle_status(self):
        # if the player is not moving, add the idle
        if self.direction.magnitude() == 0:
            self.movement_status = self.movement_status.split('_')[0] +  "_idle"

    def update(self, delta_time):
        self.controls()
        self.move(delta_time)
        self.animate_character(delta_time)
        self.check_idle_status()

