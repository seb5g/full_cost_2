from typing import Any

from dataclasses import dataclass
from collections.abc import Iterable
from pathlib import Path

import toml

from fullcoster.constants.entities import Entity, ENTITIES, EntityCategory, WUCategory
from fullcoster.utils.enum import BaseEnum


activity_config_path = Path(__file__).parent.parent.joinpath('resources/config_activities.toml')


@dataclass()
class Activity:
    activity_short: str
    activity_long: str
    wu: WUCategory
    wu_unit: Any
    wu_unity: float
    wu_label: str
    session_names: list[str]
    night: bool
    entities: Iterable[Entity]

    def get_entities_short(self):
        return (entity.short for entity in self.entities)

    def get_entities_name(self):
        return (entity.name for entity in self.entities)


ActivityCategory = BaseEnum(
    'ActivityCategory',
    [(key, val['name']) for key, val in toml.load(activity_config_path)['activities'].items()]
)

ACTIVITIES: dict[ActivityCategory, Activity] = {}


def check_entities_are_compatible(activity: str, entities: list[Entity]):
    wu = entities[0].wu
    for entity in entities:
        if entity.wu != wu:
            raise TypeError(f'The entities {[str(entity) for entity in entities]} grouped '
                            f'in the activity {activity} '
                            f'have no compatible working units')


for activity_short, activity_dict in toml.load(activity_config_path)['activities'].items():

    entities: list[Entity] = [ENTITIES[EntityCategory[entity]] for entity in activity_dict['entities']]
    check_entities_are_compatible(activity_short, entities)

    ACTIVITIES[ActivityCategory[activity_short]] = (
        Activity(activity_short,
                 activity_long=activity_dict['name'],
                 wu=WUCategory[entities[0].wu.category],  # to make sure the wu is within the possible options
                 wu_unit=activity_dict.get('wu_unit', 'day'),
                 wu_unity = activity_dict.get('wu_unity', 1),
                 wu_label=activity_dict.get('wu_label', 'Working Unit:'),
                 session_names=activity_dict.get('session_names', None),
                 night=activity_dict.get('night', False),
                 entities=entities
                 ))

activities_choices = [(ACTIVITIES[activity].activity_short,
                       ACTIVITIES[activity].activity_long,) for activity in ACTIVITIES]

def get_entities_ids_from_activity(act: ActivityCategory):
    return list(zip(
        ACTIVITIES[act].get_entities_short(),
        ACTIVITIES[act].get_entities_name()))


def get_entities_short_from_activity(act: ActivityCategory) -> list[str]:
    return ACTIVITIES[act].get_entities_short()


def get_entities_obj_from_activity(act: ActivityCategory) -> list[Entity]:
    return ACTIVITIES[act].entities


def get_activities_from_entity(entity_enum: EntityCategory) -> Iterable[ActivityCategory]:
    activities = []
    for activity in ACTIVITIES:
        for entity in ACTIVITIES[activity].entities:
            if entity.short == entity_enum.name:
                activities.append(activity)
    return activities


def get_activities_as_list() -> list[tuple[str, str]]:
    return activities_choices