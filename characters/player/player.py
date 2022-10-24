import pygame
from support_functions.support_functions import SupportFunctions
from enum import Enum
from util_timer.util_timer import Timer
from inventory.inventory import Inventory

# Class constans for all the player movements. Name is relative to the folder directory 
class Movement(Enum):
    UP = 'up'
    UP_IDLE = "up_idle"
    UP_SWING = "up_swing"
    DOWN = 'down'
    DOWN_IDLE = 'down_idle'
    DOWN_SWING = "down_swing"
    LEFT = 'left'
    LEFT_IDLE = 'left_idle'
    LEFT_SWING = "left_swing"
    RIGHT = 'right'
    RIGHT_IDLE = 'right_idle'
    RIGHT_SWING = "right_swing"

# Class constant for all the player weapon animations. Name is relative to the folder directory 
class Weapon(Enum):
    SWORD = '_swing'

# Class constants for all ther player abilities linked to the Timer
class TimerObjects(Enum):
    WEAPON_USE = 'use weapon'

class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple, group: pygame.sprite.Group):
        super().__init__(group)
        self.health = 100
        # get the basic graphics of the player
        self.import_graphics()
        self.movement_status = Movement.DOWN_IDLE.value
        self.player_frame = 0 
        # image of the sprite (width, height)
        self.image = self.animations[self.movement_status][self.player_frame]
        self.rect = self.image.get_rect(center = position)
        # vector direction as x = 0, y = 0
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.timers = {
            TimerObjects.WEAPON_USE.value: Timer(350, self.use_weapon)
        }

        # Player utilties
        self.selected_weapon = Weapon.SWORD.value

        # inventory
        self.inventory = Inventory()

    def controls(self):
        keys = pygame.key.get_pressed()
        if self.timers[TimerObjects.WEAPON_USE.value].check_active(): return

        # Vertical movements
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.movement_status = Movement.UP.value
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.movement_status = Movement.DOWN.value
        else:
            self.direction.y = 0

        # Horizontal movements
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.movement_status = Movement.RIGHT.value
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.movement_status = Movement.LEFT.value
        else: 
            self.direction.x = 0
        
        # weapon 
        if keys[pygame.K_k]:
            self.timers[TimerObjects.WEAPON_USE.value].start_timer()
            # reset the direction when using a weapon and the player index
            self.direction = pygame.math.Vector2()
            self.player_frame = 0


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def use_weapon(self):
        print("using weapon")

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
        # dictonary keys matches folder name
        self.animations = {
            Movement.UP.value: [], Movement.UP_IDLE.value: [], Movement.UP_SWING.value: [], 
            Movement.DOWN.value: [], Movement.DOWN_IDLE.value: [], Movement.DOWN_SWING.value: [],
            Movement.LEFT.value: [], Movement.LEFT_IDLE.value: [], Movement.LEFT_SWING.value: [],
            Movement.RIGHT.value: [], Movement.RIGHT_IDLE.value: [], Movement.RIGHT_SWING.value: [],
        }
        general_path = 'graphics/character/'
        for animation_key in self.animations.keys():
            animation_path = general_path + animation_key
            self.animations[animation_key] = SupportFunctions.import_folder(animation_path)
    
    def animate_character(self, delta_time):
        if self.timers[TimerObjects.WEAPON_USE.value].check_active():
            self.player_frame += 12 * delta_time
        else:
            self.player_frame += 4 * delta_time

        if self.player_frame >= len(self.animations[self.movement_status]):
            self.player_frame = 0
        self.image = self.animations[self.movement_status][int(self.player_frame)]
    
    def add_action_to_respected_status(self, action):
        return self.movement_status.split('_')[0] + action

    def check_idle_status(self):
        # if the player is not moving, add the idle
        if self.direction.magnitude() == 0:
            self.movement_status = self.add_action_to_respected_status("_idle")
        
        if self.timers[TimerObjects.WEAPON_USE.value].check_active():
            self.movement_status = self.add_action_to_respected_status(self.selected_weapon)


    def update(self, delta_time):
        self.controls()
        self.move(delta_time)
        self.animate_character(delta_time)
        self.update_timers()
        self.check_idle_status()

