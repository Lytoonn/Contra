from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'client-dashboard'),
    path('browse-articles/', views.browse_articles, name = 'client-browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name = 'client-subscribe-plan'),
    path('update-user/', views.update_user, name = 'client-update-user'),
    path('create-subscription/<str:sub_id>/<str:plan_code>', views.create_subscription, name = 'client-create-subscription'),
]