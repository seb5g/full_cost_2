""" Create a new app from the jinja2 template directory app_base.activity_base"""
import subprocess
import sys
import importlib
from collections.abc import Iterable
from pathlib import Path, PurePath
import toml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import shutil

from fullcoster.constants.activities import Activity, ActivityCategory, ACTIVITIES

template_path = Path(__file__).parent.joinpath('activity_template')
apps_parent_path = template_path.parent.parent
js_parent_path = Path(__file__).parent.joinpath('js')
toml_path = Path(__file__).parent.joinpath('apps.toml')


env = Environment(
    loader=FileSystemLoader(template_path),
    autoescape=select_autoescape()
)

def create_parent_dir(path: Path):
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

def create_file_from_template(activity: str, template_path_rel: str):
    path = apps_parent_path.joinpath(activity.lower()).joinpath(template_path_rel)
    create_parent_dir(path)

    if 'logo' in path.stem:
        # rename the logo png file with the proper name
        new_path = path.parent.joinpath(f'logo_{activity.lower()}.png')
        shutil.copy(template_path.joinpath(template_path_rel), new_path)

    else:
        try:
            with path.open('w') as fp:
                env.get_template(template_path_rel).stream(activity= f"'{activity}'").dump(fp)
        except UnicodeError:
            shutil.copy(template_path.joinpath(template_path_rel), path)


def populate_experiments(app: str):
    """ create experiments in database for installed apps"""
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fullcoster.full_cost.settings")
    import django
    django.setup()

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

        activity_obj = ACTIVITIES[ActivityCategory[activity]]

        apps_parent_path.joinpath(activity.lower()).mkdir(exist_ok=True)
        apps_parent_path.joinpath(f'{activity.lower()}/static/js').mkdir(parents=True, exist_ok=True)

        # manage javascript
        new_path = apps_parent_path.joinpath(f'{activity.lower()}/static/js/{activity.lower()}_record.js')
        if activity_obj.uo == 'day':
            js_path = js_parent_path.joinpath('day_record.js')
        elif activity_obj.uo == 'sample':
            js_path = js_parent_path.joinpath('sample_record.js')
        elif activity_obj.uo == 'hours':
            js_path = js_parent_path.joinpath('hour_record.js')
        elif activity_obj.uo == 'session':
            js_path = js_parent_path.joinpath('session_record.js')
        shutil.copy(js_path, new_path)

        toml_dict['apps'].append(activity)
        with toml_path.open('w') as f:
            toml.dump(toml_dict, f)
        for template_path in env.loader.list_templates():
            create_file_from_template(activity, template_path)

    make_migrations()
    migrate()
    for activity in activities:
        populate_experiments(activity)


def _empty_dirs(start_path: Path):
    for path in start_path.iterdir():
        if path.is_dir():
            _empty_dirs(path)
        else:
            path.unlink()


def _delete_dir(start_path: Path):
    _empty_dirs(start_path)
    for path in start_path.iterdir():
        _empty_dirs(path)
        try:
            path.rmdir()
        except OSError:
            _delete_dir(path)
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


def make_migrations():

    subprocess.run(['python', '-m', 'fullcoster.manage', 'makemigrations'],
                   stdout=sys.stdout)

def migrate():
    subprocess.run(['python', '-m', 'fullcoster.manage', 'migrate'],
                   stdout=sys.stdout)


activities = ActivityCategory.names()


if __name__ == '__main__':
    create_activities_apps(('GROWTH_IMP', ))
    #remove_activity('PREPA')
    #clear_activities()
