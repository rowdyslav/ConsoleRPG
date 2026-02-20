# ConsoleRPG

A modern console RPG prototype on `Typer` with TOML-driven content.

## Stack
- Python `3.14+`
- `uv` for environment, locking, and runs
- `Typer` + `rich` for CLI UX
- TOML configs for game content

## Run

```bash
uv sync --extra dev
uv run main.py play
```

With explicit configs:

```bash
uv run main.py play --items settings/items.toml --equip settings/equip.toml
```

## Dev workflow (uv only)

```bash
uv lock
uv sync --extra dev
uv run ruff check .
```

## Config format (TOML only)

Items example:

```toml
[Weapon.BattleFury]
name = "$kws$"
damage = 10
durability = 5
```

Equipment example:

```toml
["0"]
weapon = "Battle Fury"

[rowdyslav]
consume = "Fairy Fire"
```
