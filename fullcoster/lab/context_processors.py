from pathlib import Path
import importlib

import toml

from fullcoster.constants.activities import Activity, ActivityCategory, ACTIVITIES
toml_path = Path(__file__).parent.parent.joinpath('app_base/apps.toml')

all_activity_short = []
all_activity_long = []

for installed_apps in toml.load(toml_path)['apps']:
    activity = ACTIVITIES[ActivityCategory[installed_apps]]
    all_activity_short.append(activity.activity_short.lower())
    all_activity_long.append(activity.activity_long)


def get_all_activity(request):
    return {'all_activity_short': all_activity_short, 'all_activity_long': all_activity_long,}
