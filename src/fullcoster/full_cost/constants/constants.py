"""
CEMES organisation
People enter their working units per activity => one database per activity
Admins make an invoice per facturation => one bill use entries possibly from various databases or an inset of databases
"""

#
#
# def get_activities_from_entity(entity):
#     if entity == '':
#         return list(ACTIVITIES.keys())
#     else:
#         billings = [d['entity'][0] for d in BILLINGS]
#         ind = billings.index(entity)
#         return BILLINGS[ind]['activities']
#
# def get_entity_long(entity):
#     billings = [d['entity'][0] for d in BILLINGS]
#     ind = billings.index(entity)
#     return BILLINGS[ind]['entity'][1]
#
# def get_subbillings_from_entity_short(entity):
#     billings = [d['entity'][0] for d in BILLINGS]
#     ind = billings.index(entity)
#     return [d['short'] for d in BILLINGS[ind]['related_subbillings']]
#
# def get_subbillings_from_entity_long(entity):
#     billings = [d['entity'][0] for d in BILLINGS]
#     ind = billings.index(entity)
#     return [d['long'] for d in BILLINGS[ind]['related_subbillings']]
#
# def get_billings_from_activity(activity):
#     billings = []
#     for bill in BILLINGS:
#         if activity in bill['activities']:
#             billings.append(activity)
#
# def get_billing_entities_as_list():
#     return [bill['entity'] for bill in BILLINGS]