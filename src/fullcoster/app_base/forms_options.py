from django.forms import ModelForm, DateInput, Textarea, NumberInput, Select, CharField, TimeInput, ModelChoiceField
from crispy_forms.layout import Fieldset, Submit, Row, Column, Div, Reset, Layout, Button
from crispy_forms.bootstrap import FormActions

from fullcoster.constants.activities import Activity
from fullcoster.constants.entities import WUCategory


def get_field(activity: Activity):
    fields = []
    fields.append('date_from')
    if activity.wu == WUCategory.day:
        fields.append('date_to')
    if activity.session_names is not None:
        fields.extend(['time_from', 'time_to'])
    if activity.wu == WUCategory.duration:
        fields.append('duration')
    fields.extend(['user', 'wu'])
    if activity.night:
        fields.append('nights')
    fields.extend(['group', 'project', 'experiment', 'remark'])
    return fields


def get_labels(activity: Activity):
    labels = {}
    if activity.wu == WUCategory.sample:
        labels.update({'date_from': 'Date:'})
    else:
        labels.update({'date_from': 'From:'})
    if activity.wu == WUCategory.day:
        labels.update({'date_to': 'To:'})
    if activity.wu == WUCategory.duration:
        labels.update({'duration': 'Duration in s:'})
    labels.update({'wu': 'WU:', 'experiment': 'Experiment:'})
    if activity.night:
        labels.update({'nights': 'N nights:'})
    if activity.session_names is not None:
        labels.update({'time_from': 'Time From:', 'time_to': 'Time To:'})
    return labels


def get_help_text(activity: Activity):
    help_texts = {}
    help_texts.update({'date_from': 'The starting date of your run'})
    if activity.wu == WUCategory.day:
        help_texts.update({'date_to': 'The last date of your run'})

    #help_texts.update({'wu': activity.wu_label})
    help_texts.update({'experiment': 'Pick an experiment'})
    if activity.night:
        help_texts.update({'nights': 'If your run went late (after 20h), add the number of late nights you did'})
    if activity.session_names is not None:
        help_texts.update({'time_from': 'The first session of your run',
                           'time_to': 'The last session of your run'})
    return help_texts


def get_widgets(activity: Activity):
    widgets = {}
    widgets.update({'date_from': DateInput(attrs={'type': 'date', 'class': 'datepicker dfrom time'})})
    if activity.wu == WUCategory.day:
        widgets.update({'date_to': DateInput(attrs={'type': 'date', 'class': 'datepicker dto time'})})
    if activity.wu == WUCategory.duration:
        widgets.update({'duration': NumberInput(attrs={'min':0, 'step':1, 'class': 'duration'}),})

    if activity.session_names is not None:
        if activity.wu == WUCategory.day or activity.wu == WUCategory.session:
            widgets.update({'time_from': Select(attrs={'class': 'tfrom time'}),
                            'time_to': Select(attrs={'class': 'tto time'})})
        elif activity.wu == WUCategory.hours:
            widgets.update({'time_from': TimeInput(attrs={'type': 'time', 'class': 'timepicker tfrom time'}),
                            'time_to': TimeInput(attrs={'type': 'time', 'class': 'timepicker tto time'}),})

    widgets.update(
        {'remark': Textarea(attrs={'placeholder': 'Enter some detail here about your experiment',
                                   'rows': '1', 'cols': '50'}),
         'experiment': Select(attrs={'class': 'experiment', }),
         'group': Select(attrs={'class': 'group', }),
         'project': Select(attrs={'class': 'project', }),
         'user': Select(attrs={'placeholder': 'Surname Name', 'class': 'user'}),
         'wu': NumberInput(attrs={'required': False, 'class': 'wu', 'value': 0, 'min': 0, 'step': 0.5,
                                  'style': 'width:10ch'}),})
    if activity.night:
        widgets.update({'nights': NumberInput(attrs={'class': 'nights time', 'value': 0, 'min': 0, 'step': 1}),})
    return widgets


def get_layout(activity: Activity):
    wu_row = Row()
    if activity.night:
        wu_row .append(Column('nights', css_class='form-group col-md-6 nightcol'))
    wu_row.append(Column('wu', css_class='form-group col-md-4 wucol'))

    date_row = Row(Column('date_from', css_class='form-group col-md-3'), css_class='form-row')

    if activity.wu == WUCategory.day or activity.wu == WUCategory.session or activity.wu == WUCategory.hour:
        date_row.append(Column('time_from', css_class='form-group col-md-3'))

    date_row.append(Div(css_class='w-100'))

    if activity.wu == WUCategory.day:
        date_row.append(Column('date_to', css_class='form-group col-md-3'))
    if activity.wu == WUCategory.day or activity.wu == WUCategory.session or activity.wu == WUCategory.hour:
        date_row.append(Column('time_to', css_class='form-group col-md-3'))
    if activity.wu == WUCategory.duration:
        date_row.append(Column('duration', css_class='form-group col-md-6 gi-col durationcol'))
    date_row.append(Column('experiment', css_class='form-group col-6'))

    layout = Layout(
        Div(
            date_row,
            wu_row,
            Row('project'),
            Row(
                Column('user', css_class='form-group col-md-6'),
                Column('group', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('user_text_name', css_class='form-group col-md-6 usercol'),
                Column('user_text_surname', css_class='form-group col-md-6 usercol'),
                css_class='form-row'
            ),
            Row(
                Column('remark', css_class='form-group mr-5'),
                Column(FormActions(
                    Button('okbutton', 'Submit', css_class='btn-primary okclass'),
                    # form will be triggered using a popup jquery, see static/js/osp_records.js
                    Reset('name', 'Reset', css_class='btn-secondary')
                ), css_class='form-group align-items-center')
            ),
        )
    )
    return layout