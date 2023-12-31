from random import randint, choice
from collections.abc import Callable
from typing import List, Dict

from item_types import Consume, Weapon

# from typing import Callable, Tuple  !Deprecated!


class Item:
    def __init__(self, name: str, mana_cost: int):
        self.name = name
        self.mana_cost = mana_cost

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__bases__[0].__name__}Item{vars(self)}"


class Player:
    def __init__(self, nick: str):
        self.game: Game = None
        self.nick = nick
        self.hp_max = randint(1, 100)
        self.mana_max = randint(1, self.hp_max)
        self.hp, self.mana = self.hp_max, self.mana_max
        self.weapon: Weapon = None
        self.consume: Consume = None

    def __str__(self):
        return self.nick

    def __repr__(self):
        return f"Player{vars(self)}"

    def _have_weapon(self) -> bool:
        return bool(self.weapon)

    def _have_consume(self) -> bool:
        return bool(self.consume)

    def _mana_enough(self, item: Item) -> bool:
        return self.mana > item.mana_cost

    def _get_targets(self, conditions: List[Callable]) -> list:
        return [
            target
            for target in self.game.players
            if all(cond(self, target) for cond in conditions)
        ]

    def _attack(self, other_player) -> tuple[str, bool]:
        wp = self.weapon

        self.mana -= wp.mana_cost

        other_player.hp -= wp.damage

        wp.durab -= 1
        if wp.durab == 0:
            self.weapon = None

        return (
            f"Атака {self.nick} оружием {wp.name} прошла успешно,"
            f"он теряет {wp.mana_cost} маны! {other_player.nick} теряет {wp.damage} хп!"
        ), True

    def _use(self) -> tuple[str, bool]:
        cs = self.consume

        self.mana -= cs.mana_cost

        self.hp += cs.hp_regen
        self.mana += cs.mana_regen

        cs.count -= 1

        if cs.count == 0:
            self.consume = None

        return (
            f"{self.nick} использовал {cs.name}, восстановив {cs.hp_regen} хп и {cs.mana_regen} маны",
            True,
        )

    def make_move(self, move: str) -> tuple[str, bool]:
        match move[0].upper():
            case "A":
                if not self._have_weapon():
                    return "Нет оружия для атаки!", False
                if not self._mana_enough(self.weapon):
                    return f"Недостаточно маны для атаки {self.weapon.name}", False

                form = "{} ({})\n"
                target_tip = (
                    "Возможные цели атаки:\n"
                    + "\n".join(
                        [
                            form.format(self.game.players.index(x), x.nick)
                            for x in self._get_targets([lambda i, j: i.nick != j.nick])
                        ]
                    )
                    + "-> "
                )
                target_index = int(input(target_tip))
                try:
                    result = self._attack(self.game.players[target_index])
                except IndexError:
                    result = "Неправильная цель атаки", False
                return result
            case "U":
                if not self._have_consume():
                    return "Нету расходника для использования!", False
                if not self._mana_enough(self.consume):
                    return (
                        f"Недостаточно маны для использования {self.consume.name}",
                        False,
                    )

                result = self._use()
                return result

            case "S":
                hp_reg, mana_reg = self.hp_max // 10, self.mana_max // 10
                return (
                    f"Игрок {self.nick} решает отдохнуть, восстанавливает {hp_reg} хп и {mana_reg} маны",
                    True,
                )

            case "I":
                message = (
                    f"Ваш ник - {self.nick}\n"
                    f"ХП - {self.hp} / {self.hp_max}\n"
                    f"Мана {self.mana} / {self.mana_max}\n"
                )

                message += f"Оружие {self.weapon}\n" if self.weapon else "Оружия нет\n"
                message += (
                    f"Расходник {self.consume} (еще {self.consume.count})\n"
                    if self.consume
                    else "Расходника нет\n"
                )

                return message, False
            case _:
                return "Неправильный ход!", False


class Game:
    def __init__(
        self,
        players: List[Player],
        items_dict: Dict[str, List[Item]],
        equip: Dict[Player, Dict[str, Item]] = None,
    ):
        self.players = players
        self.items_list = items_dict
        self.equip = equip

    def start(self):
        for player in self.players:
            if not player.game:
                player.game = self
            else:
                print(
                    f"Игрок {self.players.index(player)} ({player.nick}) уже находится в другой сессии!\n"
                    f"Удалите из этой с помощью Game.remove_player(индекс)"
                )
        if not self.equip:
            for player in self.players:
                player.weapon = choice(
                    self.items_list["Weapon"] + self.items_list["ActionWeapon"]
                )
                player.consume = choice(self.items_list["Consume"])
        else:
            for player in self.players:
                player.weapon = self.equip[player]["weapon"]
                player.consume = self.equip[player]["consume"]

    def get_players_info(self):  # ##
        return self.players
