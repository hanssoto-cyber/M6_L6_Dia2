from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Perfil, Postulacion, Contacto


class RegistroForm(forms.Form):
    first_name = forms.CharField(label='Nombre', max_length=150)
    last_name = forms.CharField(label='Apellido', max_length=150)
    username = forms.CharField(label='Usuario', max_length=150)
    email = forms.EmailField(label='Correo')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este usuario ya existe.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Las contraseñas no coinciden.')
        return cleaned_data

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password1'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        exclude = ['usuario']
        widgets = {
            'resumen': forms.Textarea(attrs={'rows': 4}),
            'habilidades': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'telefono': 'Teléfono',
            'ciudad': 'Ciudad',
            'resumen': 'Resumen profesional',
            'habilidades': 'Habilidades (separadas por coma)',
            'cargo_actual': 'Cargo actual',
            'annos_experiencia': 'Años de experiencia',
        }
        
class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['carta_presentacion']
        labels = {
            'carta_presentacion': 'Carta de presentación (opcional)',
        }
        widgets = {
            'carta_presentacion': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Preséntate y explica por qué eres el candidato ideal...'
            }),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'asunto', 'mensaje', 'archivo_adjunto']
        labels = {
            'nombre': 'Nombre completo',
            'email': 'Correo electrónico',
            'asunto': 'Asunto',
            'mensaje': 'Mensaje',
            'archivo_adjunto': 'Archivo adjunto (opcional)',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 6}),
        }