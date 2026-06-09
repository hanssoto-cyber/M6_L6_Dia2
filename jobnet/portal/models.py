from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    resumen = models.TextField(blank=True)
    habilidades = models.TextField(blank=True)
    cargo_actual = models.CharField(max_length=200, blank=True)
    annos_experiencia = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'

class OfertaLaboral(models.Model):
    MODALIDAD_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    descripcion = models.TextField()
    requisitos = models.TextField()
    habilidades_requeridas = models.TextField(blank=True)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES, default='presencial')
    salario_min = models.PositiveIntegerField(null=True, blank=True)
    salario_max = models.PositiveIntegerField(null=True, blank=True)
    activa = models.BooleanField(default=True)
    publicada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} — {self.empresa}'
    
class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('enviada', 'Enviada'),
        ('en_revision', 'En revisión'),
        ('entrevista', 'Entrevista agendada'),
        ('rechazada', 'Rechazada'),
        ('seleccionada', 'Seleccionada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postulaciones')
    oferta = models.ForeignKey(OfertaLaboral, on_delete=models.CASCADE, related_name='postulaciones')
    carta_presentacion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='enviada')
    fecha_postulacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'oferta')

    def __str__(self):
        return f'{self.usuario.username} → {self.oferta.titulo}'
    
class Contacto(models.Model):
    ASUNTO_CHOICES = [
        ('consulta', 'Consulta general'),
        ('empresa', 'Quiero publicar una oferta'),
        ('problema', 'Reportar un problema'),
        ('sugerencia', 'Sugerencia de mejora'),
    ]

    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    asunto = models.CharField(max_length=20, choices=ASUNTO_CHOICES, default='consulta')
    mensaje = models.TextField()
    archivo_adjunto = models.FileField(upload_to='contacto/', blank=True, null=True)
    enviado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} — {self.get_asunto_display()}'