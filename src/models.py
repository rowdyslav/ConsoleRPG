from dataclasses import dataclass
from random import Random


@dataclass(slots=True)
class Item:
    name: str
    mana_cost: int = 0


@dataclass(slots=True)
class Weapon(Item):
    damage: int = 1
    durability: int = 1


@dataclass(slots=True)
class ActionWeapon(Weapon):
    action_id: str = ""


@dataclass(slots=True)
class Consume(Item):
    hp_regen: int = 1
    mana_regen: int = 0
    count: int = 1


@dataclass(eq=False, slots=True)
class Player:
    nick: str
    hp_max: int
    mana_max: int
    hp: int
    mana: int
    weapon: Weapon | ActionWeapon | None = None
    consume: Consume | None = None

    @classmethod
    def random(cls, nick: str, rng: Random | None = None) -> Player:
        randomizer = rng or Random()
        hp_max = randomizer.randint(35, 100)
        mana_max = randomizer.randint(20, hp_max)
        return cls(nick=nick, hp_max=hp_max, mana_max=mana_max, hp=hp_max, mana=mana_max)

    def can_pay_mana(self, item: Item) -> bool:
        return self.mana >= item.mana_cost

    def restore(self, hp: int, mana: int) -> None:
        self.hp = min(self.hp_max, self.hp + hp)
        self.mana = min(self.mana_max, self.mana + mana)
