from pathlib import Path
from django.db import models
import django_filters
from crispy_forms.helper import FormHelper
from django.forms import IntegerField, Form, DateInput, DateField
from django.forms.widgets import Select
from lab.models import Project, User, Group, Extraction



class DateRangeWidget(django_filters.widgets.SuffixedMultiWidget):
    template_name = 'django_filters/widgets/multiwidget.html'
    suffixes = ['after', 'before']

    def __init__(self, attrs=None):
        widgets = (DateInput(attrs={'type':'date', 'class':'datepicker', 'placeholder': 'from'}),
                   DateInput(attrs={'type':'date', 'class':'datepicker'}))
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

class DateRangeField(django_filters.fields.DateRangeField):
    widget = DateRangeWidget

class DateFromToRangeFilter(django_filters.DateFromToRangeFilter):
    field_class = DateRangeField

class RecordFilter(django_filters.FilterSet):

    date_from = DateFromToRangeFilter()
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(),
                                               empty_label= 'All Projects')
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all().filter(is_left=False),
                                               empty_label= 'All Users')
    group = django_filters.ModelChoiceFilter(queryset=Group.objects.all(),
                                               empty_label= 'All Groups')

    class Meta:
        fields = ('date_from', 'project', 'user', 'group', 'experiment')




class ProjectFilter(django_filters.FilterSet):

    project_name = django_filters.ChoiceFilter(choices=[(p.project_name, p.project_name) for p in Project.objects.all().distinct('project_name').order_by('project_name').filter(expired=False)], empty_label='All projects')
    project_pi = django_filters.ModelChoiceFilter(queryset=User.objects.all().filter(user_last_name__in=[p.project_pi.user_last_name for p in Project.objects.all() if p.project_pi is not None]),
                                               empty_label='All PIs')
    class Meta:
        model = Project
        fields = ['project_pi', 'project_name']



class ExtractDisplayFilter(django_filters.FilterSet):
    creation_date = django_filters.DateFilter(widget=DateInput(attrs={'type':'date', 'class':'datepicker', 'placeholder': 'from'}))
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(),
                                               empty_label= 'All Projects')

    class Meta:
        model = Extraction
        fields = ('creation_date', 'project', 'factured')


class ExtractFilterForm(Form):
    pass
    # from full_cost.constants import BILLINGS
    #
    # billing = django_filters.fields.ChoiceField(choices=[bill['entity'] for bill in BILLINGS], empty_label=None)
    # date_from = DateRangeField()
    # project = django_filters.fields.ModelChoiceField(queryset=Project.objects.all(),
    #                                            empty_label= 'All Projects')
    # class Meta:
    #     widgets = {
    #         'billing': Select(attrs={'class': 'subform'}),
    #         'date_from': DateRangeWidget(attrs={'class': 'subform'}),
    #         'project': Select(attrs={'class': 'subform'}),}



class FilterSet(django_filters.filterset.FilterSet):
    pass
    def filter_queryset(self, queryset):
        """
        Filter the queryset with the underlying form's `cleaned_data`. You must
        call `is_valid()` or `errors` before calling this method.

        This method should be overridden if additional filtering needs to be
        applied to the queryset before it is cached.
        """
        for name, value in self.form.cleaned_data.items():
            if name != 'billing':
                if name == 'date_from':
                    queryset = queryset.filter(date_from__range=(value.start, value.stop))
                else:
                    queryset = self.filters[name].filter(queryset, value)
                assert isinstance(queryset, models.QuerySet), \
                    "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
                    % (type(self).__name__, name, type(queryset).__name__)
        return queryset
    def get_form_class(self):
        """
        Returns a django Form suitable of validating the filterset data.

        This method should be overridden if the form class needs to be
        customized relative to the filterset instance.
        """

        return ExtractFilterForm

class ExtractFilterAll(django_filters.FilterSet):
    pass
    # from full_cost.utils.constants import BILLINGS
    #
    # date_from = DateFromToRangeFilter()
    # billing = django_filters.ChoiceFilter(choices=[bill['entity'] for bill in BILLINGS])
    # project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(),
    #                                            empty_label= 'All Projects')
    #
    # class Meta:
    #     pass
    # #     model = Record
    # #     fields = ('billing', 'date_from', 'project')
    #
    # def filter_queryset(self, queryset):
    #     """
    #     Filter the queryset with the underlying form's `cleaned_data`. You must
    #     call `is_valid()` or `errors` before calling this method.
    #
    #     This method should be overridden if additional filtering needs to be
    #     applied to the queryset before it is cached.
    #     """
    #     for name, value in self.form.cleaned_data.items():
    #         if name != 'billing':
    #             queryset = self.filters[name].filter(queryset, value)
    #             assert isinstance(queryset, models.QuerySet), \
    #                 "Expected '%s.%s' to return a QuerySet, but got a %s instead." \
    #                 % (type(self).__name__, name, type(queryset).__name__)
    #     return queryset