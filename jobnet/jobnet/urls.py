from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portal import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Públicas
    path('', views.home_view, name='home'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contacto/', views.contacto_view, name='contacto'),

    # Perfil
    path('perfil/', views.ver_perfil_view, name='ver_perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),

    # Ofertas
    path('ofertas/', views.lista_ofertas_view, name='lista_ofertas'),
    path('ofertas/<int:pk>/', views.detalle_oferta_view, name='detalle_oferta'),
    path('ofertas/<int:pk>/postular/', views.postular_view, name='postular'),

    # Postulaciones
    path('mis-postulaciones/', views.mis_postulaciones_view, name='mis_postulaciones'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)