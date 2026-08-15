from django import forms
from .models import Client, Appointment

class AppointmentRequestForm(forms.ModelForm):
    # Campos do cliente
    client_name = forms.CharField(max_length=150, label="Nome Completo", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Seu nome completo'}))
    client_email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'seu@email.com'}))
    client_phone = forms.CharField(max_length=20, label="WhatsApp", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(XX) XXXXX-XXXX'}))
    client_instagram = forms.CharField(max_length=50, required=False, label="Instagram (@)", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '@seuinux'}))

    class Meta:
        model = Appointment
        fields = ['date_time', 'description', 'reference_image']
        widgets = {
            'date_time': forms.TextInput(attrs={'class': 'form-input flatpickr-input', 'placeholder': 'Selecione uma data e horário...'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Descreva sua ideia, tamanho aproximado, local do corpo...'}),
            'reference_image': forms.FileInput(attrs={'class': 'form-input file-input'})
        }
    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            # Prevent double booking in the backend
            if Appointment.objects.filter(date_time=date_time).exclude(status='CANCELLED').exists():
                raise forms.ValidationError("Desculpe, este horário acabou de ser reservado. Por favor, escolha outro.")
        return date_time

    def save(self, commit=True):
        # Primeiro, cria ou atualiza o cliente
        client, created = Client.objects.get_or_create(
            email=self.cleaned_data['client_email'],
            defaults={
                'name': self.cleaned_data['client_name'],
                'phone': self.cleaned_data['client_phone'],
                'instagram_handle': self.cleaned_data['client_instagram'],
            }
        )
        
        # Se o cliente já existia, podemos querer atualizar os outros dados
        if not created:
            client.name = self.cleaned_data['client_name']
            client.phone = self.cleaned_data['client_phone']
            if self.cleaned_data['client_instagram']:
                client.instagram_handle = self.cleaned_data['client_instagram']
            client.save()

        # Depois, cria o agendamento
        appointment = super().save(commit=False)
        appointment.client = client
        appointment.status = 'PENDING'
        
        if commit:
            appointment.save()
        return appointment
