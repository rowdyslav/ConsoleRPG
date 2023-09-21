import yaml

from typing import Dict, Union, List
from base_classes import Player, Item

from item_types import Weapon, ActionWeapon, Consume


def load_equip(
    filename: str, players: List[Player], items: List[Item]
) -> Dict[Player, Dict[str, Item]]:
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

        for nick_or_ind, player_equip in data.items():
            if isinstance(nick_or_ind, str):
                player = [x for x in players if x.nick == nick_or_ind][0]
            elif isinstance(nick_or_ind, int) and not isinstance(
                data[nick_or_ind], Player
            ):
                player = players[nick_or_ind]
            else:
                print(
                    f"Неверный формат файла экипировки {filename}"
                    f"Ожидалось str или int, получено {nick_or_ind.__class__}"
                )
                break
            data[nick_or_ind] = player

            """Сдесь нужно сделать обработку дикта player_equip, который выглядит как {строка: строка}
               из этого сделать -> {строка: Item}
               где первая строка слот экипировки,
               а вторая строка name объекта Item"""
        return data
