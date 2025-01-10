from dataclasses import dataclass
from collections.abc import Iterable

from full_cost.constants.entities import Entity, ENTITIES, EntityCategory
from full_cost.utils.enum import BaseEnum


@dataclass()
class Activity:
    activity_short: str
    activity_long: str
    entities: Iterable[Entity]

    def get_entities_short(self):
        return (entity.short for entity in self.entities)

    def get_entities_name(self):
        return (entity.name for entity in self.entities)


class ActivityCategory(BaseEnum):

    MET = 'Transmission Electron Microscopy Platform'
    PREPA = 'Sample Preparation Service'
    FIB_MEB = 'Focused Ion Beam and MEB'
    OSM = 'Optical Spectroscopy and Magnetism'
    CARAC = 'Material Characterisation'
    NANOFAB = 'NanoFabrication'
    CHEM = 'Chemistry'
    GROWTH_IMP = 'Growth and Implantation'
    STM_AFM = 'UHV Imagery'
    ENGINEERING = 'Engineering'

    def to_activity(self, entities: Iterable[Entity]) -> Activity:
        return Activity(self.name, self.value, entities)


ACTIVITIES = {
    ActivityCategory.MET:
             ActivityCategory.MET.to_activity(
                 entities=(
                     ENTITIES[EntityCategory.MET_C],
                     ENTITIES[EntityCategory.MET_A],
             )),
    ActivityCategory.PREPA:
        ActivityCategory.PREPA.to_activity(
            entities=(
                ENTITIES[EntityCategory.PREPA],
                ENTITIES[EntityCategory.PREPA_SOFT],
            )),
    ActivityCategory.FIB_MEB:
        ActivityCategory.FIB_MEB.to_activity(
            entities=(
                ENTITIES[EntityCategory.FIB_MEB],
            )),
    ActivityCategory.OSM:
        ActivityCategory.OSM.to_activity(
            entities=(
                ENTITIES[EntityCategory.SPECTRO],
                ENTITIES[EntityCategory.SPECTRO_CHEMISTRY],
                ENTITIES[EntityCategory.MAGNET],
            )),
    ActivityCategory.CARAC:
        ActivityCategory.CARAC.to_activity(
            entities=(
                ENTITIES[EntityCategory.MATC],
            )),
    ActivityCategory.NANOFAB:
        ActivityCategory.NANOFAB.to_activity(
            entities=(
                ENTITIES[EntityCategory.CLEANR],
                ENTITIES[EntityCategory.NEARF],
                ENTITIES[EntityCategory.FIB_LITHO],
            )),
    ActivityCategory.CHEM:
        ActivityCategory.CHEM.to_activity(
            entities=(
                ENTITIES[EntityCategory.CHEMISTRY],
            )),
    ActivityCategory.GROWTH_IMP:
        ActivityCategory.GROWTH_IMP.to_activity(
            entities=(
                ENTITIES[EntityCategory.GROWTH],
                ENTITIES[EntityCategory.IMPLANT],
                ENTITIES[EntityCategory.MAGNET],
            )),
    ActivityCategory.STM_AFM:
        ActivityCategory.STM_AFM.to_activity(
            entities=(
                ENTITIES[EntityCategory.DUFG],
                ENTITIES[EntityCategory.UHVI],
                ENTITIES[EntityCategory.LT4P],
            )),
    ActivityCategory.ENGINEERING:
        ActivityCategory.ENGINEERING.to_activity(
            entities=(
                ENTITIES[EntityCategory.MECA],
                ENTITIES[EntityCategory.ELEC],
            )),
}

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