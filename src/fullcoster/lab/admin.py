from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.
from .models import Group, Project, User, Price, Extraction, Gestionnaire

admin.site.register(Price, SimpleHistoryAdmin)
admin.site.register(Group, SimpleHistoryAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(User, SimpleHistoryAdmin)
admin.site.register(Extraction, SimpleHistoryAdmin)
admin.site.register(Gestionnaire, SimpleHistoryAdmin)