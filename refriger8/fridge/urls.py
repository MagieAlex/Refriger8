from django.urls import path
from . import views

urlpatterns = [
    path('', views.fridge_view, name='fridge'),
]
