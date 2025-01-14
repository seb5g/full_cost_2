from pathlib import Path
from django.urls import path
from . import views
from .models import Record

activity_short = Path(__file__).parts[-2]

app_name = activity_short
urlpatterns = [
    path('', views.FilterRecord.as_view(), name='index'),
    path('record/', views.GetRecord.as_view(), name='grecord'),
    path('frecords/', views.FilterRecord.as_view(), name='frecords'),
    path('frecords/thanks', views.FilterRecord.as_view(thanks=True), name='thanks'),
    path('export/', views.Export.as_view(), name='export'),
    ]

