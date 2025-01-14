import os
import codecs
import csv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "full_cost.settings")

import django
django.setup()

from lab.models import Project, User, Group, Price, Gestionnaire
from full_cost.utils.ldap import LDAP
from full_cost.constants.activities import ACTIVITIES, ActivityCategory
from full_cost.constants.entities import ENTITIES, PriceCategory

gest = [dict(last_name='Trupin', first_name='Mireille', email='mireille.trupin@cemes.fr', groups=[]),
        dict(last_name='Rougale', first_name='Muriel', email='muriel.rougalle@cemes.fr', groups=[]),
        dict(last_name='Melendo', first_name='Rose', email='rose-marie.melendo@cemes.fr', groups=[]),
        dict(last_name='Cardeilhac', first_name='Frédérique', email='frederique.cardeilhac@cemes.fr', groups=[]),
        dict(last_name='Viala', first_name='Christine', email='christine.viala@cemes.fr',
             groups=['NEO', 'MEM', 'M3', 'I3EM', 'PPM', 'SINANO', 'GNS']),
        ]

def populate_gestionnaire():
    for g in gest:
        gg = Gestionnaire(last_name=g['last_name'], first_name=g['first_name'], email=g['email'])
        gg.save()
        print(gg)


def populate_project():
    with codecs.open('./project_pi.csv', 'r', 'utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pi_surname = row[1].split(' ')[0]
            try:
                pi = User.objects.get(user_last_name__iexact=pi_surname)
            except:
                pi = User.objects.get(user_last_name='OTHER')
            p = Project(project_name=row[0].upper(), project_pi=pi, pricing=row[2])
            p.save()
            print(row)

def populate_users():
    with codecs.open('./personnel.csv', 'r', 'utf-8') as csvfile:
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
        if group in g['groups']:
            return Gestionnaire.objects.get(last_name__iexact=g['last_name'])


def get_group(user):
    lgroup = None
    ldap = LDAP()
    group = ldap.get_group_ldap_last_name(user)
    if group is not None:
        g = Group.objects.filter(group__iexact=group['short'])
        if not g.exists():
            gest = get_gest_from_group(group['short'])
            lgroup = Group(group=group['short'].upper(), description=group['long'], gestionnaire=gest)
            lgroup.save()
        else:
            lgroup = g[0]
    return lgroup


def populate_osm_experiments():
    from osp.models import Experiment
    entities = ACTIVITIES[ActivityCategory.OSM]
    for entity in entities:
        for exp_ent in entity.experiments:
            exp = Experiment(experiment=exp_ent, exp_type=entity.short)
            exp.save()
            print(exp_ent)

def populate_mphys_experiments():
    from full_cost.mphys.models import Experiment, sub_billings
    exps = ['ATD/ATG', 'Adsorption Gaz', 'Titrimétrie','DLS', 'Zetamétrie',
    'Granulométrie Laser', 'Réfractométrie', 'Spectrofluorométrie',
    'Sonde Puissance', 'Préparation Echantillon (A121)', 'Pycnométrie',
    'Binoculaire', 'Electrochimie', 'Fours à Moufle', 'Fours tubulaires','Etuves',]

    mphys_experiments = [['PPMS', sub_billings[0][0]],
                       ['RX-D8 Advance', sub_billings[1][0]],
                         ['RX-D8 Discover', sub_billings[1][0]],
                       ['MEB', sub_billings[1][0]],
                       ['Traction', sub_billings[1][0]],
                       ['Fluage', sub_billings[1][0]],]

    for exp in exps:
        mphys_experiments.append([f'Powder-{exp}', sub_billings[1][0]])
    for e in mphys_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_chem_experiments():
    from full_cost.chem.models import Experiment, sub_billings

    chem_experiments = [['A103', sub_billings[0][0]],
                       ['A105', sub_billings[0][0]],
                       ['A107', sub_billings[0][0]],
                       ['A109', sub_billings[0][0]],
                       ['A115', sub_billings[0][0]],
                       ['A117', sub_billings[0][0]],
                        ['A123', sub_billings[0][0]],
                        ['A127', sub_billings[0][0]],
                        ['P003 MW', sub_billings[0][0]],
                        ['P007 BG', sub_billings[0][0]],
                        ['A121', sub_billings[0][0]],
                        ['A119', sub_billings[0][0]],]

    for e in chem_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_fab_experiments():
    from full_cost.fab.models import Experiment, sub_billings
    CR_exps = ['Laser lithography', 'Photolithography', 'Physical Vapor Deposition - sputtering',
    'Physical Vapor Deposition - ebeam', 'Plasma etching - RIE', 'Ion beam etching',
    'Chemistry (wet etching, surface treatments)', 'Electrical Characterizations', 'Mechanical profilometer']

    G_exps = ['Growth', 'Four', 'Four RTA']

    fab_experiments = [(f'GI-{exp}', sub_billings[2][0]) for exp in G_exps]
    fab_experiments.append(('GI-Implantation', sub_billings[3][0]))
    fab_experiments.append(('DUF Growth', sub_billings[1][0]))
    fab_experiments.extend([(f'CR-{exp}', sub_billings[0][0]) for exp in CR_exps])

    for e in fab_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_imag_experiments():
    from full_cost.imag.models import Experiment, sub_billings

    imag_experiments = [['LT-UHV', sub_billings[0][0]],
                       ['DUF RT', sub_billings[0][0]],
                       ['DUF VT', sub_billings[0][0]],
                       ['LT-4tips', sub_billings[1][0]],
                       ['Multimode', sub_billings[2][0]],
                       ['D3000', sub_billings[2][0]],
                        ['D3100-STMLE', sub_billings[2][0]],]

    for e in imag_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

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


def populate_fib_experiments():
    from full_cost.fib.models import Experiment, sub_billings, fibs

    fib_experiments = [['TEM Preparation', sub_billings[0][0], fibs[0][0]],
                       ['FIB', sub_billings[0][0], fibs[0][0]],
                       ['SEM', sub_billings[1][0], fibs[0][0]],
                       ['EDS', sub_billings[1][0], fibs[0][0]],
                       ['EBSD', sub_billings[1][0], fibs[0][0]],
                       ['SEM', sub_billings[1][0], fibs[1][0]],
                       ['Lithography', sub_billings[1][0], fibs[1][0]],
                       ['FIB', sub_billings[2][0], fibs[1][0]], ]

    for e in fib_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1], fib_name=e[2])
        exp.save()
        print(e)


def populate_engi_experiments():
    from full_cost.engi.models import Experiment, sub_billings
    from full_cost.lab.models import User
    elec_people = ['pertel', 'Lasfar']
    meca_people = ['Abeilhou', 'Auriol', 'Gatti']

    engi_experiments = [(User.objects.get(user_last_name__iexact=p), sub_billings[1][0],) for p in elec_people]
    engi_experiments.extend([(User.objects.get(user_last_name__iexact=p), sub_billings[0][0],) for p in meca_people])

    for e in engi_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_prepa_experiments():
    from full_cost.prepa.models import Experiment, sub_billings

    prep_experiments = [['PIPS', sub_billings[0][0]],
                       ['Tripod', sub_billings[0][0]],
                       ['Electropolishing', sub_billings[0][0]],
                       ['MEB', sub_billings[0][0]],
                       ['Other', sub_billings[0][0]],
                       ['Soft Matter', sub_billings[2][0]],
                       ]

    for e in prep_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

def populate_met_experiments():
    from full_cost.met.models import Experiment, sub_billings

    prep_experiments = [['JEOL', sub_billings[0][0]],
                       ['CM20 FEG', sub_billings[0][0]],
                       ['HF2000', sub_billings[0][0]],
                       ['CM30', sub_billings[0][0]],
                       ['TECNAI', sub_billings[1][0]],
                       ['I2TEM', sub_billings[1][0]],]

    for e in prep_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

if __name__ == '__main__':
    pass
    # populate_fib_experiments()
    # populate_osp_experiments()
    # populate_prepa_experiments()
    # populate_met_experiments()
    # populate_mphys_experiments()
    # populate_fab_experiments()
    #populate_engi_experiments()
    # populate_chem_experiments()
    # populate_imag_experiments()

    #populate_gestionnaire()
    #populate_prices()
    #populate_users()
    populate_project()


