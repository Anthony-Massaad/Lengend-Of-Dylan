from constants import StatsName


class ItemData:

    @classmethod
    def generate_dict_info(cls, health: int, defense: int, attack: int, stamina: int):
        return {
            StatsName.HEALTH.value: health,
            StatsName.DEFENSE.value: defense,
            StatsName.ATTACK.value: attack,
            StatsName.MANA.value: stamina
        }

    @classmethod
    def beer(cls):
        return cls.generate_dict_info(-5, -2, 10, 10)

    @classmethod
    def water(cls):
        return cls.generate_dict_info(0, 0, 0, 50)
