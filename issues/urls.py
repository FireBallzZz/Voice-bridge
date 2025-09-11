from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_issue, name='create_issue'),
    path('list/', views.issue_list, name='issue_list'),
    path('vote/<int:issue_id>/', views.vote_issue, name='vote_issue'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('edit/<int:issue_id>/', views.edit_issue, name='edit_issue'),
    path('delete/<int:issue_id>/', views.delete_issue, name='delete_issue'),
    path('like/<int:issue_id>/', views.like_issue, name='like_issue'),
    path('issue/<int:issue_id>/comment/', views.add_comment, name='add_comment'),
    path('issue/<int:issue_id>/status/', views.update_status, name='update_status'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/', views.profile_view, name='profile')


]
