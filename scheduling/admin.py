from django.contrib import admin
from .models import Client, Appointment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'date_time', 'status', 'estimated_price')
    list_filter = ('status', 'date_time')
    search_fields = ('client__name', 'description')
