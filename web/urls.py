from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.users_page, name='users'),

    path('provider-verification/', views.provider_verification, name='provider_verification'),
    path('provider-verification/<int:pk>/approve/', views.approve_provider, name='approve_provider'),
    path('provider-verification/<int:pk>/reject/', views.reject_provider, name='reject_provider'),

    path('deliveries/', views.deliveries, name='deliveries'),
    path('escrow-payments/', views.escrow_payments, name='escrow'),
    path('transactions/', views.transactions, name='transactions'),
    path('ratings-feedback/', views.ratings_feedback, name='feedback'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_page, name='settings'),
    path('logout/', views.custom_logout, name='logout'),
]