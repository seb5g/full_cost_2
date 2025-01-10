from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def names(cls):
        return (elt.name for elt in cls)

    @classmethod
    def values(cls):
        return (elt.value for elt in cls)

    @classmethod
    def to_dict(cls):
        return {elt.name: elt.value for elt in cls}
