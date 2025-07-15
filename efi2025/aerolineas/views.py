from django.shortcuts import render

from .models import Usuario, Vuelo, Reserva, Pasajero, Boleto, Avion, Asiento
from django.shortcuts import render
# Create your views here.

def vuelos_list(request):
    vuelos = Vuelo.objects.all()
    return render(request, "vuelos/list.html", {'vuelos': vuelos})

def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/list.html', {'usuarios': usuarios})

def reservas_list(request):
    reservas = Reserva.objects.all()
    return render(request, "reservas/list.html", {'reservas': reservas})

def pasajeros_list(request):
    pasajeros = Pasajero.objects.all()
    return render(request, "pasajeros/list.html", {'pasajeros': pasajeros})

def boletos_list(request):
    boletos = Boleto.objects.all()
    return render(request, "boletos/list.html", {'boletos': boletos})

def aviones_list(request):
    aviones = Avion.objects.all()
    return render(request, "aviones/list.html", {'aviones': aviones})

def asientos_list(request):
    asientos = Asiento.objects.all()
    return render(request, "asientos/list.html", {'asientos': asientos})