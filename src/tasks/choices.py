from enum import Enum


class ChoiceEnumBase(Enum):
    @classmethod
    def choices(cls):
        return tuple([
            (enum.value, name) for name, enum in
            cls.__members__.items()
        ])


class ChoiceEnum(int, ChoiceEnumBase):
    pass


class Status(ChoiceEnum):
    Done = 1
    Undone = 0
