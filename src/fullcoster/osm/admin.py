from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Experiment, Record


admin.site.register(Experiment, SimpleHistoryAdmin)
admin.site.register(Record, SimpleHistoryAdmin)