from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login  # Importar la función login como auth_login
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('usuario:Perfil')  # Redirige a la página de perfil o donde prefieras
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos')
    return render(request, 'usuario/login.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        telefono = request.POST['telefono']
        contrasena = request.POST['contrasena']
        contrasena_correcta = request.POST['contrasena_correcta']

        if contrasena == contrasena_correcta:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado')
            else:
                user = User.objects.create_user(
                    username=email,  # Usar el email como nombre de usuario
                    email=email,
                    password=contrasena,
                    first_name=nombre,
                    last_name=apellido
                )
                user.save()
                messages.success(request, 'Tu cuenta ha sido creada exitosamente')
                # Autenticar y iniciar sesión al usuario recién registrado
                new_user = authenticate(username=email, password=contrasena)
                if new_user is not None:
                    auth_login(request, new_user)  # Usar auth_login en lugar de login
                return redirect('usuario:Perfil')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
    
    return render(request, 'usuario/registro.html')

def verificacion(request):
    return render(request, "usuario/verificacion.html")

def password(request):
    return render(request, "usuario/password.html")

def perfil(request):
    return render(request, "usuario/perfil.html")

def tokenPassword(request):
    return HttpResponse("TokenPassword")

@login_required
def updatePerfil(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        telefono = request.POST['telefono']
        
        # Actualizar la información del usuario
        user = request.user
        user.first_name = nombre
        user.last_name = apellido
        user.email = email
        user.telefono = telefono  # Asegúrate de que el campo teléfono esté en el modelo User
        user.save()

        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('usuario:Perfil')

    return render(request, 'usuario/updateperfil.html')
