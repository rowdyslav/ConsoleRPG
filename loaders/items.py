import yaml
import re

from typing import Dict, Union, List
from base_classes import Item

from base_classes import Item
from item_types import ActionWeapon, Weapon, Consume


def _replace_config_values(config: Dict[str, Dict[str, Dict[str, Union[str, int]]]]):
    for item_type, items_list in config.items():
        for item_name, characteristics in items_list.items():
            for key, value in characteristics.items():
                if isinstance(value, str):
                    characteristics[key] = re.sub(
                        r"([a-z])([A-Z])", r"\1 \2", item_name
                    )
    return config


def create_item_classes(filename) -> Dict[str, List[Item]]:
    custom_item_classes = {}
    with open(filename, "r") as file:
        data = _replace_config_values(yaml.safe_load(file))
        for custom_item_parent, items_list in data.items():
            for item_name, characteristics in items_list.items():
                match custom_item_parent:
                    case "Weapon":
                        custom_item_cls = type(item_name, (Weapon,), characteristics)
                    case "ActionWeapon":
                        custom_item_cls = type(
                            item_name, (ActionWeapon,), characteristics
                        )
                    case "Consume":
                        custom_item_cls = type(item_name, (Consume,), characteristics)

                working_massive: List[type] = custom_item_classes.get(
                    custom_item_parent
                )
                if not working_massive:
                    custom_item_classes[custom_item_parent] = []
                custom_item_classes[custom_item_parent].append(custom_item_cls)

    return custom_item_classes
