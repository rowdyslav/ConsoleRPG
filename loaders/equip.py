import yaml

from typing import Dict, List
from base_classes import Player, Item


def load_equip(
    filename: str, players: List[Player], items: Dict[str, list[Item]]
) -> Dict[Player, Dict[str, Item]]:
    with open(filename, "r") as file:
        data: Dict[str | int, Dict[str, str]] = yaml.safe_load(file)

    result: Dict[Player, Dict[str, Item]] = {}
    for nick_or_index, player_equip in data.items():
        if isinstance(nick_or_index, str):
            player = [x for x in players if x.nick == nick_or_index][0]
        elif isinstance(nick_or_index, int) and not isinstance(
            data[nick_or_index], Player
        ):
            player = players[nick_or_index]
        else:
            print(
                f"Неверный формат файла экипировки {filename}"
                f"Ожидалось str или int, получено {nick_or_index.__class__}"
            )
            break

        for equip_slot, item_name in player_equip.items():
            item = [y for x in items for y in items[x] if y.name == item_name][0]
            result[player][equip_slot] = item

    return result
