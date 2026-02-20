from __future__ import annotations

from .config import load_mapping
from .errors import ConfigError
from .models import ActionWeapon, Consume, Item, Player, Weapon
from .registry import ItemRegistry


def _resolve_player(key: str, players: list[Player]) -> Player:
    if key.isdigit():
        idx = int(key)
        if idx < 0 or idx >= len(players):
            raise ConfigError(f"Player index out of range: {idx}")
        return players[idx]

    by_nick = {player.nick: player for player in players}
    player = by_nick.get(key)
    if player is None:
        raise ConfigError(f"Unknown player in equipment mapping: {key}")
    return player


def load_equipment(
    path: str,
    players: list[Player],
    registry: ItemRegistry,
) -> dict[Player, dict[str, Item]]:
    data = load_mapping(path)
    result: dict[Player, dict[str, Item]] = {}

    for key, slots in data.items():
        if not isinstance(key, str):
            raise ConfigError("Equipment key must be TOML table name (string)")
        if not isinstance(slots, dict):
            raise ConfigError("Equipment entry must be a mapping")

        player = _resolve_player(key, players)
        player_slots: dict[str, Item] = {}

        for slot, item_name in slots.items():
            if slot not in {"weapon", "consume"}:
                raise ConfigError(f"Unknown equipment slot: {slot}")
            if not isinstance(item_name, str):
                raise ConfigError("Equipment item name must be string")

            item = registry.find_item_by_name(item_name)
            if slot == "weapon" and not isinstance(item, (Weapon, ActionWeapon)):
                raise ConfigError(f"`{item_name}` is not a weapon")
            if slot == "consume" and not isinstance(item, Consume):
                raise ConfigError(f"`{item_name}` is not a consumable")
            player_slots[slot] = item

        result[player] = player_slots

    return result
