import argparse

from fullcoster.lab.management import manage_apps, populate_database_initial

parser = argparse.ArgumentParser(
                    prog='ManageFullCost',
                    description='Manage FullCost application given the configured activities',
                    epilog='')
subparsers = parser.add_subparsers(help='subcommand help', dest='subcommand')

parser_activities = subparsers.add_parser('activities')
parser_activities.add_argument('function', type=str, help='Allow to call one of the function from manage_apps')
parser_activities.add_argument('--activities', type=str, nargs='*', help='List of activities')

parser_database = subparsers.add_parser('populate')
parser_database.add_argument('table', type=str, help='Populate tables in the database from constants')


def exec_from_command():

    parsed = parser.parse_args()
    print(f'parser is: {parser}')
    print(f'parsed arguments are: {parsed}')
    print(f'parsed subcommand is: {parsed.subcommand }')

    if parsed.subcommand == 'activities':
        print(f'parsed activities command is: {parsed.function}')
        if parsed.function == 'create':
            manage_apps.create_activities_apps(parsed.activities)
        elif parsed.function == 'clear':
            manage_apps.clear_activities()
        elif parsed.function == 'remove':
            for act in parsed.activities:
                manage_apps.remove_activity(act)
        elif parsed.function == 'create_all':
            manage_apps.create_activities_all()

    elif parsed.subcommand == 'populate':
        if parsed.table == 'administrators':
            populate_database_initial.populate_administrators()
        elif parsed.table == 'users':
            populate_database_initial.populate_users()
        elif parsed.table == 'prices':
            populate_database_initial.populate_prices()
        elif parsed.table == 'projects':
            populate_database_initial.populate_projects()
        elif parsed.table == 'experiments':
            populate_database_initial.populate_experiments()
        elif parsed.table == 'all_but_experiments':
            populate_database_initial.populate_administrators()
            populate_database_initial.populate_users()
            populate_database_initial.populate_prices()
            populate_database_initial.populate_projects()


if __name__ == '__main__':
    exec_from_command()