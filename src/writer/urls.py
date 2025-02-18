from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'writer-dashboard'),
    path('create-article/', views.create_article, name='writer-create-article'),
    path('update-article/<int:id>', views.update_article, name='writer-update-article'),
    path('delete-article/<int:id>', views.delete_article, name='writer-delete-article'),
    path('my-articles/', views.my_articles, name='writer-my-articles'),
    path('update-user/', views.update_user, name='writer-update-user')
]