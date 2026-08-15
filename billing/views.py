from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import ServiceRecord
from scheduling.models import Appointment
from portfolio.models import Work, ArtistProfile, Certification
from django.db.models import Sum, Count
from django.utils import timezone
import urllib.parse
import re

@staff_member_required
def dashboard(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    from datetime import timedelta
    period = request.GET.get('period', 'month')
    
    if period == 'day':
        services_filtered = ServiceRecord.objects.filter(
            date_completed__year=current_year,
            date_completed__month=current_month,
            date_completed__day=now.day
        )
        period_label = 'Hoje'
    elif period == 'week':
        start_date = now - timedelta(days=7)
        services_filtered = ServiceRecord.objects.filter(date_completed__gte=start_date)
        period_label = 'Últimos 7 Dias'
    elif period == 'year':
        services_filtered = ServiceRecord.objects.filter(date_completed__year=current_year)
        period_label = f'Ano de {current_year}'
    else: # month
        services_filtered = ServiceRecord.objects.filter(
            date_completed__month=current_month,
            date_completed__year=current_year
        )
        period_label = 'Este Mês'

    total_revenue = services_filtered.aggregate(Sum('final_price'))['final_price__sum'] or 0
    total_tattoos = services_filtered.count()

    payment_breakdown = services_filtered.values('payment_method').annotate(
        total=Sum('final_price'),
        count=Count('id')
    )
    
    import json
    from django.db.models.functions import TruncDate
    
    pie_labels = [item['payment_method'] for item in payment_breakdown]
    pie_data = [float(item['total']) for item in payment_breakdown]
    
    trend_data = services_filtered.annotate(date=TruncDate('date_completed')).values('date').annotate(total=Sum('final_price')).order_by('date')
    line_labels = [item['date'].strftime('%d/%m') for item in trend_data]
    line_data = [float(item['total']) for item in trend_data]

    # 2. Próximos Agendamentos (Todos Pendentes ou Confirmados futuros)
    upcoming_appointments = Appointment.objects.exclude(
        status__in=['COMPLETED', 'CANCELLED']
    ).order_by('date_time')
    
    # 3. Agendamentos de Hoje e Amanhã (Visão Geral)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    tomorrow_end = today_start + timedelta(days=2)

    appointments_hoje = Appointment.objects.filter(
        date_time__gte=today_start,
        date_time__lt=today_end
    ).exclude(status__in=['COMPLETED', 'CANCELLED']).order_by('date_time')

    appointments_amanha = Appointment.objects.filter(
        date_time__gte=today_end,
        date_time__lt=tomorrow_end
    ).exclude(status__in=['COMPLETED', 'CANCELLED']).order_by('date_time')

    portfolio_works = Work.objects.all()
    
    # Perfil e Certificações
    artist_profile = ArtistProfile.objects.first()
    certifications = Certification.objects.all()

    wa_url = request.session.pop('whatsapp_redirect', None)

    context = {
        'total_revenue': total_revenue,
        'total_tattoos': total_tattoos,
        'payment_breakdown': payment_breakdown,
        'current_month_num': current_month,
        'current_year': current_year,
        'upcoming_appointments': upcoming_appointments,
        'appointments_hoje': appointments_hoje,
        'appointments_amanha': appointments_amanha,
        'portfolio_works': portfolio_works,
        'artist_profile': artist_profile,
        'certifications': certifications,
        'whatsapp_redirect': wa_url,
        'selected_period': period,
        'period_label': period_label,
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'line_labels': json.dumps(line_labels),
        'line_data': json.dumps(line_data),
    }

    return render(request, 'billing/dashboard.html', context)

@staff_member_required
def manage_appointment(request, pk):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, pk=pk)
        
        new_status = request.POST.get('status')
        estimated_price = request.POST.get('estimated_price')
        
        # Se estiver mudando para COMPLETED e ainda não tiver ServiceRecord
        if new_status == 'COMPLETED' and appointment.status != 'COMPLETED':
            final_price = request.POST.get('final_price')
            payment_method = request.POST.get('payment_method')
            
            if final_price and payment_method:
                ServiceRecord.objects.create(
                    appointment=appointment,
                    final_price=final_price,
                    payment_method=payment_method
                )
                messages.success(request, f'Agendamento de {appointment.client.name} concluído com sucesso e faturado!')
            else:
                messages.error(request, 'Preço final e método de pagamento são obrigatórios para concluir o agendamento.')
                return redirect('billing:dashboard')
        elif new_status != 'COMPLETED':
            # Caso volte o status, talvez devesse deletar o ServiceRecord?
            # Para este MVP, vamos apenas atualizar a estimativa e status.
            messages.success(request, f'Agendamento de {appointment.client.name} atualizado.')
            
        if new_status == 'CONFIRMED' and appointment.status != 'CONFIRMED':
            # Generate WhatsApp URL
            phone = re.sub(r'\D', '', appointment.client.phone)
            if len(phone) in [10, 11]:
                phone = f"55{phone}"
                
            date_str = appointment.date_time.strftime('%d/%m/%Y')
            time_str = appointment.date_time.strftime('%H:%M')
            
            text = f"Olá, {appointment.client.name}. Passando para confirmar o seu agendamento para o dia {date_str} às {time_str}. Por favor, confirme o recebimento desta mensagem. Aguardamos você!"
            encoded_text = urllib.parse.quote(text)
            
            request.session['whatsapp_redirect'] = f"https://wa.me/{phone}?text={encoded_text}"
            
        appointment.status = new_status
        if estimated_price:
            appointment.estimated_price = estimated_price
        
        appointment.save()
        
    return redirect(reverse('billing:dashboard') + '#tab-agendamentos')

@staff_member_required
def manage_portfolio(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            category = request.POST.get('category', 'tattoo')
            image = request.FILES.get('image')
            
            if title and image:
                Work.objects.create(title=title, description=description, category=category, image=image)
                messages.success(request, 'Trabalho adicionado ao portfólio com sucesso!')
            else:
                messages.error(request, 'Título e Imagem são obrigatórios.')
                
        elif action == 'delete':
            work_id = request.POST.get('tattoo_id')
            if work_id:
                work = get_object_or_404(Work, id=work_id)
                work.image.delete() # Deleta o arquivo da imagem
                work.delete()
                messages.success(request, 'Trabalho removido do portfólio.')
                
    return redirect(reverse('billing:dashboard') + '#tab-portfolio')

@staff_member_required
def manage_profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            name = request.POST.get('name')
            bio = request.POST.get('bio')
            profile_image = request.FILES.get('profile_image')
            
            profile = ArtistProfile.objects.first()
            if not profile:
                profile = ArtistProfile(name=name, bio=bio)
            else:
                profile.name = name
                profile.bio = bio
                
            if profile_image:
                profile.profile_image = profile_image
                
            profile.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            
        elif action == 'add_cert':
            title = request.POST.get('title')
            image = request.FILES.get('image')
            
            if title and image:
                Certification.objects.create(title=title, image=image)
                messages.success(request, 'Certificação adicionada com sucesso!')
            else:
                messages.error(request, 'Título e imagem da certificação são obrigatórios.')
                
        elif action == 'delete_cert':
            cert_id = request.POST.get('cert_id')
            if cert_id:
                cert = get_object_or_404(Certification, id=cert_id)
                cert.image.delete()
                cert.delete()
                messages.success(request, 'Certificação removida.')
                
    return redirect(reverse('billing:dashboard') + '#tab-perfil')

@staff_member_required
def consent_pdf(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'billing/consent_pdf.html', {'appointment': appointment})

