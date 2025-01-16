from pathlib import Path

from django.db import models
from fullcoster.lab.models import (Record as LRecord,  Extraction, Record2Range, RecordDate, RecordNights)
from simple_history.models import HistoricalRecords

from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory
""" 
The template tag {{'activity'}} will be replaced by the name of the ActivityCategory enum specifying the Activity
"""
activity: Activity = ACTIVITIES[ActivityCategory[{{'activity'}}]]


activity_short = f'{activity.activity_short}'
entities = activity.entities



class Experiment(models.Model):
    experiment = models.CharField(max_length=200)
    exp_type = models.CharField(choices=[(entity.short, entity.name) for entity in entities],
                                default=entities[0].short,
                                max_length=200)
    def __str__(self):
        return '{:s}'.format(self.experiment)

# class Extraction(Extraction):
#     history = HistoricalRecords()

class Record(LRecord, RecordDate, Record2Range, RecordNights):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    extraction = models.ForeignKey(Extraction, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name="%(app_label)s_%(class)s_related",
                                   related_query_name="%(app_label)s_%(class)ss",
                                   )
    history = HistoricalRecords()

    def __str__(self):
        sub = self.submitted.strftime('%Y-%m-%d')
        try:
            return (f'{activity_short} record {self.id} submitted the {sub}: {self.user} used '
                    f'{self.experiment} from {self.date_from}/{self.get_time_from_display()} to'
                    f' {self.date_to}/{self.get_time_to_display()}')
        except:
            return 'Null record'


