from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

from .errors import ConfigError


def _split_camel_case(raw: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", raw)


def load_mapping(path: str | Path) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        raise ConfigError(f"Config file not found: {file_path}")
    if file_path.suffix.lower() != ".toml":
        raise ConfigError("Only TOML configs are supported. Use .toml")

    with file_path.open("rb") as file:
        data = tomllib.load(file)

    if not isinstance(data, dict):
        raise ConfigError(f"Expected mapping at top-level in {file_path}")
    return data


def resolve_name(value: str, key_name: str) -> str:
    if value.strip() == "$kws$":
        return _split_camel_case(key_name)
    return value
