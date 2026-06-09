from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Perfil, OfertaLaboral, Postulacion, Contacto
from .forms import RegistroForm, LoginForm, PerfilForm, PostulacionForm, ContactoForm

def home_view(request):
    ofertas_recientes = OfertaLaboral.objects.filter(activa=True)[:3]
    total_ofertas = OfertaLaboral.objects.filter(activa=True).count()
    return render(request, 'portal/home.html', {
        'ofertas_recientes': ofertas_recientes,
        'total_ofertas': total_ofertas,
    })
    
def registro_view(request):
    if request.user.is_authenticated:
        return redirect('lista_ofertas')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user)
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name}!')
            return redirect('lista_ofertas')
    else:
        form = RegistroForm()

    return render(request, 'portal/registro.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('lista_ofertas')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola, {user.username}!')
            return redirect('lista_ofertas')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm(request)

    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Cerraste sesión.')
    return redirect('login')

@login_required
def ver_perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    postulaciones = Postulacion.objects.filter(usuario=request.user).select_related('oferta')
    return render(request, 'portal/ver_perfil.html', {
        'perfil': perfil,
        'postulaciones': postulaciones,
    })


@login_required
def editar_perfil_view(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('ver_perfil')
    else:
        form = PerfilForm(instance=perfil)

    return render(request, 'portal/editar_perfil.html', {'form': form})

@login_required
def lista_ofertas_view(request):
    ofertas = OfertaLaboral.objects.filter(activa=True)
    ya_postuladas = set(
        Postulacion.objects.filter(usuario=request.user).values_list('oferta_id', flat=True)
    )
    return render(request, 'portal/lista_ofertas.html', {
        'ofertas': ofertas,
        'ya_postuladas': ya_postuladas,
    })


@login_required
def detalle_oferta_view(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk, activa=True)
    ya_postulo = Postulacion.objects.filter(usuario=request.user, oferta=oferta).exists()
    return render(request, 'portal/detalle_oferta.html', {
        'oferta': oferta,
        'ya_postulo': ya_postulo,
    })


@login_required
def postular_view(request, pk):
    oferta = get_object_or_404(OfertaLaboral, pk=pk, activa=True)

    if Postulacion.objects.filter(usuario=request.user, oferta=oferta).exists():
        messages.warning(request, 'Ya postulaste a esta oferta.')
        return redirect('detalle_oferta', pk=pk)

    if request.method == 'POST':
        form = PostulacionForm(request.POST)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.usuario = request.user
            postulacion.oferta = oferta
            postulacion.save()
            messages.success(request, '¡Postulación enviada!')
            return redirect('mis_postulaciones')
    else:
        form = PostulacionForm()

    return render(request, 'portal/postular.html', {
        'oferta': oferta,
        'form': form,
    })


@login_required
def mis_postulaciones_view(request):
    postulaciones = Postulacion.objects.filter(
        usuario=request.user
    ).select_related('oferta')
    return render(request, 'portal/mis_postulaciones.html', {
        'postulaciones': postulaciones,
    })
    
def contacto_view(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado! Te responderemos pronto.')
            return redirect('contacto')
    else:
        form = ContactoForm()

    return render(request, 'portal/contacto.html', {'form': form})