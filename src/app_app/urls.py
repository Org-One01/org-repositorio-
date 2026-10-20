# src/app_app/urls.py
from django.urls import path
from .views import suma_view
from . import views

urlpatterns = [
    path('', suma_view, name='suma'),
    path('producto/editar/<str:db_engine>/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<str:db_engine>/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]