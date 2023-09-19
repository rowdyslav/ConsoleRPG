from item_types import Consume


class FairyFire(Consume):
    def __init__(self):
        super().__init__(name="Fairy Fire", mana_cost=0, hp_regen=20)
