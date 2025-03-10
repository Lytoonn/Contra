from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name = 'client-dashboard'),
    path('browse-articles/', views.browse_articles, name = 'client-browse-articles'),
    path('subscribe-plan/', views.subscribe_plan, name = 'client-subscribe-plan'),
    path('update-user/', views.update_user, name = 'client-update-user'),
    path('create-subscription/<str:sub_id>/<str:plan_code>', views.create_subscription, name = 'client-create-subscription'),
    path('cancel-subscription/<int:id>', views.cancel_subscription, name = 'client-cancel-subscription'),
    path('update-subscription/<int:id>', views.update_subscription, name = 'client-update-subscription'),
    path('update-subscription-confirmed/', views.update_subscription_confirmed, name = 'client-update-subscription-confirmed'),
]