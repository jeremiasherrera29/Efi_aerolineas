from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
import uuid
from django.contrib.auth import login
from django.http import JsonResponse
from .models import Vuelo, Pasajero, Reserva, Boleto, Usuario, Avion, Asiento
from .forms import VueloForm, PasajeroForm, ReservaForm, BoletoForm, UsuarioForm, AvionForm, AsientoForm
from aerolineas.services.vuelo_service import VueloService

# ---------------------- VUELOS ----------------------
class VueloList(ListView):
    model = Vuelo
    template_name = "vuelos/list.html"
    context_object_name = "vuelos"

    def get_queryset(self):
        return VueloService.listar_vuelos(self.request.GET)
class VueloDetail(DetailView):
    model = Vuelo
    template_name = "vuelos/detail.html"
    context_object_name = "vuelo"
    pk_url_kwarg = "vuelo_id"

class VueloDelete(DeleteView):
    model = Vuelo
    template_name = "vuelos/delete.html"
    success_url = reverse_lazy("vuelos_list")
    pk_url_kwarg = "vuelo_id"

class VueloCreate(CreateView):
    model = Vuelo
    form_class = VueloForm
    template_name = "vuelos/create.html"
    success_url = reverse_lazy("vuelos_list")

# ---------------------- PASAJEROS ----------------------
class PasajeroList(ListView):
    model = Pasajero
    template_name = "pasajeros/list.html"
    context_object_name = "pasajeros"

class PasajeroDetail(DetailView):
    model = Pasajero
    template_name = "pasajeros/detail.html"
    context_object_name = "pasajero"
    pk_url_kwarg = "pasajero_id"

class PasajeroCreate(CreateView):
    model = Pasajero
    form_class = PasajeroForm
    template_name = "pasajeros/create.html"
    success_url = reverse_lazy("pasajeros_list")

class PasajeroDelete(DeleteView):
    model = Pasajero
    template_name = "pasajeros/delete.html"
    success_url = reverse_lazy("pasajeros_list")
    pk_url_kwarg = "pasajero_id"

class HistorialVuelosPasajero(View):
    def get(self, request, pasajero_id):
        pasajero = get_object_or_404(Pasajero, pk=pasajero_id)
        reservas = Reserva.objects.filter(pasajero=pasajero)
        return render(request, "pasajeros/historial.html", {"pasajero": pasajero, "reservas": reservas})

# RESERVAS
class ReservaList(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/list.html"
    context_object_name = "reservas"

    def get_queryset(self):
        user = self.request.user
        if user.rol in ["ADM", "EMP"]:
            return Reserva.objects.all()
        elif user.rol == "PAS":
            return Reserva.objects.filter(pasajero__usuario=user)
        return Reserva.objects.none()


class ReservaCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/create.html"
    success_url = reverse_lazy("reservas_list")

    def test_func(self):
        return self.request.user.rol in ["ADM", "EMP", "PAS"]

    def form_valid(self, form):
        user = self.request.user

        # PASAJERO: asignar pasajero y guardar antes de crear boleto
        if user.rol == "PAS":
            pasajero = Pasajero.objects.filter(usuario=user).first()
            if not pasajero:
                form.add_error(None, "No se encontró el pasajero vinculado a este usuario.")
                return self.form_invalid(form)
            
            # Guardar reserva con pasajero
            self.object = form.save(commit=False)
            self.object.pasajero = pasajero
            self.object.save()
            form.save_m2m()

            from .models import Boleto
            try:
                boleto = Boleto.objects.create(
                    reserva=self.object,
                    codigo_barra=str(uuid.uuid4())[:8],
                    fecha_emision=timezone.now(),
                    estado="emitido"
                )
                print("BOLETO CREADO:", boleto)
            except Exception as e:
                print("ERROR CREANDO BOLETO:", e)

            return redirect(self.get_success_url())

        return super().form_valid(form)

class ReservaDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reserva
    pk_url_kwarg = "reserva_id"
    template_name = "reservas/delete.html"
    success_url = reverse_lazy("reservas_list")

    def test_func(self):
        user = self.request.user
        reserva = self.get_object()
        if user.rol in ["ADM", "EMP"]:
            return True
        if user.rol == "PAS":
            pasajero = Pasajero.objects.filter(usuario=user).first()
            return pasajero == reserva.pasajero
        return False


class ReservaDetail(LoginRequiredMixin, DetailView):
    model = Reserva
    pk_url_kwarg = "reserva_id"
    template_name = "reservas/detail.html"
    context_object_name = "reserva"

    def get_queryset(self):
        user = self.request.user
        if user.rol in ["ADM", "EMP"]:
            return Reserva.objects.all()
        elif user.rol == "PAS":
            return Reserva.objects.filter(pasajero__usuario=user)
        return Reserva.objects.none()



# BOLETOS

class BoletoList(LoginRequiredMixin, ListView):
    model = Boleto
    template_name = 'boletos/list.html'
    context_object_name = 'boletos'

    def get_queryset(self):
        user = self.request.user
        if user.rol in ["ADM", "EMP"]:
            return Boleto.objects.all()
        elif user.rol == "PAS":
            return Boleto.objects.filter(reserva__pasajero__email=user.email)
        return Boleto.objects.none()


class BoletoCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Boleto
    form_class = BoletoForm
    template_name = 'boletos/create.html'
    success_url = reverse_lazy('boletos_list')

    def test_func(self):
        return self.request.user.rol in ["ADM", "EMP"]


class BoletoDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Boleto
    pk_url_kwarg = "boleto_id"
    template_name = 'boletos/delete.html'
    success_url = reverse_lazy('boletos_list')

    def test_func(self):
        user = self.request.user
        boleto = self.get_object()
        if user.rol in ["ADM", "EMP"]:
            return True
        return user.rol == "PAS" and boleto.reserva.pasajero.email == user.email


class BoletoDetail(LoginRequiredMixin, DetailView):
    model = Boleto
    template_name = 'boletos/detail.html'
    context_object_name = 'boleto'

    def get_queryset(self):
        user = self.request.user
        if user.rol in ["ADM", "EMP"]:
            return Boleto.objects.all()
        elif user.rol == "PAS":
            return Boleto.objects.filter(reserva__pasajero__email=user.email)
        return Boleto.objects.none()

class BuscarBoletoView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("codigo")
        boletos = None
        if query:
            boletos = Boleto.objects.filter(codigo_barra__icontains=query)
        return render(request, "boletos/buscar.html", {"boletos": boletos, "query": query}) 

# ---------------------- USUARIOS ----------------------
class UsuarioList(ListView):
    model = Usuario
    template_name = "usuarios/list.html"
    context_object_name = "usuarios"

class UsuarioCreate(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "usuarios/create.html"
    success_url = reverse_lazy("usuarios_list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.rol = form.cleaned_data["rol"]     
        user.save()
        return super().form_valid(form)
    
class RegisterView(View):
    def get(self, request):
        return render(request, "usuarios/register.html")

    def post(self, request):
        username = request.POST["username"]
        email = request.POST["email"]
        rol = request.POST["rol"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        usuario = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        usuario.rol = rol
        usuario.save()

        if rol == "PAS":
            Pasajero.objects.create(
                usuario=usuario,
                nombre=username,
                email=email
            )

        login(request, usuario)
        return redirect("vuelos_list")
class UsuarioDelete(DeleteView):
    model = Usuario
    template_name = "usuarios/delete.html"
    success_url = reverse_lazy("usuarios_list")
    pk_url_kwarg = "usuario_id"

class UsuarioUpdate(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = "usuarios/update.html"
    success_url = reverse_lazy("usuarios_list")
    pk_url_kwarg = "usuario_id"

# ---------------------- AVIONES ----------------------
class AvionList(ListView):
    model = Avion
    template_name = "aviones/list.html"
    context_object_name = "aviones"

class AvionDetail(DetailView):
    model = Avion
    template_name = "aviones/detail.html"
    context_object_name = "avion"
    pk_url_kwarg = "avion_id"

class AvionCreate(CreateView):
    model = Avion
    form_class = AvionForm
    template_name = "aviones/create.html"
    success_url = reverse_lazy("aviones_list")

class AvionDelete(DeleteView):
    model = Avion
    template_name = "aviones/delete.html"
    success_url = reverse_lazy("aviones_list")
    pk_url_kwarg = "avion_id"

# ---------------------- ASIENTOS ----------------------
class AsientoList(ListView):
    model = Asiento
    template_name = "aerolineas/asientos/list.html"
    context_object_name = "asientos"

class AsientoDetail(DetailView):
    model = Asiento
    template_name = "aerolineas/asientos/detail.html"
    context_object_name = "asiento"
    pk_url_kwarg = "asiento_id"

class AsientoCreate(CreateView):
    model = Asiento
    form_class = AsientoForm
    template_name = "aerolineas/asientos/create.html"
    success_url = reverse_lazy("asientos_list")

class AsientoDelete(DeleteView):
    model = Asiento
    template_name = "aerolineas/asientos/delete.html"
    success_url = reverse_lazy("asientos_list")
    pk_url_kwarg = "asiento_id"

# ---------------------- FUNCIONES EXTRA ----------------------
def disponibilidad_asientos(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos = Asiento.objects.filter(avion=vuelo.avion)
    asientos_disponibles = asientos.filter(estado="Disponible")
    return render(request, "aerolineas/asientos/disponibilidad.html", {
        "vuelo": vuelo,
        "asientos": asientos_disponibles
})
def reservar_asiento(request, vuelo_id, asiento_id):
    asiento = get_object_or_404(Asiento, id=asiento_id, vuelo_id=vuelo_id)
    asiento.disponible = False
    asiento.save()
    return redirect("disponibilidad_asientos", vuelo_id=vuelo_id)

def reporte_pasajeros_por_vuelo(request, vuelo_id):
    vuelo = get_object_or_404(Vuelo, pk=vuelo_id)
    reservas = Reserva.objects.filter(vuelo=vuelo)
    pasajeros = [r.pasajero for r in reservas]
    return render(request, "aerolineas/reporte_pasajeros_por_vuelo.html", {"vuelo": vuelo, "pasajeros": pasajeros})
