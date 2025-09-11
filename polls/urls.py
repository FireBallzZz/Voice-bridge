from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('create/', views.create_poll, name='create_poll'),
    path('vote/<int:poll_id>/', views.vote_poll, name='vote_poll'),
    path('edit/<int:poll_id>/', views.edit_poll, name='edit_poll'),
    path('delete/<int:poll_id>/', views.delete_poll, name='delete_poll'),
]