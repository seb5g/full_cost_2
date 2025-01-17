""" Create a new app from the jinja2 template directory app_base.activity_base"""
import importlib
from collections.abc import Iterable
from pathlib import Path, PurePath
import toml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from fullcoster.constants.activities import Activity, ActivityCategory, ACTIVITIES

template_path = Path(__file__).parent.joinpath('activity_template')
apps_parent_path = template_path.parent.parent
toml_path = Path(__file__).parent.joinpath('apps.toml')


env = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape()
)


def create_file_from_template(activity: str, template_path: str):
    path = apps_parent_path.joinpath(activity.lower()).joinpath(template_path)
    if not path.parent.exists():
        path.parent.mkdir(exist_ok=True)

    if 'record.js' in path:
        # rename the record javascript file with the proper name
        path = path.parent.joinpath(f'{activity.lower()}_record.js')

    if 'logo.png' in path:
        # rename the logo png file with the proper name
        path = path.parent.joinpath(f'logo_{activity.lower()}.js')

    with path.open('w') as fp:
        env.get_template(template_path).stream(activity= f"'{activity}'").dump(fp)


def populate_experiments():
    """ create experiments in database for installed apps"""
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fullcoster.full_cost.settings")
    import django
    django.setup()

    for app in toml.load(toml_path)['apps']:
        models_module = importlib.import_module(f'fullcoster.{app.lower()}.models')

        experiments = []
        for entity in ACTIVITIES[ActivityCategory[app]].entities:
            experiments.extend([(exp, entity.short) for exp in entity.experiments])

        for e in models_module.Experiment.objects.all():
            e.delete()

        for e in experiments:
            exp = models_module.Experiment(experiment=e[0], exp_type=e[1])
            exp.save()
            print(e)


def create_activities_apps(activities: Iterable[str]):
    toml_dict = toml.load(toml_path)
    for activity in activities:
        toml_dict['apps'].append(activity)
        with toml_path.open('w') as f:
            toml.dump(toml_dict, f)
        for template_path in env.loader.list_templates():
            create_file_from_template(activity, template_path)


def _empty_dirs(start_path: Path):
    for path in start_path.iterdir():
        if path.is_dir():
            _empty_dirs(path)
        else:
            path.unlink()


def _delete_dir(start_path: Path):
    _empty_dirs(start_path)
    for path in start_path.iterdir():
        path.rmdir()
    start_path.rmdir()


def remove_activity(activity: str):
        toml_dict = toml.load(toml_path)
        if activity in toml_dict['apps']:
            toml_dict['apps'].remove(activity)
            with toml_path.open('w') as f:
                toml.dump(toml_dict, f)
        if apps_parent_path.joinpath(activity.lower()).exists():
            _delete_dir(apps_parent_path.joinpath(activity.lower()))


def clear_activities():
    for activity in ActivityCategory.names():
        remove_activity(activity)


activities = ActivityCategory.names()


if __name__ == '__main__':
    create_activities_apps(('OSM',))
    #remove_activity('PREPA')
    #clear_activities()
    populate_experiments()