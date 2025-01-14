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

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),]

try:
    from fullcoster.lab.views import Index
    urlpatterns.append(path('', Index.as_view(), name='index'))
    urlpatterns.append(path('lab/', include('fullcoster.lab.urls')))
#     path('osp/', include('osp.urls')),
#     path('met/', include('met.urls')),
#     path('prepa/', include('prepa.urls')),
#     path('fib/', include('fib.urls')),
#     path('mphys/', include('mphys.urls')),
#     path('chem/', include('chem.urls')),
#     path('imag/', include('imag.urls')),
#     path('fab/', include('fab.urls')),
#     path('implant/', include('implant.urls')),
#     path('engi/', include('engi.urls')),

except Exception as e:
    print(str(e))
