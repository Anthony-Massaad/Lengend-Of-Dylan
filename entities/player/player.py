from enum import Enum

import pygame

from constants import StatsName, ItemName, entity_data, PlayerWeapons, PlayerMagics, PlayerUtilNames, FilePath
from inventory.inventory import Inventory
from item.item import Item
from item.item_data import ItemData
from logger.log import Log
from support_functions.support_functions import SupportFunctions
from timer.timer import Timer
from entities.entity import Entity

# Class constants for all the player movements. Name is relative to the folder directory
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


class DataConstant(Enum):
    STRENGTH = 'strength'
    COST = 'cost'


class Player(Entity):

    def __init__(self, sprite_name, position: tuple, group: pygame.sprite.Group, game_obstacle_sprites: pygame.sprite.Group):
        super().__init__(group, game_obstacle_sprites, position, Movement, FilePath.character_path.value, sprite_name)
        self.max_stats = {
            StatsName.HEALTH.value: 100,
            StatsName.MANA.value: 100
        }

        self.magic_data = {
            PlayerMagics.FLAME.value: {DataConstant.STRENGTH: 5, DataConstant.COST: 55},
            PlayerMagics.HEAL.value: {DataConstant.STRENGTH: 25, DataConstant.COST: 35}
        }

        ### BEGINNING OF UTILS ###
        self.util_switch_direction = 1
        self.last_util_switch = PlayerUtilNames.MAGIC
        # Player weapons
        self.weapon_index = 0
        self.weapons = []
        for weapon_name in PlayerWeapons:
            self.weapons.append(weapon_name.value)
        self.selected_weapon = self.weapons[self.weapon_index]
        self.weapon_switch_timer = Timer(200, lambda direction: self.switch_weapon(direction))
        Log.info(f"Player weapons list: {self.weapons}")
        # Player Magic
        self.magic_index = 0
        self.magics = []
        for magic in PlayerMagics:
            self.magics.append(magic.value)
        Log.info(f"Player Magics List: {self.magics}")
        self.selected_magic = self.magics[self.magic_index]
        self.magic_switch_timer = Timer(200, lambda direction: self.switch_magic(direction))
        # utils timer
        self.util_timers = {
            PlayerWeapons.SWORD.value: Timer(300, self.use_weapon),
            PlayerMagics.FLAME.value: Timer(200, self.use_magic),
            PlayerMagics.HEAL.value: Timer(200, self.use_magic)
        }
        ### END OF UTILS ###
        self.mana_regen_timer = Timer(350, self.mana_regeneration)

        # inventory
        self.inventory = Inventory()
        self.inventory.add_item(Item(ItemName.BEER.value, ItemData.beer(), "beer"), 2)

    def controls(self):
        keys = pygame.key.get_pressed()
        if self.util_timers[self.selected_weapon].active:
            return
        # check inven active 
        # if keys[pygame.K_l] and InventoryGUI.inventory_triggered:
        #     InventoryGUI.inventory_triggered = False
        # elif InventoryGUI.inventory_triggered:
        #     InventoryGUI.display_inventory(self.screen, self.inventory, delta_time)
        #     return

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

        if self.util_timers[self.selected_magic].active:
            return

        # weapon invoked
        if keys[pygame.K_k]:
            Log.info(f"Player attack invoked using {self.selected_weapon}")
            self.util_timers[self.selected_weapon].start_timer()
            # reset the direction when using a weapon and the player index
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # magic invoked
        if keys[pygame.K_i]:
            Log.info(f"Player Magic invoked using {self.selected_magic}")
            self.util_timers[self.selected_magic].start_timer()
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # Switching weapons
        if not self.weapon_switch_timer.active:
            if keys[pygame.K_l]:
                Log.info(f"Player weapon switching invoked forward")
                self.weapon_switch_timer.start_timer()
                self.util_switch_direction = 1
                self.last_util_switch = PlayerUtilNames.WEAPON

            if keys[pygame.K_j]:
                Log.info(f"Player weapon switching invoked backward")
                self.weapon_switch_timer.start_timer()
                self.util_switch_direction = -1
                self.last_util_switch = PlayerUtilNames.WEAPON

        # Switching magic
        if not self.magic_switch_timer.active:
            if keys[pygame.K_o]:
                Log.info(f"Player magic switching invoked forward")
                self.magic_switch_timer.start_timer()
                self.util_switch_direction = 1
                self.last_util_switch = PlayerUtilNames.MAGIC

            if keys[pygame.K_u]:
                Log.info(f"Player magic switching invoked backward")
                self.magic_switch_timer.start_timer()
                self.util_switch_direction = -1
                self.last_util_switch = PlayerUtilNames.MAGIC

        # # inventory trigger
        # if keys[pygame.K_i]:
        #     self.weapon_switch_timer.switch_util()
        #     print("magic_triggered")

    def update_timers(self):
        self.util_timers[self.selected_weapon].trigger_action()
        self.util_timers[self.selected_magic].trigger_action()
        self.weapon_switch_timer.change_util(self.util_switch_direction)
        self.magic_switch_timer.change_util(self.util_switch_direction)
        self.mana_regen_timer.mana_regeneration()

    def switch_magic(self, direction):
        Log.info(f"Weapon switch direction {direction}")
        self.magic_index += direction
        if self.magic_index >= len(self.magics):
            self.magic_index = 0
        if self.magic_index < 0:
            self.magic_index = len(self.magics) - 1
        self.selected_magic = self.magics[self.magic_index]
        Log.info(f"Current weapon is {self.selected_magic}")

    def use_magic(self):
        strength = self.magic_data[self.selected_magic][DataConstant.STRENGTH]
        if self.selected_magic != PlayerMagics.HEAL.value:
            strength += self.current_stats[StatsName.MANA_ATTACK.value]
        cost = self.magic_data[self.selected_magic][DataConstant.COST]
        Log.debug(f"Magic strength of {self.selected_magic} is {strength}")
        Log.debug(f"Magic cost of {self.selected_magic} is {cost}")

        if not self.reduce_mana(cost):
            return

        if self.selected_magic == PlayerMagics.HEAL.value:
            self.heal(strength)

    def reduce_mana(self, cost):
        if self.current_stats[StatsName.MANA.value] < cost:
            return False
        self.current_stats[StatsName.MANA.value] -= cost
        if self.current_stats[StatsName.MANA.value] > self.max_stats[StatsName.MANA.value]:
            self.current_stats[StatsName.MANA.value] = self.max_stats[StatsName.MANA.value]

        return True

    def heal(self, strength):
        self.current_stats[StatsName.HEALTH.value] += strength
        if self.current_stats[StatsName.HEALTH.value] > self.max_stats[StatsName.HEALTH.value]:
            self.current_stats[StatsName.HEALTH.value] = self.max_stats[StatsName.HEALTH.value]

    def switch_weapon(self, direction):
        Log.info(f"Weapon switch direction {direction}")
        self.weapon_index += direction
        if self.weapon_index >= len(self.weapons):
            self.weapon_index = 0
        if self.weapon_index < 0:
            self.weapon_index = len(self.weapons) - 1
        Log.debug(f"Current weapon is {self.weapons[self.weapon_index]}")

    def use_weapon(self):
        direction = self.movement_status.split('_')[0]
        Log.info(f"Direction of attack is {direction}")
        if direction == Movement.RIGHT.value:
            ...
        elif direction == Movement.LEFT.value:
            ...
        elif direction == Movement.DOWN.value:
            ...
        elif direction == Movement.UP.value:
            ...

    def mana_regeneration(self):
        self.current_stats[StatsName.MANA.value] += 4
        if self.current_stats[StatsName.MANA.value] > self.max_stats[StatsName.MANA.value]:
            self.current_stats[StatsName.MANA.value] = self.max_stats[StatsName.MANA.value]

        Log.info(f"Mana regenerating. Current {self.current_stats[StatsName.MANA.value]}")

    def animate_entity(self, delta_time: float):
        if self.util_timers[self.selected_weapon].active:
            self.frame_index += 12 * delta_time
            Log.debug(f"Player frame on hit {int(self.frame_index)}")
        else:
            self.frame_index += 4 * delta_time

        if self.frame_index >= len(self.animations[self.movement_status]):
            self.frame_index = 0
        self.image = self.animations[self.movement_status][int(self.frame_index)]

    def add_action_to_respected_status(self, action: str):
        return self.movement_status.split('_')[0] + action

    def check_idle_status(self):
        # if the player is not moving, add the idle
        if self.direction.magnitude() == 0:
            self.movement_status = self.add_action_to_respected_status("_idle")

        if self.util_timers[PlayerWeapons.SWORD.value].active:
            self.movement_status = self.add_action_to_respected_status(f'_{self.selected_weapon}_swing')

    def update(self, delta_time: float):
        self.controls()
        if self.current_stats[StatsName.MANA.value] < self.max_stats[StatsName.MANA.value] and not self.mana_regen_timer.active:
            self.mana_regen_timer.start_timer()
        self.move(delta_time)
        self.animate_entity(delta_time)
        self.update_timers()
        self.check_idle_status()
        # weapon switching
