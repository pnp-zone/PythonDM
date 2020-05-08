import json

from dice import *

class Character(object):

    __slots__ = [
                "name",
                "max_hp",
                "hp",
                "ac",
                "str",
                "dex",
                "con",
                "int",
                "wis",
                "cha"
            ]

    __defaults__ = {
            "ac": 10,
            "str": 0,
            "dex": 0,
            "con": 0,
            "int": 0,
            "wis": 0,
            "cha": 0
            }

    def __init__(self, name, sheet=None, **kwargs):
        self.name = name

        if sheet is not None:
            with open(sheet) as f:
                sheet = json.load(f)
            sheet.update(kwargs)
        else:
            sheet = kwargs

        for key, value in sheet.items():
            self.__setattr__(key, value)

        if isinstance(self.max_hp, str):
            self.max_hp = eval(self.max_hp)
        self.hp = self.max_hp

    def __getattr__(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError as e:
            if e.args == (key,) and key in Character.__defaults__:
                return Character.__defaults__[key]
            else:
                raise e

    @property
    def _global_name(self):
        return self.name.lower().replace(" ", "_")

    def _roll_initiative(self):
        self.initiative = d20 + self.dex

    def __repr__(self):
        return f"{self.name} ({self.hp} / {self.max_hp})"