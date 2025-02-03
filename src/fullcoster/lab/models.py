from pathlib import Path
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.utils.timezone import now
from simple_history.models import HistoricalRecords
import datetime
from fullcoster.constants.entities import PriceCategory, ENTITIES, get_entities_as_list

activity_short = Path(__file__).parts[-2]

# Create your models here.


class Gestionnaire(models.Model):

    first_name = models.CharField(max_length=200, default=None)
    last_name = models.CharField(max_length=200, default=None)
    email = models.EmailField(max_length=200, default=None)
    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return '{:s} {:s}'.format(self.last_name, self.first_name)


class Group(models.Model):
    group = models.CharField(max_length=200)
    description = models.CharField(max_length=200, default='')
    gestionnaire = models.ForeignKey(Gestionnaire, on_delete=models.SET_NULL, default=None, null=True)
    history = HistoricalRecords()
    class Meta:
        ordering = ['group']

    def __str__(self):
        return self.group


class User(models.Model):
    user_last_name = models.CharField(max_length=200)
    user_first_name = models.CharField(max_length=200)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, default=None, null=True)
    is_left = models.BooleanField(default=False)

    history = HistoricalRecords()
    class Meta:
        ordering = ['user_last_name']

    def __str__(self):
        return f'{self.user_last_name} {self.user_first_name}'


class Project(models.Model):

    project_name = models.CharField(max_length=200)
    project_pi = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    is_cnrs = models.BooleanField(default=True) # project managed by CNRS (True) or other institutions (False)
    is_academic = models.BooleanField(default=True) #for academic clients (CNRS, Fac, INSA, others) for private clients or prestations (False)
    is_national = models.BooleanField(default=True) #for ANR or NEXT (True)
    expired = models.BooleanField(default=False)
    expired_date = models.DateField(default=now)
    amount_left = models.FloatField(default=0.0)
    history = HistoricalRecords()

    class Meta:
        ordering = ['project_name']

    def __str__(self):
        return f'{self.project_name} / {self.project_pi}'


class Price(models.Model):
    price_category = models.CharField(max_length=200,
                                      choices={pcat.name: pcat.value for pcat in PriceCategory},
                                      default=PriceCategory.T1)
    price = models.FloatField(default=0)
    price_name = models.CharField(max_length=200, default='')
    price_entity = models.CharField(max_length=200, choices=get_entities_as_list(),
                                    default=get_entities_as_list()[0])
    def __str__(self):
        return f'{self.price_entity}: {self.price_name}/{self.price_category}'

    class Meta:
        ordering = ['price_entity', 'price_name', 'price_category']


class Extraction(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date_after = models.DateField(default=now)
    date_before = models.DateField(default=now)
    creation_date = models.DateField(default=now)
    creation_id = models.IntegerField(default=-1)
    factured = models.BooleanField(default=False)
    amount = models.FloatField(default=0.0)
    billing = models.CharField(max_length=200, choices=get_entities_as_list(),
                               default=get_entities_as_list()[0])
    submitted = models.BooleanField(default=False)
    class Meta:
        ordering = ['creation_date', 'creation_id']

    def __str__(self):
        return (f"Extraction {self.billing}-{self.creation_date.strftime('%y')}-"
                f"{self.creation_id:03d} for {self.project}")

class Record(models.Model):
    submitted = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank = True, null=True,
                             related_name="%(app_label)s_%(class)s_related",
                             related_query_name="%(app_label)s_%(class)ss",
                             )
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name="%(app_label)s_%(class)s_related",
                              related_query_name="%(app_label)s_%(class)ss",
                              )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank = True,
                                related_name="%(app_label)s_%(class)s_related",
                                related_query_name="%(app_label)s_%(class)ss",
                                )
    remark = models.TextField()
    wu = models.FloatField(default=0, validators=[MinValueValidator(0)], blank=True)
    billing = models.CharField(max_length=200, choices=get_entities_as_list(),
                               default=get_entities_as_list()[0][0])


    class Meta:
        abstract = True
        ordering = ['submitted']

    def __str__(self):
        sub = self.submitted.strftime('%Y-%m-%d')
        try:
            return f'{activity_short} record {self.id} submitted the {sub}'
        except:
            return 'Null record'


class RecordNights(models.Model):
    nights = models.PositiveIntegerField(default=0)
    class Meta:
        abstract = True

class RecordDuration(models.Model):
    duration = models.PositiveIntegerField(default=0)
    class Meta:
        abstract = True

class RecordOneDate(models.Model):
    date_from = models.DateField(default=now)
    class Meta:
        abstract = True

class RecordOneDateTwoTimes(models.Model):
    date_from = models.DateField(default=now)
    time_from = models.TimeField(default=datetime.time(0, 0, 0))
    time_to = models.TimeField(default=datetime.time(0, 0, 0))
    class Meta:
        abstract = True

class RecordTwoDatesTwoTimes(models.Model):
    date_from = models.DateField(default=now)
    date_to = models.DateField(default=now)
    time_from = models.TimeField(default=datetime.time(0, 0, 0))
    time_to = models.TimeField(default=datetime.time(0, 0, 0))
    class Meta:
        abstract = True


class RecordTwoTimes(models.Model):
    time_from = models.TimeField(default=datetime.time(0, 0, 0))
    time_to = models.TimeField(default=datetime.time(0, 0, 0))
    class Meta:
        abstract = True


class RecordDate(models.Model):
    date_from = models.DateField(default=now)
    date_to = models.DateField(default=now)

    class Meta:
        abstract = True


class RecordDateTime(RecordDate):
    date_from = models.DateTimeField(default=now)
    date_to = models.DateTimeField(default=now)

    class Meta:
        abstract = True