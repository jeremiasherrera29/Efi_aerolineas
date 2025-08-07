from django.urls import path
from . import views
from .views import (
    VueloList, VueloDetail, VueloDelete, VueloCreate,
    PasajeroList, PasajeroDetail, PasajeroDelete, PasajeroCreate,
    ReservaList, ReservaDetail, ReservaDelete, ReservaCreate,
    BoletoList, BoletoDetail, BoletoDelete, BoletoCreate,
    UsuarioList, UsuarioDelete, UsuarioCreate, UsuarioUpdate,
    AvionList, AvionDetail, AvionDelete, AvionCreate,
    AsientoList, AsientoDetail, AsientoDelete, AsientoCreate,
)

urlpatterns = [
    path('vuelos/<int:vuelo_id>/pasajeros/', views.pasajeros_por_vuelo, name='pasajeros_por_vuelo'),
    # Vuelos   
    path('vuelos/', VueloList.as_view(), name='vuelos_list'),
    path('vuelos/<int:vuelo_id>/', VueloDetail.as_view(), name='vuelos_detail'),
    path('vuelos/<int:vuelo_id>/eliminar/', VueloDelete.as_view(), name='vuelos_delete'),
    path('vuelos/crear/', VueloCreate.as_view(), name='vuelos_create'),

    # Pasajeros
    path('pasajeros/', PasajeroList.as_view(), name='pasajeros_list'),
    path('pasajeros/<int:pasajero_id>/', PasajeroDetail.as_view(), name='pasajeros_detail'),
    path('pasajeros/<int:pasajero_id>/eliminar/', PasajeroDelete.as_view(), name='pasajeros_delete'),
    path('pasajeros/crear/', PasajeroCreate.as_view(), name='pasajeros_create'),

    # Reservas
    path('reservas/', ReservaList.as_view(), name='reservas_list'),
    path('reservas/<int:reserva_id>/', ReservaDetail.as_view(), name='reservas_detail'),
    path('reservas/<int:reserva_id>/eliminar/', ReservaDelete.as_view(), name='reservas_delete'),
    path('reservas/crear/', ReservaCreate.as_view(), name='reservas_create'),

    # Boletos
    path('boletos/', BoletoList.as_view(), name='boletos_list'),
    path('boletos/<int:boleto_id>/', BoletoDetail.as_view(), name='boletos_detail'),
    path('boletos/<int:boleto_id>/eliminar/', BoletoDelete.as_view(), name='boletos_delete'),
    path('boletos/crear/', BoletoCreate.as_view(), name='boletos_create'),

    # Usuarios
    path('usuarios/', UsuarioList.as_view(), name='usuarios_list'),
    path('usuarios/<int:usuario_id>/eliminar/', UsuarioDelete.as_view(), name='usuarios_delete'),
    path('usuarios/crear/', UsuarioCreate.as_view(), name='usuarios_create'),
    path('usuarios/<int:usuario_id>/editar/', UsuarioUpdate.as_view(), name='usuarios_update'),

    # Aviones
    path('aviones/', AvionList.as_view(), name='aviones_list'),
    path('aviones/<int:avion_id>/', AvionDetail.as_view(), name='aviones_detail'),
    path('aviones/<int:avion_id>/eliminar/', AvionDelete.as_view(), name='aviones_delete'),
    path('aviones/crear/', AvionCreate.as_view(), name='aviones_create'),

    # Asientos
    path('asientos/', AsientoList.as_view(), name='asientos_list'),
    path('asientos/<int:asiento_id>/', AsientoDetail.as_view(), name='asientos_detail'),
    path('asientos/<int:asiento_id>/eliminar/', AsientoDelete.as_view(), name='asientos_delete'),
    path('asientos/crear/', AsientoCreate.as_view(), name='asientos_create'),
]
