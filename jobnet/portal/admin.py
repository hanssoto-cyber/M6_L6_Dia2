from django.contrib import admin
from .models import Perfil, OfertaLaboral, Postulacion, Contacto


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cargo_actual', 'ciudad', 'annos_experiencia']
    search_fields = ['usuario__username', 'usuario__first_name', 'cargo_actual']


@admin.register(OfertaLaboral)
class OfertaLaboralAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'modalidad', 'activa', 'publicada_en']
    list_filter = ['activa', 'modalidad']
    list_editable = ['activa']
    search_fields = ['titulo', 'empresa']


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'oferta', 'estado', 'fecha_postulacion']
    list_filter = ['estado']
    list_editable = ['estado']
    search_fields = ['usuario__username', 'oferta__titulo']


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'enviado_en']
    list_filter = ['asunto']
    search_fields = ['nombre', 'email']