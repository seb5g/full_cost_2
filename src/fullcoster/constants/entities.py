from typing import Any, Union
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import toml

from fullcoster.utils.enum import BaseEnum


entity_config_path = Path(__file__).parent.parent.joinpath('app_base/config_entities.toml')


class PriceCategory(BaseEnum):
    T1 = 'CNRS Interne'
    T2 = 'CNRS Externe'
    T3 = 'Private'

    @classmethod
    def as_choices(cls):
        return [(price_enum.name, price_enum.value) for price_enum in cls]


@dataclass()
class WU:
    """ A description of the working unit of an entity to be instantiated from the WUCategory enum

    For instance, the Entity SPECTRO as a WU category of day and a def number of 0.5 because split activities in half
    days.

    Attributes
    ----------
    category: str
        One of the name of the WUCategory enum
    cat_quantity: float
        The quantity related to the category, usually one but could be 1/2 (half a day), 1/4 (quarter of a day),
         1 sample...
    cat_extra: Any
        Any extra argument required to define the WU, for instance for WUCategory.session, it could be a list of names
        to specify the number and name of the sessions
    """
    category: str
    cat_quantity: Union[float, Iterable[str]]
    cat_extra: dict = None


class WUCategory(BaseEnum):
    day = 1
    hour = 2
    sample = 3
    session = 4

    def to_wu(self,
              cat_quantity: Union[float, Iterable[str]],
              cat_extra=None,) -> WU:
        return WU(self.name, cat_quantity, cat_extra)


@dataclass()
class Entity:
    """ A class describing "something" related to a price in the full cost project"""
    name: str
    short: str
    prices: dict[PriceCategory, float]
    experiments: Iterable[str]
    wu: WU

    def get_prices(self):
        prices = []
        for price_enum in PriceCategory:
            prices.append((price_enum.name,
                           self.prices[price_enum],
                           self.short))
        return prices


EntityCategory = BaseEnum(
    'EntityCategory',
    [(key, val['name']) for key, val in toml.load(entity_config_path)['entities'].items()]
)

ENTITIES = {}

for entity_short, entity_dict in toml.load(entity_config_path)['entities'].items():
    ENTITIES[EntityCategory[entity_short]] = Entity(entity_dict['name'],
                                                    short=entity_short,
                                                    prices={PriceCategory.T1: entity_dict['T1'],
                                                            PriceCategory.T2: entity_dict['T2'],
                                                            PriceCategory.T3: entity_dict['T3'],},
                                                    experiments=entity_dict['experiments'],
                                                    wu=WUCategory[entity_dict['wu']].to_wu(
                                                        cat_quantity=entity_dict.get('wu_quantity', 1),
                                                        cat_extra=entity_dict.get('wu_extra', None)
                                                    ))

def get_entities_as_list() -> list[(str, str)]:
    return [(entity.name, entity.value) for entity in ENTITIES]