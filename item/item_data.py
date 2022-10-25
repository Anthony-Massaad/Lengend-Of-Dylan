from constants import CharacterInfo

class ItemData:

    @classmethod
    def generate_dict_info(cls, health: int, defense: int, attack: int, stamina: int):
        return {
            CharacterInfo.HEALTH.value: health, 
            CharacterInfo.DEFENSE.value: defense,
            CharacterInfo.ATTACK.value: attack,
            CharacterInfo.STAMINA.value: stamina
        }
    
    @classmethod
    def beer(cls):
        return cls.generate_dict_info(-5, -2, 10, 10)
    
    @classmethod
    def water(cls):
        return cls.generate_dict_info(0, 0, 0, 50)