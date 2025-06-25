from django.contrib import admin

# Register your models here.

from aerolineas.models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto, Usuario

@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ("id", "modelo", "capacidad","filas","columnas")
    list_filter = ("modelo", "capacidad","filas","columnas")
    search_fields = ("modelo",)

@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ("id", "avion", "origen","destino","fecha_salida","fecha_llegada","duracion","estado", "precio_base")
    list_filter = ("avion", "origen","destino","fecha_salida","fecha_llegada","duracion","estado")
    search_fields = ("avion","destino","duracion","fecha_salida")

@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "documento","email","telefono", "fecha_nacimiento", "tipo_documento")
    list_filter = ("nombre", "documento","telefono")
    search_fields = ("nombre","documento","telefono")

@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ("id", "avion", "numero","fila","columna", "tipo", "estado")
    list_filter = ("avion", "estado", "fila","columna")
    search_fields = ("avion","numero",)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ("id", "vuelo", "pasajero","asiento","estado", "fecha_reserva", "precio", "codigo_reserva")
    list_filter = ("vuelo", "fecha_reserva", "pasajero","estado")
    search_fields = ("vuelo","pasajero")

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ("id", "reserva","codigo_barra", "fecha_emision","estado")
    list_filter = ("reserva","estado")
    search_fields = ("reserva","fecha_emision")

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "username","password", "email","rol")
    list_filter = ("username","rol")
    search_fields = ("username","email")




