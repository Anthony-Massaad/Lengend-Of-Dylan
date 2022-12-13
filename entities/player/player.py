import random
from enum import Enum

import pygame

from constants import StatsName, ItemName, PlayerWeapons, PlayerMagics, PlayerUtilNames, FilePath, GAME_WIDTH
from inventory.inventory import Inventory
from item.item import Item
from item.item_data import ItemData
from logger.log import Log
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

    def __init__(self, sprite_name, position: tuple, group: pygame.sprite.Group, visible_sprites, game_obstacle_sprites: pygame.sprite.Group, attackable_sprites: pygame.sprite.Group, particle_animations):
        super().__init__(group, visible_sprites, game_obstacle_sprites, attackable_sprites, position, Movement, FilePath.character_path.value, sprite_name, particle_animations)
        self.max_stats = {
            StatsName.HEALTH.value: 100,
            StatsName.MANA.value: 100
        }

        self.magic_data = {
            PlayerMagics.FLAME.value: {DataConstant.STRENGTH: 5, DataConstant.COST: 55},
            PlayerMagics.HEAL.value: {DataConstant.STRENGTH: 15, DataConstant.COST: 10}
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
        self.magic_timers = {
            PlayerMagics.FLAME.value: Timer(1000, self.allow_magic),
            PlayerMagics.HEAL.value: Timer(800, self.allow_magic)
        }
        self.magic_invoked = False
        ### END OF UTILS ###
        self.mana_regen_timer = Timer(350, self.mana_regeneration)
        # inventory
        self.inventory = Inventory()
        self.inventory.add_item(Item(ItemName.BEER.value, ItemData.beer(), "beer"), 2)

    def controls(self):
        keys = pygame.key.get_pressed()
        if self.is_attacking:
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

        if self.magic_invoked:
            return

        # weapon invoked
        if keys[pygame.K_k] and not self.attack_cooldown.active:
            Log.info(f"Player attack invoked using {self.selected_weapon}")
            self.is_attacking = True
            self.attack()
            # reset the direction when using a weapon and the player index
            self.direction = pygame.math.Vector2()
            self.frame_index = 0

        # magic invoked
        if keys[pygame.K_i] and not self.magic_timers[self.selected_magic].active:
            Log.info(f"Player Magic invoked using {self.selected_magic}")
            self.magic_invoked = True
            self.use_magic()
            self.magic_timers[self.selected_magic].start_timer()
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
        self.attack_cooldown.cooldown()
        self.magic_timers[self.selected_magic].cooldown()
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

    def allow_magic(self):
        self.magic_invoked = False

    def attack(self):
        direction = self.movement_status.split('_')[0]
        Log.info(f"Direction of attack is {direction}")
        attack = None
        if direction == Movement.RIGHT.value:
            attack = self.image.get_rect(center=self.rect.center)
            attack.x += 32
        elif direction == Movement.LEFT.value:
            attack = self.image.get_rect(center=self.rect.center)
            attack.x -= 32
        elif direction == Movement.DOWN.value:
            attack = self.image.get_rect(center=self.rect.center)
            attack.y += 32
        elif direction == Movement.UP.value:
            attack = self.image.get_rect(center=self.rect.center)
            attack.y -= 32
        attack = attack.inflate(0, -32)

        for attackable_sprite in self.attackable_sprites:
            if attackable_sprite.hitbox.colliderect(attack):
                if attackable_sprite.sprite_type == "enemy":
                    attackable_sprite.is_attacked(self.current_stats[StatsName.ATTACK.value])
                else:
                    pos = attackable_sprite.rect.center - pygame.math.Vector2(0, 64)
                    for amount_leaves in range(random.randint(2, 6)):
                        self.particle_animations.create_grass_particles(pos, self.visible_sprites)
                    attackable_sprite.kill()

    def mana_regeneration(self):
        self.current_stats[StatsName.MANA.value] += 4
        if self.current_stats[StatsName.MANA.value] > self.max_stats[StatsName.MANA.value]:
            self.current_stats[StatsName.MANA.value] = self.max_stats[StatsName.MANA.value]

        Log.debug(f"Mana regenerating. Current {self.current_stats[StatsName.MANA.value]}")

    def animate_entity(self, delta_time: float):
        self.frame_index += 4 * delta_time * 2
        if self.frame_index >= len(self.animations[self.movement_status]):
            if self.is_attacking:
                self.is_attacking = False
                self.attack_cooldown.start_timer()
                self.attack()
            self.frame_index = 0
        self.image = self.animations[self.movement_status][int(self.frame_index)]

    def add_action_to_respected_status(self, action: str):
        return self.movement_status.split('_')[0] + action

    def check_idle_status(self):
        # if the player is not moving, add the idle
        if self.direction.magnitude() == 0:
            self.movement_status = self.add_action_to_respected_status("_idle")

        if self.is_attacking:
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
