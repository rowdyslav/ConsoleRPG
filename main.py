from base_classes import Game, Player
from itertools import cycle

from loaders.equip import load_equip
from loaders.items import create_item_classes


def main():
    players = list(map(Player, input("Введите ники игроков через пробел -> ").split()))
    items = create_item_classes("settings/items.yml")
    # equip = load_equip("settings/equip.yml", players, items)

    session = Game(players, items)
    session.start()

    move_tip = (
        "Варианты хода:\n"
        "A - атака\n"
        "U - использовать расходник\n"
        "S - пропустить ход, восстановить 10% здоровья и 10% маны\n"
        "I - узнать свои данные (не завершает ход)\n"
        "-> "
    )

    turns_order = cycle(iter(players))
    player = next(turns_order)
    print(f"Ход игрока {player.nick}")
    try:
        while True:
            message, is_move_end = player.make_move(input(move_tip))
            while not is_move_end:
                print(message)
                message, is_move_end = player.make_move(input(move_tip))
            print(message)
            player = next(turns_order)
            print(f"Ход игрока {player.nick}")
    except KeyboardInterrupt:
        print("\nВыход из игры..")


if __name__ == "__main__":
    main()
