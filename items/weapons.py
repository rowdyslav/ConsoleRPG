from item_types import Weapon


class BattleFury(Weapon):
    def __init__(self):
        super().__init__(name="Battle Fury", damage=10, durab=1, mana_cost=1)
