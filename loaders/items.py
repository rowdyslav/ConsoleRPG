import yaml
import re

from typing import Dict, List

from base_classes import Item
from item_types import ActionWeapon, Weapon, Consume


def _replace_config_values(config: Dict[str, Dict[str, Dict[str, str | int]]]):
    for item_type, items_list in config.items():
        for item_name, characteristics in items_list.items():
            for key, value in characteristics.items():
                if isinstance(value, str):
                    characteristics[key] = re.sub(
                        r"([a-z])([A-Z])", r"\1 \2", item_name
                    )
    return config


def create_item_classes(filename) -> Dict[str, List[Item]]:
    item_classes = {}
    with open(filename, "r") as file:
        data = _replace_config_values(yaml.safe_load(file))
        for item_parent, items_list in data.items():
            for item_name, characteristics in items_list.items():
                match item_parent:
                    case "Weapon":
                        item_class = type(item_name, (Weapon,), {})
                    case "ActionWeapon":
                        item_class = type(item_name, (ActionWeapon,), {})
                    case "Consume":
                        item_class = type(item_name, (Consume,), {})

                if not item_classes.get(item_parent):
                    item_classes[item_parent] = []

                item_classes[item_parent].append(item_class(**characteristics))  # type: ignore

    return item_classes
