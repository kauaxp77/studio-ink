from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from .forms import AppointmentRequestForm
from django.forms import model_to_dict
from .models import Appointment
from django.utils import timezone
def booked_dates_api(request):
    booked = Appointment.objects.exclude(status='CANCELLED') \
        .annotate(date=TruncDate('date_time')) \
        .values('date') \
        .annotate(appointments_count=Count('id')) \
        .filter(appointments_count__gte=4)
        
    blocked_dates = [item['date'].strftime('%Y-%m-%d') for item in booked]
    return JsonResponse({'blocked_dates': blocked_dates})

def times_for_date_api(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date is required'}, status=400)
    
    # Busca agendamentos para a data específica (não cancelados)
    appointments = Appointment.objects.filter(
        date_time__date=date_str
    ).exclude(status='CANCELLED')
    
    # Convert aware UTC datetimes to local time before extracting H:M
    booked_times = [timezone.localtime(appt.date_time).strftime('%H:%M') for appt in appointments]
    
    return JsonResponse({'booked_times': booked_times})

def request_appointment(request):
    if request.method == 'POST':
        form = AppointmentRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua solicitação de agendamento foi enviada com sucesso! Entraremos em contato em breve.')
            return redirect('portfolio:index')
    else:
        form = AppointmentRequestForm()
    
    return render(request, 'scheduling/request_appointment.html', {'form': form})
