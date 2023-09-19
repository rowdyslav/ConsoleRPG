from base_classes import Game, Player
from items import weapons, consumes
from itertools import cycle


def main():
    players = list(map(Player, input("Введите ники игроков через пробел -> ").split()))

    session = Game(players)

    for x in (0, 1):  # ##
        session.players[x].weapon = weapons.BattleFury()  # ##
        session.players[x].consume = consumes.FairyFire()  # ##

    mm = session.make_move
    move_tip = (
        "Варианты хода:\n"
        "A - атака\n"
        "U - использовать расходник\n"
        "S - пропустить ход, восстановить 10% здоровья и 10% маны\n"
        "I - узнать свои данные (не завершает ход)"
        "\n-> "
    )

    order = cycle(iter(players))
    player = next(order)
    print(f"Ход игрока {player.nick}")
    while True:
        message, move_end = mm(player, input(move_tip))
        while not move_end:
            print(message)
            message, move_end = mm(player, input(move_tip))
        print(message)
        player = next(order)
        print(f"Ход игрока {player.nick}")


if __name__ == "__main__":
    main()
