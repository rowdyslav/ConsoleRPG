from itertools import cycle
from pathlib import Path
from typing import Annotated

import typer

from .engine import GameSession
from .equipment import load_equipment
from .errors import ConfigError, GameplayError
from .models import Player
from .registry import create_item_registry

APP = typer.Typer(help="Console RPG powered by TOML configs")


MOVE_TIP = (
    "Варианты хода:\n"
    "A - атака\n"
    "U - использовать расходник\n"
    "S - пропустить ход, восстановить 10% здоровья и 10% маны\n"
    "I - узнать свои данные (не завершает ход)\n"
)


def _ask_target_index(targets_count: int) -> int | None:
    raw = typer.prompt("Индекс цели").strip()
    if not raw.isdigit():
        typer.echo("Нужно ввести число")
        return None
    target_index = int(raw)
    if target_index < 0 or target_index >= targets_count:
        typer.echo("Неправильная цель атаки")
        return None
    return target_index


@APP.command()
def play(
    items: Annotated[Path, typer.Option(help="Path to items .toml")] = Path(
        "settings/items.toml",
    ),
    equip: Annotated[Path | None, typer.Option(help="Path to equipment .toml")] = None,
) -> None:
    """Start interactive game session."""
    try:
        nicknames = typer.prompt("Введите ники игроков через пробел").split()
        if len(nicknames) < 2:
            raise GameplayError(_ := "Нужно минимум 2 игрока")

        players = [Player.random(nick) for nick in nicknames]
        registry = create_item_registry(str(items))
        equipment = load_equipment(str(equip), players, registry) if equip else None

        session = GameSession(
            players=players,
            weapons=registry.weapons,
            action_weapons=registry.action_weapons,
            consumables=registry.consumables,
        )
        session.start(equipment)

        turns_order = cycle(players)
        player = next(turns_order)
        typer.echo(f"Ход игрока {player.nick}")

        while True:
            move = typer.prompt(MOVE_TIP)
            target_index = None
            if move and move[0].upper() == "A":
                targets = session.targets_for(player)
                for index, target in enumerate(targets):
                    typer.echo(f"{index}: {target.nick}")
                target_index = _ask_target_index(len(targets))
                if target_index is None:
                    continue

            result = session.make_move(player, move, target_index=target_index)
            typer.echo(result.message)
            if result.turn_ended:
                player = next(turns_order)
                typer.echo(f"Ход игрока {player.nick}")
    except KeyboardInterrupt:
        typer.echo("\nВыход из игры..")
    except (ConfigError, GameplayError, ValueError) as exc:
        typer.echo(f"Ошибка: {exc}", err=True)
        raise typer.Exit(code=1) from exc
