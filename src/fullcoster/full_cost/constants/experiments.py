from .entities import ENTITIES
from .activities import ACTIVITIES



def populate_osp_experiments():
    from full_cost.osp.models import Experiment, sub_billings

    osp_experiments = [['Xplora', sub_billings[0][0]],
                       ['T64000', sub_billings[0][0]],
                       ['Visible', sub_billings[0][0]],
                       ['UV', sub_billings[0][0]],
                       ['Reflectivité', sub_billings[0][0]],
                       ['TERS', sub_billings[0][0]],
                       ['FLIM', sub_billings[0][0]],
                       ['Plasmonique quantique', sub_billings[0][0]],
                       ['Femto', sub_billings[0][0]],
                       ['UV (A125)', sub_billings[0][0]],
                       ['IR (A125)', sub_billings[0][0]],
                       ['Electrochimie (A125)', sub_billings[0][0]], ]
    for e in osp_experiments:
        exp = Experiment(experiment=e[0], exp_type=e[1])
        exp.save()
        print(e)

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
