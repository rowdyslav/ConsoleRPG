from random import randint
from typing import List


class Player:
    def __init__(self, n):
        self.nick = n
        self.hp_max = randint(1, 100)
        self.mana_max = randint(1, self.hp_max)
        self.hp, self.mana = self.hp_max, self.mana_max
        self.weapon = None
        self.consume = None

    def __str__(self):
        return self.nick

    def __repr__(self):
        return f"Player{vars(self)}"

    def have_weapon(self):
        return bool(self.weapon)

    def have_consume(self):
        return bool(self.consume)

    def attack(self, other_player):
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

    def use(self):
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


class Item:
    def __init__(self, name: str = "Неизвестный предмет", mana_cost: int = 0):
        self.name = name
        self.mana_cost = mana_cost

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__bases__[0].__name__}Item{vars(self)}"

    def mana_enough(self, player: Player):
        return player.mana > self.mana_cost


class Game:
    def __init__(self, players: List[Player]):
        self.players = players

    def get_players_info(self):
        return self.players

    def enum_players(self, without=""):
        return [
            f"{x} ({y.nick})" for x, y in enumerate(self.players) if y.nick != without
        ]

    def make_move(self, player, move):
        match move[0].upper():
            case "A":
                if not player.have_weapon():
                    return "Нет оружия для атаки!", False
                if not player.weapon.mana_enough(player):
                    return f"Недостаточно маны для атаки {player.weapon.name}", False

                n = "\n"
                target_index = int(
                    input(
                        f"Возможные цели атаки: {n.join(self.enum_players(without=player.nick))}\n-> "
                    )
                )
                try:
                    result = player.attack(self.players[target_index])
                except IndexError:
                    result = "Неправильная цель атаки", False
                return result
            case "U":
                if not player.have_consume():
                    return "Нету расходника для использования!", False

                if not player.consume.mana_enough(player):
                    return (
                        f"Недостаточно маны для использования {player.consume.name}",
                        False,
                    )

                result = player.use()
                return result
            case "S":
                hp_reg, mana_reg = player.hp_max / 10, player.mana_max / 10
                return (
                    f"Игрок {player.nick} решает отдохнуть, восстанавливает {hp_reg} хп и {mana_reg} маны",
                    True,
                )
            case "I":
                message = (
                    f"Ваш ник - {player.nick}\n"
                    f"ХП - {player.hp} / {player.hp_max}\n"
                    f"Мана {player.mana} / {player.mana_max}\n"
                )

                message += (
                    f"Оружие {player.weapon}\n" if player.weapon else "Оружия нет\n"
                )
                message += (
                    f"Расходник {player.consume} (еще {player.consume.count})\n"
                    if player.consume
                    else "Расходника нет\n"
                )

                return message, False
            case _:
                return "Неправильный ход!", False
