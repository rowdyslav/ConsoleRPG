from itertools import cycle
from pathlib import Path
from typing import Annotated

import typer
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

from .engine import GameSession
from .equipment import load_equipment
from .errors import ConfigError, GameplayError
from .models import Player
from .registry import create_item_registry

APP = typer.Typer(no_args_is_help=True, help="Console RPG powered by Typer + TOML")
CONSOLE = Console()

MOVE_CHOICES = ["A", "U", "S", "I"]
MOVE_HINTS = {
    "A": "Атака",
    "U": "Использовать расходник",
    "S": "Пропуск хода и отдых",
    "I": "Показать информацию о себе",
}


def _render_player_panel(player: Player, active: bool) -> Panel:
    weapon = player.weapon.name if player.weapon else "Нет"
    consume = f"{player.consume.name} x{player.consume.count}" if player.consume else "Нет"

    body = Text()
    body.append(f"HP: {player.hp}/{player.hp_max}\n", style="green")
    body.append(f"Mana: {player.mana}/{player.mana_max}\n", style="cyan")
    body.append(f"Weapon: {weapon}\n", style="magenta")
    body.append(f"Consume: {consume}", style="yellow")

    border = "bright_green" if active else "dim"
    title = f"▶ {player.nick}" if active else player.nick
    return Panel(body, title=title, border_style=border)


def _show_battlefield(players: list[Player], active: Player) -> None:
    panels = [_render_player_panel(player, player is active) for player in players]
    CONSOLE.print(Columns(panels, equal=True, expand=True))


def _show_targets(targets: list[Player]) -> None:
    table = Table(title="Цели атаки")
    table.add_column("Индекс", justify="right", style="cyan")
    table.add_column("Игрок", style="bold")
    table.add_column("HP", justify="right", style="green")
    for index, target in enumerate(targets):
        table.add_row(str(index), target.nick, f"{target.hp}/{target.hp_max}")
    CONSOLE.print(table)


def _ask_target_index(targets_count: int) -> int | None:
    try:
        target_index = IntPrompt.ask("Индекс цели")
    except (KeyboardInterrupt, EOFError):
        raise
    except Exception:
        CONSOLE.print("Нужно ввести число", style="bold red")
        return None

    if target_index < 0 or target_index >= targets_count:
        CONSOLE.print("Неправильная цель атаки", style="bold red")
        return None
    return target_index


def _ask_move() -> str:
    move = Prompt.ask(
        "Ход [bold](A/U/S/I)[/bold]",
        choices=MOVE_CHOICES,
        default="I",
        show_choices=False,
    ).upper()
    CONSOLE.print(f"[dim]{MOVE_HINTS[move]}[/dim]")
    return move


def _ask_nicknames() -> list[str]:
    nicknames = Prompt.ask("Введите ники игроков через пробел").split()
    nicknames = [nick.strip() for nick in nicknames if nick.strip()]
    unique_nicknames = list(dict.fromkeys(nicknames))
    if len(unique_nicknames) < 2:
        raise GameplayError("Нужно минимум 2 уникальных игрока")
    return unique_nicknames


@APP.command()
def play(
    items: Annotated[Path, typer.Option(help="Path to items .toml")] = Path(
        "settings/items.toml"
    ),
    equip: Annotated[Path | None, typer.Option(help="Path to equipment .toml")] = None,
) -> None:
    """Start interactive game session."""
    try:
        CONSOLE.print(
            Panel(
                "[bold cyan]ConsoleRPG[/bold cyan]\n"
                "[dim]Typer + TOML build, later-ready for Textual migration[/dim]",
                border_style="cyan",
            )
        )

        nicknames = _ask_nicknames()
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

        while True:
            CONSOLE.rule(f"[bold green]Ход игрока {player.nick}[/bold green]")
            _show_battlefield(players, player)

            move = _ask_move()
            target_index = None
            if move == "A":
                targets = session.targets_for(player)
                _show_targets(targets)
                target_index = _ask_target_index(len(targets))
                if target_index is None:
                    continue

            result = session.make_move(player, move, target_index=target_index)
            CONSOLE.print(Panel(result.message, border_style="blue"))
            if result.turn_ended:
                player = next(turns_order)
    except (KeyboardInterrupt, EOFError):
        CONSOLE.print("\nВыход из игры..", style="bold yellow")
    except (ConfigError, GameplayError, ValueError) as exc:
        CONSOLE.print(f"Ошибка: {exc}", style="bold red")
        raise typer.Exit(code=1) from exc
