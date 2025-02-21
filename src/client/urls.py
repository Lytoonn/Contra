from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'client-dashboard'),
    path('browse-articles/', views.browse_articles, name = 'client-browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name = 'client-subscribe-plan'),
]