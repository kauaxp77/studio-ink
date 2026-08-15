from django.db import models

class Work(models.Model):
    CATEGORY_CHOICES = [
        ('tattoo', 'Tatuagem'),
        ('piercing', 'Piercing'),
    ]

    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tattoo', verbose_name="Categoria")
    image = models.ImageField(upload_to='portfolio_images/', verbose_name="Imagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado em")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Trabalho"
        verbose_name_plural = "Trabalhos"
        ordering = ['-created_at']

class ArtistProfile(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome Artístico", default="Tatuador")
    bio = models.TextField(verbose_name="Biografia (Sobre Mim)")
    profile_image = models.ImageField(upload_to='artist_images/', verbose_name="Foto de Perfil")
    
    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = "Perfil do Artista"
        verbose_name_plural = "Perfil do Artista"

class Certification(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título da Certificação")
    image = models.ImageField(upload_to='certifications/', verbose_name="Imagem do Certificado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Adicionado em")
    
    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = "Certificação"
        verbose_name_plural = "Certificações"
        ordering = ['-created_at']
