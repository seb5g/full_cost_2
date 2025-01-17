"""
URL configuration for full_cost_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from pathlib import Path
import toml

from django.contrib import admin
from django.urls import path, include

ACTIVITY_APPS = toml.load(Path(__file__).parent.parent.joinpath('app_base/apps.toml'))['apps']


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),]

try:
    from fullcoster.lab.views import Index
    urlpatterns.append(path('', Index.as_view(), name='index'))
    urlpatterns.append(path('lab/', include('fullcoster.lab.urls')))

    for app in ACTIVITY_APPS:
        urlpatterns.append(path(f'{app.lower()}/', include(f'fullcoster.{app.lower()}.urls')))


except Exception as e:
    print(str(e))
