from pathlib import Path
from fullcoster.lab.views import FilterRecord, Export, GetRecord

from .models import Record
from .forms import RecordForm
from .tables import RecordTable, RecordTableFull
from .filters import RecordFilter

from fullcoster.utils import manage_time

#################################################################
from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory
from fullcoster.constants.entities import WUCategory
""" 

The template tag {{'activity'}} will be replaced by the name of the ActivityCategory enum specifying the Activity

"""
activity: Activity = ACTIVITIES[ActivityCategory['FIB_MEB']]
activity_short = f'{activity.activity_short.lower()}'
activity_long = activity.activity_long

activity_dict = {'short': activity_short, 'long': activity_long,}
#####################################################

class FilterRecord(FilterRecord):
    filter_class = RecordFilter
    table_class = RecordTable
    activity = activity_dict

class Export(Export):
    table_class = RecordTableFull
    activity = activity_dict


class GetRecord(GetRecord):
    record_class = Record
    form_class = RecordForm
    activity = activity_dict

    def validate_record(self, record, form):
        if activity.wu == WUCategory.day or activity.wu == WUCategory.session:
            error = manage_time.is_range_intersecting_date_session(record, self.record_class)
        elif activity.wu == WUCategory.sample:
            error = None
        elif activity.wu == WUCategory.duration:
            error = None
        elif activity.wu == WUCategory.hour:
            error = manage_time.is_range_intersecting_datetime(record, self.record_class)

        if error is not None:
            form.add_error(None, error)
        validate_state = True
        return form, validate_state

