from base_classes import Game, Player
from itertools import cycle

from items_loader import create_item_classes


def main():
    players = list(map(Player, input("Введите ники игроков через пробел -> ").split()))
    items = create_item_classes("items.yml")

    session = Game(players, items)
    session.start()

    mm = Player.make_move
    move_tip = (
        "Варианты хода:\n"
        "A - атака\n"
        "U - использовать расходник\n"
        "S - пропустить ход, восстановить 10% здоровья и 10% маны\n"
        "I - узнать свои данные (не завершает ход)\n"
        "-> "
    )

    order = cycle(iter(players))
    player = next(order)
    print(f"Ход игрока {player.nick}")
    try:
        while True:
            message, is_move_end = mm(player, input(move_tip))
            while not is_move_end:
                print(message)
                message, is_move_end = mm(player, input(move_tip))
            print(message)
            player = next(order)
            print(f"Ход игрока {player.nick}")
    except KeyboardInterrupt:
        print("Выход из игры..")


if __name__ == "__main__":
    main()
