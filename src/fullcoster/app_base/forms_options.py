from django.forms import ModelForm, DateInput, Textarea, NumberInput, Select, CharField, TextInput, ModelChoiceField
from crispy_forms.layout import Fieldset, Submit, Row, Column, Div, Reset, Layout, Button
from crispy_forms.bootstrap import FormActions

from fullcoster.constants.activities import Activity


def get_field(activity: Activity):
    fields = []
    if activity.dates == 1:
        fields.append('date_from')
    elif activity.dates == 2:
        fields.append('date_to')
    fields.extend(['time_from', 'time_to',
                   'user', 'wu'])
    if activity.night:
        fields.append('nights')
    fields.extend(['group', 'project', 'experiment', 'remark'])
    return fields


def get_labels(activity: Activity):
    labels = {}
    if activity.dates == 1:
        labels.update({'date_from': 'From:'})
    elif activity.dates == 2:
        labels.update({'date_to': 'To:'})
    labels.update({'wu': 'WU:', 'experiment': 'Experiment:'})
    if activity.night:
        labels.update({'nights': 'N nights:'})
    labels.update({'time_from': 'Time:', 'time_to': 'Time:'})
    return labels


def get_help_text(activity: Activity):
    help_texts = {'date_from': 'The starting date of your run',
                  'date_to': 'The last date of your run',
                  'time_from': 'The first session of your run',
                  'time_to': 'The last session of your run',
                  'nights': 'If your run went late (after 20h), add the number of late nights you did',
                  'experiment': 'Pick an experiment'
                  }
    help_texts = {}
    if activity.dates == 1:
        help_texts.update({'date_from': 'The starting date of your run'})
    elif activity.dates == 2:
        help_texts.update({'date_to': 'The last date of your run'})
    help_texts.update({'wu': 'Working Unit:', 'experiment': 'Pick an experiment'})
    if activity.night:
        help_texts.update({'nights': 'If your run went late (after 20h), add the number of late nights you did'})
    help_texts.update({'time_from': 'The first session of your run',
                       'time_to': 'The last session of your run'})
    return help_texts


def get_widgets(activity: Activity):
    widgets = {}
    if activity.dates == 1:
        widgets.update({'date_from': DateInput(attrs={'type': 'date', 'class': 'datepicker dfrom time'})})
    elif activity.dates == 2:
        widgets.update({'date_to': DateInput(attrs={'type': 'date', 'class': 'datepicker dto time'})})
    widgets.update({'wu': 'WU:', 'experiment': 'Experiment:'})
    if activity.night:
        widgets.update({'nights': 'N nights:'})
    widgets.update({'time_from': Select(attrs={'class': 'tfrom time'}),
                    'time_to': Select(attrs={'class': 'tto time'})})
    widgets.update(
        {'remark': Textarea(attrs={'placeholder': 'Enter some detail here about your experiment',
                                   'rows': '1', 'cols': '50'}),
         'experiment': Select(attrs={'class': 'experiment', }),
         'group': Select(attrs={'class': 'group', }),
         'project': Select(attrs={'class': 'project', }),
         'user': Select(attrs={'placeholder': 'Surname Name', 'class': 'user'}),
         'wu': NumberInput(attrs={'required': False, 'class': 'uo', 'value': 0, 'min': 0, 'step': 0.5,
                                  'style': 'width:10ch'}),})
    widgets.update({'nights': NumberInput(attrs={'class': 'nights time', 'value': 0, 'min': 0, 'step': 1}),})
    return widgets


def get_layout(activity: Activity):
    wu_row = Row()
    if activity.night:
        wu_row .append(Column('nights', css_class='form-group col-md-6 nightcol'))
    wu_row.append(Column('wu', css_class='form-group col-md-4 uocol'))

    date_row = Row(Column('date_from', css_class='form-group col-md-3'),
                   Column('time_from', css_class='form-group col-md-3'),
                   Div(css_class='w-100'), css_class='form-row')

    if activity.dates == 2:
        date_row.extend([Column('date_to', css_class='form-group col-md-3'),
                         Column('time_to', css_class='form-group col-md-3'),
                         Column('experiment', css_class='form-group col-6'),
                         ])

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