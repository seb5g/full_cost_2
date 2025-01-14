from typing import Iterable, Any
from dataclasses import dataclass


from ..utils.enum import BaseEnum


class PriceCategory(BaseEnum):
    T1 = 'CNRS Interne'
    T2 ='CNRS Externe'
    T3 = 'Private'

    @classmethod
    def as_choices(cls):
        return [(price_enum.name, price_enum.value) for price_enum in cls]


@dataclass()
class UO:
    """ A description of the working unit of an entity to be instantiated from the UOCategory enum

    For instance, the Entity SPECTRO as a UO category of day and a def number of 0.5 because split activities in half
    days.

    Attributes
    ----------
    category: str
        One of the name of the UOCategory enum
    cat_quantity: float
        The quantity related to the category, usually one but could be 1/2 (half a day), 1/4 (quarter of a day),
         1 sample...
    cat_extra: Any
        Any extra argument required to define the UO, for instance for UOCategory.session, it could be a list of names
        to specify the number and name of the sessions
    """
    category: str
    cat_quantity: float
    cat_extra: Any = None


class UOCategory(BaseEnum):
    day = 1
    hour = 2
    sample = 3
    session = 4

    def to_uo(self,
              cat_quantity: float,
              cat_extra=None,) -> UO:
        return UO(self.name, cat_quantity, cat_extra)


@dataclass()
class Entity:
    """ A class describing "something" related to a price in the full cost project"""
    name: str
    short: str
    prices: dict[PriceCategory, float]
    experiments: Iterable[str]
    uo: UO

    def get_prices(self):
        prices = []
        for price_enum in PriceCategory:
            prices.append((price_enum.name,
                           self.prices[price_enum],
                           self.short))
        return prices



class EntityCategory(BaseEnum):
    MET_C = 'Conventionnal TEM'
    MET_A = 'Advanced TEM'

    PREPA = 'Preparation for MET and MEB'
    PREPA_SOFT = 'Soft Matter Preparation'

    FIB_MEB = 'FIB Preparation and MEB'

    SPECTRO = 'Optical Spectroscopy'
    SPECTRO_CHEMISTRY = 'Optical Spectroscopy for Chemistry'
    MAGNET = 'Magnetic Properties'

    MEBA = 'Advanced MEB'

    MATC = 'Material Caracterisation'

    CLEANR = 'Clean Room Processes'
    NEARF = 'Near-field microscopy'
    FIB_LITHO = 'Lithography using the ZEISS'

    CHEMISTRY = 'Chemistry'

    UHVI = 'UHV Imagery'
    DUFG = 'Growth DUF'
    LT4P = 'LT-UHV 4 tips'

    GROWTH = 'Growth'
    IMPLANT = 'Ionic Implantation'

    MECA = 'Mechanic Service'
    ELEC = 'Electronic Service'

    def to_entity(self,
                  prices: dict[PriceCategory, float],
                  experiments: Iterable[str],
                  uo: UO) -> Entity:
        return Entity(self.name, self.value, prices, experiments, uo)


ENTITIES = {
    EntityCategory.MET_C:
        EntityCategory.MET_C.to_entity(
            prices={
                PriceCategory.T1: 247.,
                PriceCategory.T2: 1066.,
                PriceCategory.T3: 1333.,},
            experiments=('JEOL',
                         'CM20FEG',
                         'FemtoTEM',
                         'JEOL 2100',
                         'HF2000',
                         ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.MET_A:
        EntityCategory.MET_A.to_entity(
            prices={
                PriceCategory.T1: 81.,
                PriceCategory.T2: 976.,
                PriceCategory.T3: 1121., },
            experiments=('Technai',
                         'I2TEM',
                         'HC-IUMI',
                         ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.PREPA:
        EntityCategory.PREPA.to_entity(
            prices={
                PriceCategory.T1: 119.,
                PriceCategory.T2: 1366.,
                PriceCategory.T3: 1708., },
            experiments=('PIPS',
                         'PIPS II',
                         'Tripod',
                         'Electro-polishing',
                         'Electro-erosion',
                         'Other',
                         ),
            uo=UOCategory.sample.to_uo(cat_quantity=1),
        ),
    EntityCategory.PREPA_SOFT:
        EntityCategory.PREPA_SOFT.to_entity(
            prices=
            {PriceCategory.T1: 119.,
             PriceCategory.T2: 1366.,
             PriceCategory.T3: 1708., },
            experiments=('Soft Matter',
                         ),
            uo=UOCategory.sample.to_uo(cat_quantity=1),
        ),
    EntityCategory.FIB_MEB:
        EntityCategory.FIB_MEB.to_entity(
            prices={
                PriceCategory.T1: 202.,
                PriceCategory.T2: 341.,
                PriceCategory.T3: 426., },
            experiments=('EBSD/HELIOS',
                         'EDS/HELIOS',
                         'FIB/HELIOS',
                         'SEM/HELIOS',
                         'TEM Preparation/HELIOS',
                         'FIB/ZEISS',
                         'SEM/ZEISS',
                         ),
            uo=UOCategory.session.to_uo(cat_quantity=4,
                                        cat_extra=['Morning', 'AfterNoon', 'Evening', 'Night']),
        ),
    EntityCategory.SPECTRO:
        EntityCategory.SPECTRO.to_entity(
            prices={
                PriceCategory.T1: 130.,
                PriceCategory.T2: 419.,
                PriceCategory.T3: 524., },
            experiments=('Xplora',
                         'T64000',
                         'Visible',
                         'UV',
                         'Reflectivité',
                         'TERS',
                         'FLIM',
                         'Plasmonique quantique',
                         'Femto',
                         'Micro-Moke',
                         'Macro-Moke',
                         'µ-scope IR',
                         'Stationnary Waves',
                         ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5, cat_extra={'night': True}),
        ),
    EntityCategory.SPECTRO_CHEMISTRY:
        EntityCategory.SPECTRO_CHEMISTRY.to_entity(
            prices={
                PriceCategory.T1: 130.,
                PriceCategory.T2: 419.,
                PriceCategory.T3: 524., },
            experiments=('UV (A125)',
                         'IR (A125)',
                         'Electrochimie (A125)',
                         ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.MAGNET:
        EntityCategory.MAGNET.to_entity(
            prices={
                PriceCategory.T1: 130.,
                PriceCategory.T2: 419.,
                PriceCategory.T3: 524., },
            experiments=('Magneto-transport',),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.MATC:
        EntityCategory.MATC.to_entity(
            prices={
                PriceCategory.T1: 66.,
                PriceCategory.T2: 358.,
                PriceCategory.T3: 448., },
            experiments=(
                'RX-D8 Advance',
                'RX-D8 Discover',
                'Traction ',
                'Fluage',
                'Powder-ATD/ATG',
                'Powder-Adsorption Gaz',
                'Powder-Titrimétrie',
                'Powder-DLS',
                'Powder-Zetamétrie',
                'Powder-Granulométrie Laser',
                'Powder-Réfractométrie',
                'Powder-Spectrofluorométrie',
                'Powder-Sonde Puissance',
                'Powder-Préparation Echantillon (A121)',
                'Powder-Pycnométrie',
                'Powder-Binoculaire',
                'Powder-Electrochimie',
                'Powder-Fours à Moufle',
                'Powder-Fours tubulaires',
                'Powder-Etuves',
                'Powder-Chaine conductimétrique',
                'Powder-Chaine ionométrique',
                'Powder-Dosage métaux (voltamétrie)',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.CLEANR:
        EntityCategory.CLEANR.to_entity(
            prices={
                PriceCategory.T1: 281.,
                PriceCategory.T2: 652.,
                PriceCategory.T3: 815., },
            experiments=(
                'CR-Laser lithography',
                'CR-Photolithography',
                'CR-Physical Vapor Deposition - sputtering',
                'CR-Physical Vapor Deposition - ebeam',
                'CR-Plasma etching - RIE',
                'CR-Ion beam etching',
                'CR-Chemistry (wet etching, surface treatments)',
                'CR-Electrical Characterizations',
                'CR-Mechanical profilometer',
                'CR-DUS',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.NEARF:
        EntityCategory.NEARF.to_entity(
            prices={
                PriceCategory.T1: 281.,
                PriceCategory.T2: 652.,
                PriceCategory.T3: 815., },
            experiments=(
                'D3000'
                'D3100-STMLE',
                'Multimode',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.FIB_LITHO:
        EntityCategory.CLEANR.to_entity(
            prices={
                PriceCategory.T1: 281.,
                PriceCategory.T2: 652.,
                PriceCategory.T3: 815.,},
            experiments=(
                'Lithography/ZEISS'
            ),
            uo=UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.CHEMISTRY:
        EntityCategory.CHEMISTRY.to_entity(
            prices={
                PriceCategory.T1: 95.,
                PriceCategory.T2: 149.,
                PriceCategory.T3: 186.,},
            experiments=(
                'Labo 103',
                'Labo 105',
                'Labo 107',
                'Labo 109',
                'Labo 115',
                'Labo 117',
                'Labo 119',
                'Labo 121',
                'Labo 121 Four à gaz réduction',
                'Labo 123',
                'Labo 127',
                'P007 boite à gants',
            ),
            uo = UOCategory.day.to_uo(cat_quantity=0.5),
        ),
    EntityCategory.GROWTH:
        EntityCategory.GROWTH.to_entity(
            prices={
                PriceCategory.T1: 122.,
                PriceCategory.T2: 219.,
                PriceCategory.T3: 274., },
            experiments=(
                'Growth Plassys',
                'Growth Mantis',
                'Four',
                'Four RTA',
            ),
            uo=UOCategory.hour.to_uo(cat_quantity=1, cat_extra={'at_least': 1}),
        ),
    EntityCategory.IMPLANT:
        EntityCategory.GROWTH.to_entity(
            prices={
                PriceCategory.T1: 232.,
                PriceCategory.T2: 2958.,
                PriceCategory.T3: 3698., },
            experiments=(
                'Implantation',
            ),
            uo=UOCategory.hour.to_uo(cat_quantity=1, cat_extra={'at_least': 1}),
        ),
    EntityCategory.UHVI:
        EntityCategory.UHVI.to_entity(
            prices={
                PriceCategory.T1: 413.,
                PriceCategory.T2: 540.,
                PriceCategory.T3: 676., },
            experiments=(
                'DUF-RT STM/AFM Maintenance',
                'DUF-RT STM/AFM Sample/Spectroscopy',
                'DUF-VT STM/AFM Maintenance',
                'DUF-VT STM/AFM Sample/Spectroscopy',
                'LT-UHV-STM/Qplus Maintenance',
                'LT-UHV-STM/Qplus Sample preparation',
                'LT-UHV-STM/Qplus Imagery/Spectroscopy',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=1,),
        ),
    EntityCategory.DUFG:
        EntityCategory.DUFG.to_entity(
            prices={
                PriceCategory.T1: 413.,
                PriceCategory.T2: 540.,
                PriceCategory.T3: 676., },
            experiments=(
                'DUF-Ion Source Maintenance',
                'DUF-Ion Source Ion deposition',
                'DUF-MBE Growth Maintenance',
                'DUF-MBE Growth Sample Growth',
                'DUF-Preparation Maintenance',
                'DUF-Preparation Sample/Tip preparation',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=1, ),
        ),
    EntityCategory.LT4P:
        EntityCategory.LT4P.to_entity(
            prices={
                PriceCategory.T1: 1166.,
                PriceCategory.T2: 1459.,
                PriceCategory.T3: 1824., },
            experiments=(
                'LT-UHV-4STM SEM Maintenance',
                'LT-UHV-4STM SEM Sample preparation',
                'LT-UHV-4STM SEM Spectroscopy',
                'LT-UHV-4STM SEM Topography',
                'LT-UHV-4STM SEM Atom-Manipulation',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=1, ),
        ),
    EntityCategory.MECA:
        EntityCategory.MECA.to_entity(
            prices={
                PriceCategory.T1: 247.,
                PriceCategory.T2: 1066.,
                PriceCategory.T3: 1333., },
            experiments=(
                'ABEILHOU Pierre',
                'GATTI Bertrand',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=1/2, ),
        ),
    EntityCategory.ELEC:
        EntityCategory.ELEC.to_entity(
            prices={
                PriceCategory.T1: 81.,
                PriceCategory.T2: 976.,
                PriceCategory.T3: 1121., },
            experiments=(
                'PERTEL Christian',
                'LASFAR Abdelouahed',
            ),
            uo=UOCategory.day.to_uo(cat_quantity=1, ),
        ),
}


def get_entities_as_list() -> list[(str, str)]:
    return [(entity.name, entity.value) for entity in ENTITIES]