from django.forms import ModelForm, DateInput, Textarea, NumberInput, Select, CharField, TextInput, ModelChoiceField
from django.db.models.query import QuerySet
from .models import Record, Extraction
from lab.models import Project, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div

class RecordForm(ModelForm):

    user = ModelChoiceField(queryset=User.objects.all().filter(is_left=False), label='User:',
                            help_text='Select OTHER if not in list', widget=Select(attrs={'class': 'user'}))

    user_text_name = CharField(required=False, max_length=200, label='', widget=TextInput(attrs={'class': 'user_other', 'placeholder': 'First Name', 'required': False,}))
    user_text_surname = CharField(required=False, max_length=200, label='', widget=TextInput(attrs={'class': 'user_other', 'placeholder': 'Last Name', 'required': False}))
    project = ModelChoiceField(queryset=Project.objects.all().filter(expired__exact=False),
                               help_text='If your project is not in the list, enter Divers or Service',
                               label='Project and PI:', widget=Select(attrs={'class': 'project'}))

    class Meta:
        error_css_class = 'error'
        required_css_class = 'required'
        model = Record
        fields = [f.name for f in model._meta.fields]

class ExtractionForm(ModelForm):

    extractions = ModelChoiceField(queryset=Extraction.objects.all().filter(factured=False), help_text='Select the Extraction you want to set as factured',
                               label='Extractions list:')

    class Meta:
        model = Extraction
        error_css_class = 'error'
        required_css_class = 'required'

        fields = ('extractions',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.help_text_inline = False
        self.helper.form_class = 'form-horizontal mr-1'
        self.helper.form_id = 'form_id'
        self.helper.form_tag = False

        self.helper.layout = Layout(
                Row(
                    Column('extractions', css_class='form-group col-md-6 mb-0 mr-1'),
                    Submit('submit', 'Set as Factured', css_class='ml-1'),
                    css_class='form-row mr-1'
                ),
                Div(css_class='mb-2')
        )
        super().__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update(
                    {'class': 'has-popover',
                     'data - toggle': 'popover',
                     'data-content': help_text, 'data-placement': 'right',
                     'data-container': 'body'})
            self.fields['extractions'].widget.attrs.update({'class': 'extfield'})