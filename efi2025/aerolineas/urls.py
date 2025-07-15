from django.urls import path

from aerolineas.views import vuelos_list, usuarios_list, reservas_list, pasajeros_list, boletos_list, aviones_list, asientos_list

urlpatterns = [
    path("vuelos/list/", vuelos_list, name="vuelos_list"),
    path("usuarios/list/", usuarios_list, name="usuarios_list"),
    path("reservas/list/", reservas_list, name="reservas_list"),
    path("pasajeros/list/", pasajeros_list, name="pasajeros_list"),
    path("boletos/list/", boletos_list, name="boletos_list"),
    path("aviones/list/", aviones_list, name="aviones_list"),
    path("asientos/list/", asientos_list, name="asientos_list"),
]   