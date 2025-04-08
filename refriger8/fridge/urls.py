from django.urls import path
from . import views

urlpatterns = [
    path('', views.fridge_view, name='fridge'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('export/', views.export_items_csv, name='export_items'),
    path('overview/', views.overview_view, name='overview'),

]
