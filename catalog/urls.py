from django.urls import path
from . import views

urlpatterns = [
        path('', views.catalog_main, name='catalog_main'),
]
