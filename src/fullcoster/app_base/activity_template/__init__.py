from django.apps import AppConfig
from importlib import import_module

from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory

apps = import_module('apps', __package__)


""" Creating dynamically the AppConfig of the given activity

The template tag {{'activity'}} will be replaced by the name of the ActivityCategory enum specifying the Activity

"""

activity: Activity = ACTIVITIES[ActivityCategory[{{activity}}]]

my_config_class = type(f'{activity.activity_short.capitalize()}Config',
             (AppConfig, ),
             {'name': activity.activity_short.lower()})
my_config_class.__module__ = f'fullcoster.{activity.activity_short.lower()}.apps'


setattr(apps, f'{activity.activity_short.capitalize()}Config', my_config_class)

pass

