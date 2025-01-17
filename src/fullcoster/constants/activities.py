from dataclasses import dataclass
from collections.abc import Iterable
from pathlib import Path

import toml

from fullcoster.constants.entities import Entity, ENTITIES, EntityCategory
from fullcoster.utils.enum import BaseEnum


activity_config_path = Path(__file__).parent.parent.joinpath('app_base/config_activities.toml')


@dataclass()
class Activity:
    activity_short: str
    activity_long: str
    entities: Iterable[Entity]

    def get_entities_short(self):
        return (entity.short for entity in self.entities)

    def get_entities_name(self):
        return (entity.name for entity in self.entities)


ActivityCategory = BaseEnum(
    'ActivityCategory',
    [(key, val['name']) for key, val in toml.load(activity_config_path)['activities'].items()]
)

ACTIVITIES = {}

for activity_short, activity_dict in toml.load(activity_config_path)['activities'].items():
    ACTIVITIES[ActivityCategory[activity_short]] = (
        Activity(activity_short,
                 activity_dict['name'],
                 entities=[
                     ENTITIES[EntityCategory[entity]] for entity in activity_dict['entities']
                 ]
                 ))

activities_choices = [(ACTIVITIES[activity].activity_short,
                       ACTIVITIES[activity].activity_long,) for activity in ACTIVITIES]

def get_entities_ids_from_activity(act: ActivityCategory):
    return list(zip(
        ACTIVITIES[act].get_entities_short(),
        ACTIVITIES[act].get_entities_name()))


def get_activities_from_entity(entity_enum: EntityCategory) -> Iterable[ActivityCategory]:
    activities = []
    for activity in ACTIVITIES:
        for entity in ACTIVITIES[activity].entities:
            if entity.short == entity_enum.name:
                activities.append(activity)
    return activities