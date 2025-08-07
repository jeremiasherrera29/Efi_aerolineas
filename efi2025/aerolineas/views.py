from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .models import Vuelo, Reserva, Pasajero, Boleto, Usuario, Avion, Asiento
from .forms import VueloForm, ReservaForm, PasajeroForm, BoletoForm, UsuarioForm, AvionForm, AsientoForm

# --- VUELO ---
class VueloList(ListView):
    model = Vuelo
    template_name = 'vuelos/list.html'
    context_object_name = 'vuelos'

class VueloDetail(DetailView):
    model = Vuelo
    template_name = 'vuelos/detail.html'
    context_object_name = 'vuelo'
    pk_url_kwarg = 'vuelo_id'

class VueloDelete(DeleteView):
    model = Vuelo
    template_name = "vuelos/delete.html"
    pk_url_kwarg = 'vuelo_id'
    success_url = reverse_lazy('vuelos_list')

class VueloCreate(CreateView):
    form_class = VueloForm
    template_name = 'vuelos/create.html'
    success_url = reverse_lazy('vuelos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Vuelo'
        return context

# --- PASAJERO ---
class PasajeroList(ListView):
    model = Pasajero
    template_name = 'pasajeros/list.html'
    context_object_name = 'pasajeros'

class PasajeroDetail(DetailView):
    model = Pasajero
    template_name = 'pasajeros/detail.html'
    context_object_name = 'pasajero'
    pk_url_kwarg = 'pasajero_id'

class PasajeroDelete(DeleteView):
    model = Pasajero
    template_name = "pasajeros/delete.html"
    pk_url_kwarg = 'pasajero_id'
    success_url = reverse_lazy('pasajeros_list')

class PasajeroCreate(CreateView):
    form_class = PasajeroForm
    template_name = 'pasajeros/create.html'
    success_url = reverse_lazy('pasajeros_list')

# --- RESERVA ---
class ReservaList(ListView):
    model = Reserva
    template_name = 'reservas/list.html'
    context_object_name = 'reservas'

class ReservaDetail(DetailView):
    model = Reserva
    template_name = 'reservas/detail.html'
    context_object_name = 'reserva'
    pk_url_kwarg = 'reserva_id'

class ReservaDelete(DeleteView):
    model = Reserva
    template_name = "reservas/delete.html"
    pk_url_kwarg = 'reserva_id'
    success_url = reverse_lazy('reservas_list')

class ReservaCreate(CreateView):
    form_class = ReservaForm
    template_name = 'reservas/create.html'
    success_url = reverse_lazy('reservas_list')

# --- BOLETO ---
class BoletoList(ListView):
    model = Boleto
    template_name = 'boletos/list.html'
    context_object_name = 'boletos'

class BoletoDetail(DetailView):
    model = Boleto
    template_name = 'boletos/detail.html'
    context_object_name = 'boleto'
    pk_url_kwarg = 'boleto_id'

class BoletoDelete(DeleteView):
    model = Boleto
    template_name = "boletos/delete.html"
    pk_url_kwarg = 'boleto_id'
    success_url = reverse_lazy('boletos_list')

class BoletoCreate(CreateView):
    form_class = BoletoForm
    template_name = 'boletos/create.html'
    success_url = reverse_lazy('boletos_list')

# --- USUARIO ---
class UsuarioList(ListView):
    model = Usuario
    template_name = 'usuarios/list.html'
    context_object_name = 'usuarios'

class UsuarioDelete(DeleteView):
    model = Usuario
    template_name = "usuarios/delete.html"
    pk_url_kwarg = 'usuario_id'
    success_url = reverse_lazy('usuarios_list')

class UsuarioCreate(CreateView):
    form_class = UsuarioForm
    template_name = 'usuarios/create.html'
    success_url = reverse_lazy('usuarios_list')
    

class UsuarioUpdate(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuarios/upgrade.html'
    pk_url_kwarg = 'usuario_id'
    success_url = reverse_lazy('usuarios_list')


# --- AVION ---
class AvionList(ListView):
    model = Avion
    template_name = 'aviones/list.html'
    context_object_name = 'aviones'

class AvionDetail(DetailView):
    model = Avion
    template_name = 'aviones/detail.html'
    context_object_name = 'avion'
    pk_url_kwarg = 'avion_id'

class AvionDelete(DeleteView):
    model = Avion
    template_name = "aviones/delete.html"
    pk_url_kwarg = 'avion_id'
    success_url = reverse_lazy('aviones_list')

class AvionCreate(CreateView):
    form_class = AvionForm
    template_name = 'aviones/create.html'
    success_url = reverse_lazy('aviones_list')

# --- ASIENTO ---
class AsientoList(ListView):
    model = Asiento
    template_name = 'asientos/list.html'
    context_object_name = 'asientos'

class AsientoDetail(DetailView):
    model = Asiento
    template_name = 'asientos/detail.html'
    context_object_name = 'asiento'
    pk_url_kwarg = 'asiento_id'

class AsientoDelete(DeleteView):
    model = Asiento
    template_name = "asientos/delete.html"
    pk_url_kwarg = 'asiento_id'
    success_url = reverse_lazy('asientos_list')

class AsientoCreate(CreateView):
    form_class = AsientoForm
    template_name = 'asientos/create.html'
    success_url = reverse_lazy('asientos_list')

#-- PASAJERO_POR_VUELO --#

def pasajeros_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    pasajeros = Pasajero.objects.filter(reserva__vuelo=vuelo).distinct()

    return render(request, 'reportes/pasajeros_por_vuelo.html', {'vuelo': vuelo,'pasajeros': pasajeros,})