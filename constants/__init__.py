from enum import Enum

GAME_WIDTH = GAME_HEIGHT = 800

INVEN_ITEM_BASE_X = 75
INVEN_ITEM_BASE_Y = 75
TILE_SIZE = 64

class FilePath(Enum):
    character_path = 'graphics/character'
    monsters = 'graphics/enemies/monsters'

weapon_images_path = 'graphics/character/weapons'
magic_path = 'graphics/character/magic'

class SpriteType(Enum):
    OBJECT = "object"
    INVISIBLE = "invisible"
    ENEMY = "enemy"
    GRASS = 'grass'

class StatsName(Enum):
    HEALTH = 'health'
    MANA = 'mana'
    DEFENSE = 'defense'
    ATTACK = 'action'
    MANA_ATTACK = 'mana_attack'
    SPEED = "speed"
    ATTACK_TYPE = "attack_type"
    RESISTANCE = "resistance"
    ATTACK_RADIUS = "attack_radius"
    NOTICE_RADIUS = "notice_radius"
    ATTACK_COOLDOWN = "attack_cooldown"
    MAX_HEALTH = "max_health"

# Enemy Data


entity_data = {
    'raccoon': {StatsName.HEALTH.value: 300, StatsName.MAX_HEALTH.value: 300, StatsName.DEFENSE.value: 25, StatsName.ATTACK.value: 15, StatsName.ATTACK_TYPE.value: 'claw', StatsName.ATTACK_COOLDOWN.value: 350, StatsName.SPEED.value: 180, StatsName.RESISTANCE.value: 3, StatsName.ATTACK_RADIUS.value: 50, StatsName.NOTICE_RADIUS.value: 300},
    'spirit': {StatsName.HEALTH.value: 100, StatsName.MAX_HEALTH.value: 100, StatsName.DEFENSE.value: 5, StatsName.ATTACK.value: 5, StatsName.ATTACK_TYPE.value: 'thunder', StatsName.ATTACK_COOLDOWN.value: 125, StatsName.SPEED.value: 270, StatsName.RESISTANCE.value: 3, StatsName.ATTACK_RADIUS.value: 50, StatsName.NOTICE_RADIUS.value: 250},
    'player': {StatsName.HEALTH.value: 100, StatsName.DEFENSE.value: 25, StatsName.ATTACK.value: 50, StatsName.MANA_ATTACK.value: 5, StatsName.ATTACK_COOLDOWN.value: 125, StatsName.MANA.value: 100, StatsName.SPEED.value: 500}
}


class PlayerUtilNames(Enum):
    MAGIC = "magic"
    WEAPON = "weapon"


class PlayerWeapons(Enum):
    SWORD = 'sword'
    SPEAR = "spear"
    SAI = "sai"
    AXE = "axe"


class PlayerMagics(Enum):
    FLAME = "flame"
    HEAL = "heal"


class ItemName(Enum):
    BEER = 'beer'
    WATER = 'water'


class Font(Enum):
    ARIAL = 'Arial'


class FontSize(Enum):
    size_18 = 18


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    DARK_RED = (84, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    ORANGE = (252, 163, 0)
    GREY = (168, 168, 168)
    GOLD = (255, 215, 0)


class CollisionName(Enum):
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
