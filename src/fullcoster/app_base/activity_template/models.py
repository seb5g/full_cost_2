from pathlib import Path

from django.db import models
from fullcoster.lab.models import Extraction
from fullcoster.lab import models as lab_models
from simple_history.models import HistoricalRecords

from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory, UO
""" 
The template tag {{activity}} will be replaced by the name of the ActivityCategory enum specifying the Activity
"""
activity: Activity = ACTIVITIES[ActivityCategory[{{activity}}]]


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


bases = [lab_models.Record]
if activity.uo == UO.day:
    RecordDate = lab_models.RecordDate
else:
    RecordDate = lab_models.RecordOneDate


base_class = [lab_models.Record, RecordDate]
if (activity.session_names is not None and
        (activity.uo == UO.day or
         activity.uo == UO.session or
         activity.uo == UO.sample)):

    class RecordRange(models.Model):
        date_choices = [(ind, name) for ind, name in enumerate(activity.session_names)]
        time_from = models.SmallIntegerField(choices=date_choices, default=0)
        time_to = models.SmallIntegerField(choices=date_choices, default=0)

        class Meta:
            abstract = True

    base_class.append(RecordRange)

elif activity.uo == UO.hours:
    base_class.append(lab_models.RecordTwoTimes)
elif activity.uo == UO.duration:
    base_class.append(lab_models.RecordDuration)

if activity.night:
    base_class.append(lab_models.RecordNights)


class Record(*base_class):
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


