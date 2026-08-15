from django.db import models
from scheduling.models import Appointment

class ServiceRecord(models.Model):
    PAYMENT_CHOICES = [
        ('PIX', 'PIX'),
        ('CREDIT', 'Cartão de Crédito'),
        ('DEBIT', 'Cartão de Débito'),
        ('CASH', 'Dinheiro'),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='service_record', verbose_name="Agendamento")
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço Final Cobrado (R$)")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="Método de Pagamento")
    date_completed = models.DateTimeField(auto_now_add=True, verbose_name="Data de Conclusão")

    def __str__(self):
        return f"Serviço - {self.appointment.client.name} - R${self.final_price}"

    class Meta:
        verbose_name = "Registro de Serviço"
        verbose_name_plural = "Registros de Serviços"
        ordering = ['-date_completed']
