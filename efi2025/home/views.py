from django.shortcuts import render

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

# Create your views here.

def home_view(request):
    return render(request, 'index.html')

def register_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        pass1 = data.get('password1')
        pass2 = data.get('password2')
        email = data.get('email')
        
        if not username or not pass1 or not pass2 or not email: # Si algunos de estos campos esta vacio 
            messages.error(request, "Faltan datos") # Te tira un error con un mensaje 
            return render(request, 'accounts/register.html') # Vuelve a cargar el formulario de registro

        elif _validate_pass(pass1, pass2):
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'accounts/register.html')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya está en uso")
            return render(request, 'accounts/register.html')

        else:
            User.objects.create_user(  # Si todo esta bien, crea un nuevo usuario
                username=username, 
                password=pass1,
                email=email
            )
            messages.success(request, "Cuenta creada correctamente")
            return redirect('login')

    return render(request, 'accounts/register.html',{'ocultar_nav': True}) # Oculta el nav en el register 

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