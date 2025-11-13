from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


#   MODELOS PRINCIPALES

class Avion(models.Model):
    modelo = models.CharField(max_length=200)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()

    def __str__(self):
        return self.modelo


class Vuelo(models.Model):
    ESTADOS_VUELO = [
        ('PRG', 'Programado'),
        ('ABR', 'Abordando'),
        ('DES', 'Despegado'),
        ('ENR', 'En ruta'),
        ('ARR', 'Aterrizado'),
        ('RET', 'Retrasado'),
        ('CNL', 'Cancelado'),
        ('DESV', 'Desviado'),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    origen = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    estado = models.CharField(max_length=200, choices=ESTADOS_VUELO)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Origen: {self.origen} - Destino: {self.destino}"


class Pasajero(models.Model):
    DOCUMENTO = [
        ("DNI", "Documento Nacional de Identidad"),
        ("CUIL", "CUIL"),
        ("CARCOND", "Carnet de Conducir"),
    ]
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='pasajero'
    )
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    tipo_documento = models.CharField(max_length=200, choices=DOCUMENTO)

    def __str__(self):
        return f"{self.nombre} ({self.documento})"


class Asiento(models.Model):
    TIPO_ASIENTO = [
        ('ECO', 'Económica'),
        ('PRE', 'Premium'),
        ('BUS', 'Ejecutiva'),
        ('FIR', 'Primera Clase'),
    ]
    ESTADOS_ASIENTO = [
        ("Disponible", "Disponible"),
        ("Ocupado", "Ocupado")
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    numero = models.CharField(max_length=100)
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100, choices=TIPO_ASIENTO)
    estado = models.CharField(max_length=60, choices=ESTADOS_ASIENTO, default="Disponible")

    def __str__(self):
        return f"Asiento {self.numero} ({self.tipo}) - {self.estado}"


class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ("confirmado", "Confirmado"),
        ("pendiente", "Pendiente"),
        ("cancelado", "Cancelado"),
    ]

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    estado = models.CharField(max_length=60, choices=ESTADOS_RESERVA)
    fecha_reserva = models.DateTimeField(default=timezone.now)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_reserva = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Reserva {self.codigo_reserva} - {self.pasajero}"

    def save(self, *args, **kwargs):
        # Generar un código único si no existe
        if not self.codigo_reserva:
            self.codigo_reserva = str(uuid.uuid4())[:8].upper()

        super().save(*args, **kwargs)

        # Crear boleto si la reserva está confirmada
        if self.estado.lower() == "confirmado":
            from .models import Boleto
            if not Boleto.objects.filter(reserva=self).exists():
                Boleto.objects.create(
                    reserva=self,
                    codigo_barra=str(uuid.uuid4())[:8],
                    fecha_emision=timezone.now(),
                    estado="emitido"
                )

#   USUARIO PERSONALIZADO
class Usuario(AbstractUser):
    ROLES = [
        ('ADM', 'Administrador'),
        ('EMP', 'Empleado'),
        ('PAS', 'Pasajero'),
    ]
    
    rol = models.CharField(max_length=50, choices=ROLES, default='PAS')

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
#   BOLETO

class Boleto(models.Model):
    ESTADOS_BOLETO = [
        ('emitido', 'Emitido'),
        ('cancelado', 'Cancelado'),
        ('usado', 'Usado'),
    ]

    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    codigo_barra = models.CharField(max_length=50, unique=True)
    fecha_emision = models.DateTimeField()
    estado = models.CharField(max_length=50, choices=ESTADOS_BOLETO)

    def __str__(self):
        return f"Boleto {self.codigo_barra} - {self.estado}"
