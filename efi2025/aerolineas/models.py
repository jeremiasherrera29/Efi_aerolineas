from django.db import models
from django.utils import timezone

# Create your models here.
class Avion(models.Model):
    modelo = models.CharField(max_length=200)
    capacidad = models.PositiveIntegerField()
    filas = models.PositiveIntegerField()
    columnas = models.PositiveIntegerField()

    def __str__(self):
        return self.modelo

class Vuelo(models.Model):
    ESTADOS_VUELO = [
        ('PRG', 'Programado'), # Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('ABR', 'Abordando'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('DES', 'Despegado'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('ENR', 'En ruta'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('ARR', 'Aterrizado'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('RET', 'Retrasado'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('CNL', 'Cancelado'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
        ('DESV', 'Desviado'),# Primer valor: se muestra en la base de datos, segundo valor: lo que ve el usuario
    ]
    avion = models.ForeignKey(
        Avion,
        on_delete=models.CASCADE
    ) #FK
    origen = models.CharField(max_length=200)
    destino = models.CharField(max_length=200)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
    duracion = models.DurationField()
    estado = models.CharField(max_length=200, choices=ESTADOS_VUELO) #Busca las opciones de ESTADOS_VUELO para que el usuario no escriba cualquier cosa
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Origen: {self.origen} - Destino: {self.destino}"


class Pasajero(models.Model):
    DOCUMENTO = [
        ("DNI", "Documento"),
        ("CUIL", "Cuil"),
        ("CARCOND", "Carnet Conducir")
    ]
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    tipo_documento = models.CharField(max_length=200, choices=DOCUMENTO)#Busca las opciones de DOCUMENTO para que el usuario no escriba cualquier cosa
    
    def __str__(self):
        return f"Nombre: {self.nombre} - Documento: {self.documento}"
    

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
    avion = models.ForeignKey(
        Avion,
        on_delete=models.CASCADE
    ) #FK
    numero = models.CharField(max_length=100)
    fila = models.PositiveIntegerField()
    columna = models.PositiveIntegerField()
    tipo = models.CharField(max_length=100, choices= TIPO_ASIENTO)
    estado = models.CharField(max_length=60, choices=ESTADOS_ASIENTO)# Busca las opciones de ESTADOS_ASIENTO para que el usuario no escriba cualquier cosa

    def __str__(self):
        return f"Avion: {self.avion} - Numero: {self.numero}"
    
class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ("confirmado", "Confirmado"),
        ("pendiente", "Pendiente"),
        ("cancelado", "Cancelado")
    ]
    vuelo = models.ForeignKey(
        Vuelo,
        on_delete=models.CASCADE
    ) #FK)
    pasajero = models.ForeignKey(
        Pasajero,
        on_delete=models.CASCADE
    ) #FK)
    asiento = models.ForeignKey(
        Asiento,
        on_delete=models.CASCADE
    ) #FK)
    estado = models.CharField(max_length=60, choices=ESTADOS_RESERVA)
    fecha_reserva = models.DateTimeField(default=timezone.now)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_reserva = models.CharField(max_length=100)

    def __str__(self):
        return f"Reserva: {self.codigo_reserva} - Pasajero: {self.pasajero}"
    
class Usuario(models.Model):
    ROLES = [
        ('ADM', 'Administrador'),
        ('EMP', 'Empleado'),
        ('PAS', 'Pasajero'),
    ]
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=120)
    email = models.EmailField()
    rol = models.CharField(max_length=50, choices=ROLES)

    def __str__(self):
        return f"Usuario: {self.username} - Rol: {self.rol}"
    
class Boleto(models.Model):
    ESTADOS_BOLETO = [
        ('emitido', 'Emitido'),
        ('cancelado', 'Cancelado'),
        ('usado', 'Usado'),
    ]

    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE
    )
    codigo_barra = models.CharField(max_length=50)
    fecha_emision = models.DateTimeField()
    estado = models.CharField(max_length=50, choices=ESTADOS_BOLETO)

    def __str__(self):
        return f"Boleto: {self.codigo_barra}"
