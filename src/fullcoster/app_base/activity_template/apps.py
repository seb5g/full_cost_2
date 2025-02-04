from django.apps import AppConfig
from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory


""" Creating dynamically the AppConfig of the given activity
{% raw %}
The template tag {{'activity'}} will be replaced by the name of the ActivityCategory enum specifying the Activity
{% endraw %}
"""

activity: Activity = ACTIVITIES[ActivityCategory['{{activity.activity_short}}']]


class AppConfig(AppConfig):
    name = f'fullcoster.{activity.activity_short.lower()}'

