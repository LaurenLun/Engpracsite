from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'boards'

urlpatterns = [
    path('create_theme', views.create_theme, name='create_theme'),
    path('list_themes', views.list_themes, name='list_themes'),
    path('edit_theme/<int:id>', views.edit_theme, name='edit_theme'),
    path('delete_theme/<int:theme_id>', views.delete_theme, name='delete_theme'),
    path('theme/<int:theme_id>', views.view_comments, name='view_comments'),
    path('theme/<int:theme_id>/comment/', views.post_comment, name='post_comment'),
]