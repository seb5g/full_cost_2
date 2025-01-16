from pathlib import Path
from lab.views import FilterRecord, Export, GetRecord

from .models import Record
from .forms import RecordForm
from .tables import RecordTable, RecordTableFull
from .filters import RecordFilter
from full_cost.utils import manage_time
from full_cost.utils.constants import ACTIVITIES
#####################################################
activity_short = Path(__file__).parts[-2]
activity_long = ACTIVITIES[activity_short]['activity_long']
activity={'short': activity_short, 'long': activity_long,}
#####################################################

class FilterRecord(FilterRecord):
    filter_class = RecordFilter
    table_class = RecordTable
    activity = activity

class Export(Export):
    table_class = RecordTableFull
    activity = activity


class GetRecord(GetRecord):
    record_class = Record
    form_class = RecordForm
    activity = activity

    def validate_record(self, record, form):
        error = manage_time.is_range_intersecting_date_session(record, self.record_class)
        if error is not None:
            form.add_error(None, error)
        validate_state = True
        return form, validate_state


