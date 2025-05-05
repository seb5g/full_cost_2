from django.forms import ModelForm, DateInput, Textarea, NumberInput, Select, CharField, TextInput, ModelChoiceField
from .models import Record
from fullcoster.lab.forms import RecordForm as LRecordForm
from fullcoster.lab.forms import ExtractionForm as LExtractionForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Submit, Row, Column, Div, Reset, Layout, Button
from crispy_forms.bootstrap import FormActions

from fullcoster.app_base import forms_options
from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory
""" 
{% raw %}
The template tag {{'activity'}} will be replaced by the name of the ActivityCategory enum specifying the Activity
{% endraw %}
"""
activity: Activity = ACTIVITIES[ActivityCategory['{{activity.activity_short}}']]

is_night = activity.night

activity_short = f'{activity.activity_short}'
entities = activity.entities


class RecordForm(LRecordForm):
    class Meta(LRecordForm.Meta):
        model = Record
        fields = forms_options.get_field(activity)
        labels = forms_options.get_labels(activity)
        help_texts = forms_options.get_help_text(activity)
        widgets = forms_options.get_widgets(activity)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.help_text_inline = False
        self.helper.form_class = 'form-horizontal formclass'
        self.helper.form_id = 'form_id'
        self.helper.form_tag = True
        self.helper.layout = forms_options.get_layout(activity)


        super().__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                if 'class' in self.fields[field].widget.attrs:
                    self.fields[field].widget.attrs['class'] += ' has-popover'
                self.fields[field].widget.attrs.update(
                    {'data - toggle': 'popover',
                     'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})


