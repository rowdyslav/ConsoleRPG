from __future__ import annotations

from dataclasses import dataclass

from .config import load_mapping, resolve_name
from .errors import ConfigError
from .models import ActionWeapon, Consume, Item, Weapon


@dataclass(slots=True)
class ItemRegistry:
    weapons: list[Weapon]
    action_weapons: list[ActionWeapon]
    consumables: list[Consume]

    def find_item_by_name(self, name: str) -> Item:
        for item in [*self.weapons, *self.action_weapons, *self.consumables]:
            if item.name == name:
                return item
        raise ConfigError(f"Item `{name}` was not found in registry")


def _as_int(mapping: dict[str, object], key: str, default: int = 0) -> int:
    value = mapping.get(key, default)
    if not isinstance(value, int):
        raise ConfigError(f"`{key}` must be int, got {type(value).__name__}")
    return value


def _as_str(mapping: dict[str, object], key: str, default: str) -> str:
    value = mapping.get(key, default)
    if not isinstance(value, str):
        raise ConfigError(f"`{key}` must be str, got {type(value).__name__}")
    return value


def create_item_registry(path: str) -> ItemRegistry:
    data = load_mapping(path)

    weapons: list[Weapon] = []
    action_weapons: list[ActionWeapon] = []
    consumables: list[Consume] = []

    for group_name, group_items in data.items():
        if not isinstance(group_name, str) or not isinstance(group_items, dict):
            raise ConfigError("Each top-level entry must be a named item group")

        for key_name, raw_item in group_items.items():
            if not isinstance(key_name, str) or not isinstance(raw_item, dict):
                raise ConfigError("Each item entry must be an object")

            item_name = resolve_name(_as_str(raw_item, "name", "$kws$"), key_name)
            mana_cost = _as_int(raw_item, "mana_cost", 0)

            if group_name == "Weapon":
                weapons.append(
                    Weapon(
                        name=item_name,
                        mana_cost=mana_cost,
                        damage=_as_int(raw_item, "damage", 1),
                        durability=_as_int(raw_item, "durab", _as_int(raw_item, "durability", 1)),
                    )
                )
            elif group_name == "ActionWeapon":
                action_weapons.append(
                    ActionWeapon(
                        name=item_name,
                        mana_cost=mana_cost,
                        damage=_as_int(raw_item, "damage", 1),
                        durability=_as_int(raw_item, "durab", _as_int(raw_item, "durability", 1)),
                        action_id=_as_str(raw_item, "action_id", ""),
                    )
                )
            elif group_name == "Consume":
                consumables.append(
                    Consume(
                        name=item_name,
                        mana_cost=mana_cost,
                        hp_regen=_as_int(raw_item, "hp_regen", 1),
                        mana_regen=_as_int(raw_item, "mana_regen", 0),
                        count=_as_int(raw_item, "count", 1),
                    )
                )
            else:
                raise ConfigError(f"Unknown item group: {group_name}")

    return ItemRegistry(weapons=weapons, action_weapons=action_weapons, consumables=consumables)
