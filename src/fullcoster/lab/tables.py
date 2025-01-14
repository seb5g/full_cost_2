import django_tables2 as tables
from .models import Project, Extraction

field_sequence = ('date_from', 'time_from',
                  'date_to', 'time_to',
                  'project', 'wu', 'nights',
                  'user', 'group',
                  'experiment', 'remark', 'factured', 'submitted',)

class RecordTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap.html"
        fields = ('id', 'submitted', 'wu', 'date_from', 'date_to', 'project', 'group',  'user',  'experiment', 'remark')
        sequence = ('id', 'date_from', 'date_to', 'project', 'wu', '...', 'submitted')

class ProjectTable(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap.html"
        model = Project
        fields = ['project_name', 'project_pi', 'amount_left', 'is_cnrs', 'is_academic', 'is_national']

    def render_amount_left(self, value):
        return f'{value:.02f}'

class RecordTableFull(tables.Table):
    class Meta:
        template_name = "django_tables2/bootstrap.html"

class ExtractionTable(tables.Table):
    class Meta:
        model = Extraction
        template_name = "django_tables2/bootstrap4.html"
        exclude = ('id',)
    def render_amount(self, value):
        return f'{value:.02f}'
