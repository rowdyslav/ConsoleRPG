# Repository Guidelines

## Project Structure & Module Organization

- `main.py` is the executable entrypoint (`uv run main.py play`).
- Application code lives in `src/`:
  - `src/cli.py` Typer commands and interactive loop.
  - `src/engine.py` game mechanics and turn actions.
  - `src/models.py` domain models (`Player`, `Item`, etc.).
  - `src/registry.py`, `src/equipment.py`, `src/config.py` config loading and validation.
- Game configuration lives in `settings/` and is **TOML-only** (`items.toml`, `equip.toml`).

## Build and Development Commands

- `uv sync --extra dev` installs runtime + dev dependencies from `pyproject.toml`/`uv.lock`.
- `uv run main.py play` runs the game.
- `uv run ruff check .` runs linting.
- `uv lock` refreshes the lockfile after dependency changes.

## Coding Style & Naming Conventions

- Follow PEP 8 with 4-space indentation and type hints for public functions.
- Use `snake_case` for functions/variables/files, `PascalCase` for classes, and `UPPER_CASE` for constants.
- Keep game logic in `src/engine.py`; keep CLI-only concerns in `src/cli.py`.
- Prefer explicit return types for command helpers and engine actions.
- Keep imports grouped: standard library, third-party, local modules.

## Configuration Tips

- `settings/items.toml` is the source of truth for item generation.
- Supported top-level groups: `Weapon`, `ActionWeapon`, `Consume`.
- `$kws$` in item `name` resolves from table key (`BattleFury` -> `Battle Fury`).
