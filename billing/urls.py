from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/manage/<int:pk>/', views.manage_appointment, name='manage_appointment'),
    path('dashboard/portfolio/', views.manage_portfolio, name='manage_portfolio'),
    path('dashboard/profile/', views.manage_profile, name='manage_profile'),
    path('dashboard/consentimento/<int:pk>/', views.consent_pdf, name='consent_pdf'),
]
