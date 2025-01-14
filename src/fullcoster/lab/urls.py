from django.urls import path
from . import views

app_name = 'lab'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('logged/', views.Index.as_view(logged=True), name='logged'),
    path('projects/', views.Projects.as_view(), name='projects'),
    path('extract/', views.ExtractRecordAll.as_view(), name='extract'),
    path('fextractions/', views.ShowSetExtractionAll.as_view(), name='fextract'),
    path('fextractions/<entity>/', views.ShowSetExtractionAll.as_view(), name='fextract_entity'),
    path('fextractions/<str:entity>/<int:id>/<str:thanks>', views.ShowSetExtractionAll.as_view(), name='fextract_entity_id')

    ]