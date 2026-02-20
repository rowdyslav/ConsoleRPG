from __future__ import annotations

from dataclasses import dataclass
from random import Random

from .errors import GameplayError
from .models import ActionWeapon, Consume, Item, Player, Weapon


@dataclass(slots=True)
class MoveResult:
    message: str
    turn_ended: bool


class GameSession:
    def __init__(
        self,
        players: list[Player],
        weapons: list[Weapon],
        action_weapons: list[ActionWeapon],
        consumables: list[Consume],
        rng: Random | None = None,
    ) -> None:
        if len(players) < 2:
            raise GameplayError("A session requires at least two players")
        if not weapons and not action_weapons:
            raise GameplayError("At least one weapon is required")
        if not consumables:
            raise GameplayError("At least one consumable is required")

        self.players = players
        self.weapons = weapons
        self.action_weapons = action_weapons
        self.consumables = consumables
        self.rng = rng or Random()

    def start(self, equipment: dict[Player, dict[str, Item]] | None = None) -> None:
        for player in self.players:
            if equipment and player in equipment:
                player.weapon = equipment[player].get("weapon")  # type: ignore[assignment]
                player.consume = equipment[player].get("consume")  # type: ignore[assignment]
                continue

            player.weapon = self.rng.choice(self.weapons + self.action_weapons)
            player.consume = self.rng.choice(self.consumables)

    def targets_for(self, actor: Player) -> list[Player]:
        return [target for target in self.players if target is not actor]

    def attack(self, actor: Player, target_index: int) -> MoveResult:
        if actor.weapon is None:
            return MoveResult("Нет оружия для атаки!", False)
        if not actor.can_pay_mana(actor.weapon):
            return MoveResult(f"Недостаточно маны для атаки {actor.weapon.name}", False)

        targets = self.targets_for(actor)
        if target_index < 0 or target_index >= len(targets):
            return MoveResult("Неправильная цель атаки", False)

        target = targets[target_index]
        actor.mana -= actor.weapon.mana_cost
        target.hp = max(0, target.hp - actor.weapon.damage)
        actor.weapon.durability -= 1

        weapon_name = actor.weapon.name
        damage = actor.weapon.damage
        mana_cost = actor.weapon.mana_cost
        if actor.weapon.durability <= 0:
            actor.weapon = None

        message = (
            f"Атака {actor.nick} оружием {weapon_name} прошла успешно, "
            f"он теряет {mana_cost} маны! {target.nick} теряет {damage} хп!"
        )
        return MoveResult(message, True)

    def use_consume(self, actor: Player) -> MoveResult:
        if actor.consume is None:
            return MoveResult("Нету расходника для использования!", False)
        if not actor.can_pay_mana(actor.consume):
            return MoveResult(
                f"Недостаточно маны для использования {actor.consume.name}",
                False,
            )

        actor.mana -= actor.consume.mana_cost
        actor.restore(actor.consume.hp_regen, actor.consume.mana_regen)

        consume_name = actor.consume.name
        hp_regen = actor.consume.hp_regen
        mana_regen = actor.consume.mana_regen
        actor.consume.count -= 1
        if actor.consume.count <= 0:
            actor.consume = None

        return MoveResult(
            f"{actor.nick} использовал {consume_name}, "
            f"восстановив {hp_regen} хп и {mana_regen} маны",
            True,
        )

    def rest(self, actor: Player) -> MoveResult:
        hp_reg = max(1, actor.hp_max // 10)
        mana_reg = max(1, actor.mana_max // 10)
        actor.restore(hp_reg, mana_reg)
        return MoveResult(
            f"Игрок {actor.nick} решает отдохнуть, "
            f"восстанавливает {hp_reg} хп и {mana_reg} маны",
            True,
        )

    def info(self, actor: Player) -> MoveResult:
        weapon = actor.weapon.name if actor.weapon else "Нет"
        consume = f"{actor.consume.name} (еще {actor.consume.count})" if actor.consume else "Нет"
        message = (
            f"Ваш ник - {actor.nick}\n"
            f"ХП - {actor.hp} / {actor.hp_max}\n"
            f"Мана - {actor.mana} / {actor.mana_max}\n"
            f"Оружие - {weapon}\n"
            f"Расходник - {consume}"
        )
        return MoveResult(message, False)

    def make_move(
        self,
        actor: Player,
        move: str,
        target_index: int | None = None,
    ) -> MoveResult:
        if not move:
            return MoveResult("Неправильный ход!", False)

        action = move[0].upper()
        if action == "A":
            if target_index is None:
                return MoveResult("Нужно выбрать цель атаки", False)
            return self.attack(actor, target_index)
        if action == "U":
            return self.use_consume(actor)
        if action == "S":
            return self.rest(actor)
        if action == "I":
            return self.info(actor)
        return MoveResult("Неправильный ход!", False)
