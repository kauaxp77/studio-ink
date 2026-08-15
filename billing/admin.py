from django.contrib import admin
from .models import ServiceRecord

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'final_price', 'payment_method', 'date_completed')
    list_filter = ('payment_method', 'date_completed')
    search_fields = ('appointment__client__name',)
