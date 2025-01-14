import django_filters
from django.db.models import Q
from .models import Record, Experiment
from ..lab.models import Project
from ..lab import filters as filters
from django.utils.timezone import now
from datetime import timedelta

filtered_project = django_filters.ModelChoiceFilter(\
        queryset=Project.objects.all().exclude(\
            Q(expired__exact=True)&Q(expired_date__lt=now()-timedelta(days=365))))

class RecordFilter(filters.RecordFilter):
    project = filtered_project

    experiment = django_filters.ModelChoiceFilter(queryset=Experiment.objects.all(),
                                               empty_label= 'All Experiments')
    class Meta(filters.RecordFilter.Meta):
        model = Record


class RecordFilterFull(django_filters.FilterSet):
    project = filtered_project
    class Meta:
        model = Record
        fields = tuple([f.name for f in Record._meta.fields])
