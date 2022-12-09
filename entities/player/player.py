import pygame
from support_functions.support_functions import SupportFunctions
from enum import Enum
from util_timer.util_timer import Timer
from inventory.inventory import Inventory
from inventory.inventory_gui import InventoryGUI
from constants import CharacterInfo, ItemName, CollisionName
from item.item import Item
from item.item_data import ItemData
from logger.log import Log

# Class constans for all the player movements. Name is relative to the folder directory 
class Movement(Enum):
    UP = 'up'
    UP_IDLE = "up_idle"
    UP_SWORD_SWING = "up_sword_swing"
    DOWN = 'down'
    DOWN_IDLE = 'down_idle'
    DOWN_SWORD_SWING = "down_sword_swing"
    LEFT = 'left'
    LEFT_IDLE = 'left_idle'
    LEFT_SWORD_SWING = "left_sword_swing"
    RIGHT = 'right'
    RIGHT_IDLE = 'right_idle'
    RIGHT_SWORD_SWING = "right_sword_swing"

# Class constant for all the player weapon animations. Name is relative to the folder directory 
class Weapon(Enum):
    SWORD = 'sword'


class Player(pygame.sprite.Sprite):

    def __init__(self, position: tuple, group: pygame.sprite.Group, game_obstacle_sprites: pygame.sprite.Group, screen: pygame.surface.Surface):
        super().__init__(group)
        # Player status
        self.current_stats = {
            CharacterInfo.HEALTH.value: 100,
            CharacterInfo.DEFENSE.value: 25,
            CharacterInfo.ATTACK.value: 10,
            CharacterInfo.MANA.value: 100
        }

        self.max_stats = {
            CharacterInfo.HEALTH.value: 100,
            CharacterInfo.MANA.value: 100
        }

        # TEMP 
        self.hit_time = {
            Weapon.SWORD.value: 0 
        }

        # get the basic graphics of the player
        self.import_graphics()
        self.movement_status = Movement.DOWN_IDLE.value
        self.player_frame = 0 
        self.screen = screen
        self.game_obstacle_sprites = game_obstacle_sprites
        # image of the sprite (width, height)
        self.image = self.animations[self.movement_status][self.player_frame]
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -20)
        # vector direction as x = 0, y = 0
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

        self.action_timers = {
            Weapon.SWORD.value: Timer(350, self.use_weapon)
        }

        # Player utilties
        self.selected_weapon = Weapon.SWORD.value

        self.selected_magic = None

        # inventory
        self.inventory = Inventory()
        self.inventory.add_item(Item(ItemName.BEER.value, ItemData.beer(), "beer"), 2)


    def controls(self, delta_time: float):
        keys = pygame.key.get_pressed()
        if self.action_timers[self.selected_weapon].check_active(): return
        
        # check inven active 
        if keys[pygame.K_l] and InventoryGUI.inventory_triggered:
            InventoryGUI.inventory_triggered = False
        elif InventoryGUI.inventory_triggered:
            InventoryGUI.display_inventory(self.screen, self.inventory, delta_time) 
            return

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
            self.action_timers[Weapon.SWORD.value].start_timer()
            # reset the direction when using a weapon and the player index
            self.direction = pygame.math.Vector2()
            self.player_frame = 0
        
        # inventory trigger
        if keys[pygame.K_i]:
            print("magic_triggered")


    def update_timer(self):
        self.action_timers[self.selected_weapon].update(self.hit_time[self.selected_weapon], int(self.player_frame))

    def use_weapon(self):
        direction = self.movement_status.split('_')[0]
        Log.info(f"Direction of attack is {direction}")

        if direction == Movement.RIGHT.value:
            ...
        elif direction == Movement.LEFT.value:
            ...
        elif direction == Movement.DOWN.value:
            print(self.hitbox.y)
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.hitbox.x, self.hitbox.y+64, 64, 64))

        elif direction == Movement.UP.value:
            ...


    def move(self, delta_time: float):
        # default the vector so diagonal is the same
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        
        # horizontal
        self.position.x += self.direction.x * self.speed * delta_time
        self.hitbox.x = self.position.x
        self.collision(CollisionName.HORIZONTAL.value)

        # vertical
        self.position.y += self.direction.y * self.speed * delta_time
        self.hitbox.y = self.position.y
        self.collision(CollisionName.VERTICAL.value)
        
        self.rect.center = self.hitbox.center
    
    def collision(self, direction: str):
        if direction == CollisionName.HORIZONTAL.value:
            for sprite in self.game_obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # check right
                    # move the overlap to the left side of the sprite
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # check left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.position.x = self.hitbox.x
        
        if direction == CollisionName.VERTICAL.value:
            for sprite in self.game_obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    # check down
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # check up 
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.position.y = self.hitbox.y

    
    def import_graphics(self):
        # dictonary keys matches folder name
        self.animations = {
            Movement.UP.value: [], Movement.UP_IDLE.value: [], Movement.UP_SWORD_SWING.value: [], 
            Movement.DOWN.value: [], Movement.DOWN_IDLE.value: [], Movement.DOWN_SWORD_SWING.value: [],
            Movement.LEFT.value: [], Movement.LEFT_IDLE.value: [], Movement.LEFT_SWORD_SWING.value: [],
            Movement.RIGHT.value: [], Movement.RIGHT_IDLE.value: [], Movement.RIGHT_SWORD_SWING.value: [],
        }
        general_path = 'graphics/character/'
        for animation_key in self.animations.keys():
            animation_path = general_path + animation_key
            self.animations[animation_key] = SupportFunctions.import_folder(animation_path)
    
    def animate_character(self, delta_time: float):
        if self.action_timers[self.selected_weapon].check_active():
            self.player_frame += 12 * delta_time
            Log.debug(f"Player frame on hit {int(self.player_frame)}")
        else:
            self.player_frame += 4 * delta_time

        if self.player_frame >= len(self.animations[self.movement_status]):
            self.player_frame = 0
        self.image = self.animations[self.movement_status][int(self.player_frame)]
    
    def add_action_to_respected_status(self, action: str):
        return self.movement_status.split('_')[0] + action

    def check_idle_status(self):
        # if the player is not moving, add the idle
        if self.direction.magnitude() == 0:
            self.movement_status = self.add_action_to_respected_status("_idle")
        
        if self.action_timers[Weapon.SWORD.value].check_active():
            self.movement_status = self.add_action_to_respected_status(f'_{self.selected_weapon}_swing')

    def update(self, delta_time: float):
        self.controls(delta_time)
        self.move(delta_time)
        # pygame.draw.rect(self.screen, (255,0,0), pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        self.animate_character(delta_time)
        self.update_timer()
        self.check_idle_status()


