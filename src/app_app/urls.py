# src/app_app/urls.py
from django.urls import path
from .views import suma_view

urlpatterns = [
    path('', suma_view, name='suma'),
]