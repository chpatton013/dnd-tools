#!/usr/bin/env python3

import argparse
import enum
import math
import random

"""
Damage calculation helper for my new Paladin, Thursday.
He rolls a lot of dice, and that's hard to keep track of.
"""


class Paladin:
    def __init__(self, name, level=0, weapons=[]):
        self.name = name
        self.level = level
        self.weapons = {weapon.name: weapon for weapon in weapons}

    def damage(self, weapon_name, crit, smite=None):
        weapon_damage = self.weapons[weapon_name].damage(crit)

        smite_damage = {}

        if self.level >= 11:
            smite_damage.setdefault(
                DamageType.RADIANT,
                Damage(DamageType.RADIANT),
            ).merge(Damage(DamageType.RADIANT, dice={Die.D8: 1}))

        if smite:
            smite_damage.setdefault(
                DamageType.RADIANT,
                Damage(DamageType.RADIANT),
            ).merge(Damage(DamageType.RADIANT, dice={Die.D8: 1 + smite}))

        if crit:
            for damage in smite_damage.values():
                for die in damage.dice.keys():
                    damage.dice[die] *= 2

        total_damage = {}
        for type, damage in weapon_damage.items():
            total_damage.setdefault(type, Damage(type)).merge(damage)
        for type, damage in smite_damage.items():
            total_damage.setdefault(type, Damage(type)).merge(damage)
        return total_damage


class Weapon:
    def __init__(self, name, damages=[], crit_dice_multiplier=2):
        self.name = name
        self.damages = damages
        self.crit_dice_multiplier = crit_dice_multiplier

    def damage(self, crit):
        damages = {}

        for damage in self.damages:
            damages.setdefault(damage.type, Damage(damage.type)).merge(damage)

        if crit:
            for damage in damages.values():
                for die in damage.dice.keys():
                    damage.dice[die] *= self.crit_dice_multiplier

        return damages


class Damage:
    def __init__(self, type, dice=None, base=0):
        self.type = type
        self.dice = dice if dice else {}
        self.base = base

    def __str__(self):
        as_str = "+".join([
            f"{count}{die}" for die, count in self.dice.items()
            ])
        if self.base > 0:
            as_str += f"+{self.base}"
        return as_str

    def expected(self):
        total = self.base
        for die, count in self.dice.items():
            total += sum(die.expected for _ in range(count))
        return total

    def roll(self):
        total = self.base
        for die, count in self.dice.items():
            total += sum(die.roll() for _ in range(count))
        return total

    def merge(self, other):
        if self.type != other.type:
            raise ValueError()

        self.base += other.base
        for die, count in other.dice.items():
            self.dice.setdefault(die, 0)
            self.dice[die] += count


class DamageType(enum.Enum):
    SLASHING = "slashing"
    PIERCING = "piercing"
    BLUDGEONING = "bludgeoning"
    POISON = "poison"
    ACID = "acid"
    FIRE = "fire"
    COLD = "cold"
    RADIANT = "radiant"
    NECROTIC = "necrotic"
    LIGHTNING = "lightning"
    THUNDER = "thunder"
    FORCE = "force"
    PSYCHIC = "psychic"

    def __str__(self):
        return self.value


class Die(enum.Enum):
    D4 = 4
    D6 = 6
    D8 = 8
    D10 = 10
    D12 = 12
    D20 = 20
    D100 = 100

    def __str__(self):
        return f"d{self.value}"

    @property
    def expected(self):
        return (self.value + 1) / 2

    def roll(self):
        return random.randint(1, self.value)


MJOLNIR_1H = Weapon(
    "Mjolnir-1H",
    damages=[
        Damage(DamageType.BLUDGEONING, base=7, dice={Die.D8: 1}),
    ],
)

MJOLNIR_2H = Weapon(
    "Mjolnir-2H",
    damages=[
        Damage(DamageType.BLUDGEONING, base=5, dice={Die.D10: 1}),
    ],
)

STORMBREAKER_1H = Weapon(
    "Stormbreaker-1H",
    damages=[
        Damage(DamageType.SLASHING, base=7, dice={Die.D8: 1}),
        Damage(DamageType.LIGHTNING, dice={Die.D4: 1}),
    ],
    crit_dice_multiplier=3,
)

STORMBREAKER_2H = Weapon(
    "Stormbreaker-2H",
    damages=[
        Damage(DamageType.SLASHING, base=5, dice={Die.D10: 1}),
        Damage(DamageType.LIGHTNING, dice={Die.D4: 1}),
    ],
    crit_dice_multiplier=3,
)

THURSDAY = Paladin(
    "Thursday",
    level=12,
    weapons=[MJOLNIR_1H, MJOLNIR_2H, STORMBREAKER_1H, STORMBREAKER_2H],
)


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("weapon_name", choices=[weapon for weapon in THURSDAY.weapons])
    parser.add_argument("--crit", action="store_true", default=False)
    parser.add_argument("--smite", choices=[1, 2, 3], type=int)
    parser.add_argument("--roll", action="store_true", default=False)
    return parser.parse_args()


def main():
    args = parse_args()

    damage_types = THURSDAY.damage(args.weapon_name, args.crit, args.smite)

    total_rolled_damage = 0
    total_expected_damage = 0
    for type, damage in damage_types.items():
        rolled_damage = damage.roll()
        total_rolled_damage += rolled_damage

        expected_damage = damage.expected()
        total_expected_damage += expected_damage

        if args.roll:
            print(f"{damage} ({expected_damage}) {type} damage = {rolled_damage}")
        else:
            print(f"{damage} ({expected_damage}) {type} damage")
    if args.roll:
        print(f"TOTAL ({total_expected_damage}) damage = {total_rolled_damage}")
    else:
        print(f"TOTAL ({total_expected_damage}) damage")


if __name__ == "__main__":
    main()
