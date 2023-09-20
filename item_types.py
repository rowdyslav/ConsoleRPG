from base_classes import Item


class Weapon(Item):
    def __init__(self, name: str = None, mana_cost: int = None, damage: int = 1, durab: int = 1):
        super().__init__(name, mana_cost)
        self.damage = damage
        self.durab = durab


class ActionWeapon(Weapon):
    def action(self):
        pass


class Consume(Item):
    def __init__(
            self, name: str = None, mana_cost: int = None, hp_regen: int = 0, mana_regen: int = 0, count: int = 1
    ):
        super().__init__(name, mana_cost)
        self.count = count
        self.hp_regen = hp_regen
        self.mana_regen = mana_regen
