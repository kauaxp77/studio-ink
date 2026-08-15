from django.db import models
from tattoo_studio.utils import convert_image_to_webp

class Client(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome Completo")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefone/WhatsApp")
    instagram_handle = models.CharField(max_length=50, blank=True, verbose_name="Instagram (@)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendente (Aguardando Aprovação)'),
        ('CONFIRMED', 'Confirmado'),
        ('COMPLETED', 'Concluído'),
        ('CANCELLED', 'Cancelado'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='appointments', verbose_name="Cliente")
    date_time = models.DateTimeField(verbose_name="Data e Hora")
    description = models.TextField(verbose_name="Detalhes da Tatuagem (Tamanho, local, ideia)")
    reference_image = models.ImageField(upload_to='references/', blank=True, null=True, verbose_name="Imagem de Referência")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço Estimado (R$)")

    def save(self, *args, **kwargs):
        if self.reference_image:
            convert_image_to_webp(self.reference_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.name} - {self.date_time.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ['date_time']
