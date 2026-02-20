# Repository Guidelines

## Project Structure & Module Organization

- `main.py` is the CLI entrypoint and game loop.
- Core domain models live in `base_classes.py` (`Game`, `Player`, `Item`).
- Item subclasses are defined in `item_types.py`.
- YAML loaders are in `loaders/` (`items.py`, `equip.py`).
- Game data/config lives in `settings/` (`items.yml`, `equip.yml`).
- Keep new runtime modules at repo root or in `loaders/`; keep static data in `settings/`.

## Build, Test, and Development Commands

- `uv run main.py` runs the game locally
- `ruff check .` runs linting
- If dependencies are missing, install:
  -- `uv pip install -r pyproject.toml`

## Coding Style & Naming Conventions

- Follow PEP 8 with 4-space indentation and type hints for public functions.
- Use `snake_case` for functions/variables/files, `PascalCase` for classes, and `UPPER_CASE` for constants.
- Keep game logic methods small and focused (`Player.make_move`, loader helpers, etc.).
- Prefer explicit return types like `-> tuple[str, bool]` for action methods.
- Keep imports grouped: standard library, third-party, local modules.

## Configuration Tips

- Treat `settings/items.yml` as the source of truth for generated item instances.
- Validate YAML key names carefully; loader logic depends on expected item types (`Weapon`, `ActionWeapon`, `Consume`).
