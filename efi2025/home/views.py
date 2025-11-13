from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from aerolineas.forms import UsuarioForm

from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import redirect, render


def home_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Cuenta creada correctamente")
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, f"Error en el form: {form.errors}")

    else:
        form = UsuarioForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'ocultar_nav': True
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(
            request, 
            username=username, 
            password=password
        )
        if user is not None: 
            login(request, user)
            messages.success(request, "Sesion iniciada")
            return redirect("index")
        else:
            messages.error(request, "El usuario o contraseña no coinciden")
            
    return render(request, "accounts/login.html",{'ocultar_nav': True}) # Oculta el nav en el login 

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect('index')

def _validate_pass(pass1, pass2):
    return pass1 != pass2