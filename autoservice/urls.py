"""autoservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from .views import (
    IndexView, SearchTimeView, SearchWorkTypeView, SearchDateView, SearchCarBrandView, SearchCarView,
    SearchCarGenerationView, CreateRequestForm, WorkInfoView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('ajax/work-info', WorkInfoView.as_view(), name='work-info'),
    path('ajax/search-car-brand', SearchCarBrandView.as_view(), name='search-car-brand'),
    path('ajax/search-car', SearchCarView.as_view(), name='search-car'),
    path('ajax/search-car-generation', SearchCarGenerationView.as_view(), name='search-car-generation'),
    path('ajax/search-work-type', SearchWorkTypeView.as_view(), name='search-work-type'),
    path('ajax/search-date', SearchDateView.as_view(), name='search-date'),
    path('ajax/search-time', SearchTimeView.as_view(), name='search-time'),
    path('ajax/create-work', CreateRequestForm.as_view(), name='create-request-form'),
    path('admin/', admin.site.urls),
]
