from django.urls import path
from . import views

app_name = 'scheduling'

urlpatterns = [
    path('agendar/', views.request_appointment, name='request'),
    path('api/booked-dates/', views.booked_dates_api, name='booked_dates_api'),
    path('api/times/', views.times_for_date_api, name='times_for_date_api'),
]
