from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'writer-dashboard'),
    path('create-article/', views.create_article, name='writer-create-article'),
    path('my-articles/', views.my_articles, name='writer-my-articles'),
    path('account-settings', views.account_settings, name='writer-account-settings')
]