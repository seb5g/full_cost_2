from pathlib import Path
from django.urls import path
from . import views
from .models import Record

from fullcoster.constants.activities import Activity, ACTIVITIES, ActivityCategory
""" 
The template tag {{activity}} will be replaced by the name of the ActivityCategory enum specifying the Activity
"""
activity: Activity = ACTIVITIES[ActivityCategory[{{activity}}]]

activity_short = f'{activity.activity_short.lower()}'


app_name = activity_short
urlpatterns = [
    path('', views.FilterRecord.as_view(), name='index'),
    path('record/', views.GetRecord.as_view(), name='grecord'),
    path('frecords/', views.FilterRecord.as_view(), name='frecords'),
    path('frecords/thanks', views.FilterRecord.as_view(thanks=True), name='thanks'),
    path('export/', views.Export.as_view(), name='export'),
    ]

