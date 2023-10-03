import yaml

from typing import Dict, Union, List
from base_classes import Player, Item


def load_equip(
    filename: str, players: List[Player], items: Dict[str, list[Item]]
) -> Dict[Player, Dict[str, Item]]:
    with open(filename, "r") as file:
        data = yaml.safe_load(file)

        nick_or_ind: Union[str, int]  # !typing! #
        player_equip: Dict[str, str]  # !typing! #
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

            for equip_slot, item_name in player_equip.items():
                item = [y for x in items for y in items[x] if y.name == item_name][0]

                data[nick_or_ind][player_equip][equip_slot] = item

        return data
