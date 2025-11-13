from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Vuelo, Reserva, Pasajero, Boleto, Usuario, Avion, Asiento

# FORMULARIOS PRINCIPALES

class VueloForm(forms.ModelForm):
    class Meta:
        model = Vuelo
        fields = ["avion", "origen", "destino", "fecha_salida", "fecha_llegada", "duracion", "estado", "precio_base"]
        widgets = {
            'avion': forms.Select(attrs={'class': 'form-control'}),
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_llegada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HH:MM:SS'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ["vuelo", "pasajero", "asiento", "precio", "estado"]
        widgets = {
            'vuelo': forms.Select(attrs={'class': 'form-control'}),
            'pasajero': forms.Select(attrs={'class': 'form-control'}),
            'asiento': forms.Select(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        vuelo = cleaned.get('vuelo')
        pasajero = cleaned.get('pasajero')
        asiento = cleaned.get('asiento')

        if vuelo and asiento:
            if asiento.avion_id != vuelo.avion_id:
                raise ValidationError("El asiento no pertenece al avión del vuelo seleccionado.")

        if vuelo and pasajero:
            if Reserva.objects.filter(vuelo=vuelo, pasajero=pasajero, estado__in=['Confirmado', 'Pendiente']).exists():
                raise ValidationError("Este pasajero ya tiene una reserva para este vuelo.")

        if asiento and asiento.estado != 'Disponible':
            raise ValidationError("El asiento no está disponible.")

        return cleaned

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ["nombre", "documento", "email", "telefono", "fecha_nacimiento", "tipo_documento"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'documento': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
        }

class BoletoForm(forms.ModelForm):
    class Meta:
        model = Boleto
        fields = ["reserva", "codigo_barra", "fecha_emision", "estado"]
        widgets = {
            'reserva': forms.Select(attrs={'class': 'form-control'}),
            'codigo_barra': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class UsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=""
    )
    password2 = forms.CharField(
        label="Repetir contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text=""
    )

    class Meta:
        model = Usuario
        fields = ["username", "email", "rol"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "rol": forms.Select(attrs={"class": "form-select"}),
        }
        help_texts = {
            "username": "",
            "email": "",
            "rol": "",
        }
        def save(self, commit=True):
            user = super().save(commit=False)
            user.rol = self.cleaned_data["rol"]

            if commit:
                user.save()

            return user
class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ["modelo", "capacidad", "filas", "columnas"]
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'filas': forms.NumberInput(attrs={'class': 'form-control'}),
            'columnas': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AsientoForm(forms.ModelForm):
    class Meta:
        model = Asiento
        fields = ["avion", "numero", "fila", "columna", "tipo", "estado"]
        widgets = {
            'avion': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fila': forms.NumberInput(attrs={'class': 'form-control'}),
            'columna': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
