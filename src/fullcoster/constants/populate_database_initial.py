import os
import codecs
import csv

from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fullcoster.full_cost.settings")

import django
django.setup()

from fullcoster.lab.models import Project, User, Group, Price, Gestionnaire
from fullcoster.utils.ldap import LDAP
from fullcoster.constants.activities import ACTIVITIES, ActivityCategory
from fullcoster.constants.entities import ENTITIES, PriceCategory


here = Path(__file__).parent

gest = [dict(last_name='Trupin', first_name='Mireille', email='mireille.trupin@cemes.fr', groups=[]),
        dict(last_name='Rougale', first_name='Muriel', email='muriel.rougalle@cemes.fr', groups=[]),
        dict(last_name='Melendo', first_name='Rose', email='rose-marie.melendo@cemes.fr', groups=[]),
        dict(last_name='Cardeilhac', first_name='Frédérique', email='frederique.cardeilhac@cemes.fr', groups=[]),
        dict(last_name='Viala', first_name='Christine', email='christine.viala@cemes.fr',
             groups=['NEO', 'MEM', 'M3', 'I3EM', 'PPM', 'SINANO', 'GNS']),
        ]

def populate_gestionnaire():
    for g in Gestionnaire.objects.all():
        g.delete()
    for g in gest:
        gg = Gestionnaire(last_name=g['last_name'],
                          first_name=g['first_name'],
                          email=g['email'])
        gg.save()
        print(gg)


def populate_project():
    for p in Project.objects.all():
        p.delete()
    with codecs.open(here.joinpath('project_pi.csv'), 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pi_surname = row[1].split(' ')[0]
            try:
                pi = User.objects.get(user_last_name__iexact=pi_surname)
            except:
                pi = User.objects.get(user_last_name='OTHER')
            p = Project(project_name=row[0].upper(), project_pi=pi)
            p.save()
            print(row)


def populate_users():
    for u in User.objects.all():
        u.delete()
    for g in Group.objects.all():
        g.delete()
    with codecs.open(here.joinpath('personnel.csv'), 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lgroup = get_group(row[0].upper())
            user = User(user_last_name=row[0].upper(), user_first_name=row[1].capitalize(), group=lgroup)
            user.save()
            print(row)
        user = User(user_last_name='OTHER', user_first_name='Name')
        user.save()


def get_gest_from_group(group):
    for g in gest:
        if group.upper() in g['groups']:
            return Gestionnaire.objects.get(last_name__iexact=g['last_name'])


def get_group(user):
    lgroup = None
    ldap = LDAP()
    group = ldap.get_group_ldap_last_name(user)
    if group is not None:
        g = Group.objects.filter(group__iexact=group['short'])
        if not g.exists():
            gest = get_gest_from_group(group['short'])
            lgroup = Group(group=group['short'].upper(),
                           description=group['long'],
                           gestionnaire=gest)
            lgroup.save()
        else:
            lgroup = g[0]
    return lgroup


def set_prices(prices, entity):
    for p in prices:
        billing = Price(price_category=p[0], price=p[1], price_name=p[2], price_entity=entity)
        billing.save()
        print(billing)


def populate_prices():
    for p in Price.objects.all():
        p.delete()
    for entity_enum in ENTITIES:
        prices = ENTITIES[entity_enum].get_prices()
        set_prices(prices, entity_enum.name)


if __name__ == '__main__':
    populate_users()
    populate_gestionnaire()
    populate_users()
    populate_prices()
    populate_project()


