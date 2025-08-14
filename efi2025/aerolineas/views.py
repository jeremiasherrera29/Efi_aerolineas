from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
import uuid
from django.contrib.auth.decorators import login_required

from .models import Vuelo, Reserva, Pasajero, Boleto, Usuario, Avion, Asiento
from .forms import VueloForm, ReservaForm, PasajeroForm, BoletoForm, UsuarioForm, AvionForm, AsientoForm


# ---------- VUELOS ----------
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


# ---------- PASAJEROS ----------
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

class HistorialVuelosPasajero(ListView):
    model = Reserva
    template_name = 'pasajeros/historial.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        pasajero_id = self.kwargs['pasajero_id']
        return Reserva.objects.filter(pasajero__id=pasajero_id).order_by('-fecha_reserva')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pasajero'] = Pasajero.objects.get(id=self.kwargs['pasajero_id'])
        return context

# ---------- RESERVAS ----------
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

def reporte_pasajeros_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    pasajeros = Pasajero.objects.filter(reserva__vuelo=vuelo)
    return render(request, "aerolineas/reporte_pasajeros_por_vuelo.html", {
        "vuelo": vuelo,
        "pasajeros": pasajeros
    })

@login_required
def reservar_asiento(request, vuelo_id, asiento_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asiento = get_object_or_404(Asiento, id=asiento_id, vuelo=vuelo)

    # Obtener pasajero asociado al usuario autenticado
    try:
        pasajero = request.user.pasajero
    except Pasajero.DoesNotExist:
        messages.error(request, "No tienes un perfil de pasajero asociado. Por favor crea uno antes de reservar.")
        return redirect('crear_pasajero')

    # Crear reserva
    Reserva.objects.create(vuelo=vuelo, asiento=asiento, pasajero=pasajero)
    asiento.disponible = False
    asiento.save()

    messages.success(request, "Reserva realizada con éxito.")
    return redirect('detalle_vuelo', pk=vuelo.id)

# ---------- BOLETOS ----------
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


# ---------- USUARIOS ----------
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
    template_name = 'usuarios/update.html'
    pk_url_kwarg = 'usuario_id'
    success_url = reverse_lazy('usuarios_list')


# ---------- AVIONES ----------
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


# ---------- ASIENTOS ----------
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


# ---------- DISPONIBILIDAD Y RESERVAS ----------
def disponibilidad_asientos(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos = Asiento.objects.filter(avion=vuelo.avion).order_by('fila', 'columna')

    filas = {}
    for asiento in asientos:
        filas.setdefault(asiento.fila, []).append(asiento)

    pasajeros = Pasajero.objects.all()  # IMPORTANTE

    return render(request, 'asientos/disponibilidad.html', {
        'vuelo': vuelo,
        'filas': filas,
        'pasajeros': pasajeros
    })

def reservar_asiento(request, vuelo_id, asiento_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asiento = get_object_or_404(Asiento, id=asiento_id)

    if asiento.estado != "Disponible":
        messages.error(request, "El asiento ya está ocupado.")
        return redirect('disponibilidad_asientos', vuelo_id=vuelo.id)

    pasajero_id = request.POST.get("pasajero_id")
    if not pasajero_id:
        messages.error(request, "Debes seleccionar un pasajero.")
        return redirect('disponibilidad_asientos', vuelo_id=vuelo.id)

    pasajero = get_object_or_404(Pasajero, id=pasajero_id)

    codigo_reserva = str(uuid.uuid4())[:8]

    reserva = Reserva.objects.create(
        vuelo=vuelo,
        pasajero=pasajero,
        asiento=asiento,
        estado="Confirmado",
        fecha_reserva=timezone.now(),
        precio=vuelo.precio_base,
        codigo_reserva=codigo_reserva
    )

    asiento.estado = "Ocupado"
    asiento.save()

    Boleto.objects.create(
        reserva=reserva,
        codigo_barra=str(uuid.uuid4())[:12],
        fecha_emision=timezone.now(),
        estado="Emitido"
    )

    messages.success(request, f"Reserva creada con código {codigo_reserva}. Boleto emitido.")
    return redirect('disponibilidad_asientos', vuelo_id=vuelo.id)