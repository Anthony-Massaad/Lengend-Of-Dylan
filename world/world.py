import pygame
import random

from constants import *
from entities.player.player import Player
from logger.log import Log
from sprites.sprites import GameObjects
from support_functions.support_functions import SupportFunctions
from user_interface.user_interface import UserInterface
from entities.enemy.enemy import Enemy

class RoomView(pygame.sprite.Group):
    """the view of the game, which inherits from pygame Group
    """

    def __init__(self) -> None:
        """Initialize the RoomView for given groups. 
        Generate offsets for the game, sprites and map.
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.view_offset = pygame.math.Vector2()

        self.has_offset = False

    def draw_room(self, player: Player, map, map_rect) -> None:
        """draw the game room with all the sprites

        Args:
            player (Player): the game player
        """

        # offset for game
        # self.view_offset.x = player.rect.centerx - self.half_width
        # self.view_offset.y = player.rect.centery - self.half_height

        self.view_offset.x = player.rect.centerx - (GAME_WIDTH // 2)
        self.view_offset.y = player.rect.centery - (GAME_HEIGHT // 2)
        # Log.info(f"Offset for game (x: {self.view_offset.x}, y: {self.view_offset.y})")
        # drawing floor as first thing to draw

        ground_offset = map_rect.topleft - self.view_offset
        # Log.debug(f"Offset for map {ground_offset}") -1372 right bottom 0 left up
        # print(ground_offset, -map_rect.width + GAME_WIDTH, -map_rect.height + GAME_HEIGHT)
        # hard stop for -1372 right bottom 0 left up
        # x = min(0, int(ground_offset.x)) # left
        # y = min(0, int(ground_offset.y)) # top
        # x = max(-map_rect.width + GAME_WIDTH, x) # right
        # y = max(-map_rect.height + GAME_HEIGHT, y) # bottom
        # self.display_surface.blit(map, (x, y))
        self.display_surface.blit(map, ground_offset)
        # print(map_rect.width - self.view_offset.x - GAME_WIDTH, map_rect.height - self.view_offset.y - GAME_HEIGHT)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset = sprite.rect.topleft - self.view_offset
            self.display_surface.blit(sprite.image, offset)

    def enemy_update(self, player, enemies):
        for enemy in enemies:
            enemy.enemy_update(player)

class World:
    def __init__(self, terrain: dict) -> None:
        """World initialization, setup and main game run
        """
        # get the surface that is generated in game

        self.display_surface = pygame.display.get_surface()
        self.terrain_data = self.generate_terrain_data(terrain)
        self.graphics = {
            'objects': SupportFunctions.import_folder('graphics/map/objects'),
            'grass': SupportFunctions.import_folder('graphics/map/grass')
        }
        Log.info("game graphics imported")
        # all objects in the game 
        self.visible_sprites = RoomView()
        self.obstacle_sprites = RoomView()
        self.player = None
        self.enemies = None
        self.map = None
        self.map_rect = None
        self.setup()
        self.user_interface = UserInterface()

        # self.enemies = []

    def generate_terrain_data(self, terrain: dict) -> dict:
        data = {}
        for style, path in terrain.items():
            data[style] = SupportFunctions.import_csv_layout(path)
        Log.debug(f"data generated for terrain {terrain}")
        return data

    def setup(self) -> None:
        """Create the world setup
        """

        for style, layout in self.terrain_data.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                    if col == '-1':
                        continue
                    if style == 'bounds':
                        GameObjects((x, y), [self.obstacle_sprites], SpriteType.INVISIBLE)
                    elif style == 'objects':
                        GameObjects((x, y), [self.visible_sprites, self.obstacle_sprites], SpriteType.OBJECT,
                                    self.graphics['objects'][int(col)])
                    elif style == 'grass':
                        GameObjects((x, y), [self.visible_sprites, self.obstacle_sprites], SpriteType.GRASS, self.graphics['grass'][int(col)])
                    elif style == 'entities':
                        if col == '394':
                            # entity is player
                            self.player = Player("player", (x, y), [self.visible_sprites], self.obstacle_sprites)
                        else:
                            monster_name = ""
                            if col == '392':
                                monster_name = "raccoon"
                            elif col == "391":
                                monster_name = "spirit"

                            if monster_name == "":
                                Log.error("MONSTER NAME UNKNOWN")

                            Enemy(monster_name, (x, y), [self.visible_sprites], self.obstacle_sprites)


        self.enemies = [sprite for sprite in self.visible_sprites.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == "enemy"]

        # add string to terrain data
        self.map = pygame.image.load("graphics/map/starting_room.png").convert()
        self.map_rect = self.map.get_rect(topleft=(0, 0))

        if not self.enemies:
            Log.warning("No enemies in the map")

        Log.info("game terrain setup complete")

        Log.info("player setup complete")

        Log.info("game setup complete")

    def run(self, delta_time: float) -> None:
        """generate the world sprites

        Args:

            delta_time (float): the game clock for independent fps
        """
        self.display_surface.fill(Color.BLACK.value)
        self.visible_sprites.enemy_update(self.player, self.enemies)
        self.visible_sprites.update(delta_time)
        self.visible_sprites.draw_room(self.player, self.map, self.map_rect)
        self.user_interface.draw(self.player, self.enemies)
