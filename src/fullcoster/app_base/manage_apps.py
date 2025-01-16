""" Create a new app from the jinja2 template directory app_base.activity_base"""
from collections.abc import Iterable
from pathlib import Path, PurePath
import toml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from fullcoster.constants.activities import Activity, ActivityCategory

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

    with path.open('w') as fp:
        env.get_template(template_path).stream(activity= f"'{activity}'").dump(fp)


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
    #create_activities_apps(activities)
    #remove_activity('PREPA')
    clear_activities()