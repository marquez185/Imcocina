from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from BD.models import Favoritos
import re

def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search("[A-Z]", contrasena):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search("[a-z]", contrasena):
        return False, "La contraseña debe contener al menos una letra minúscula."
    if not re.search("[0-9]", contrasena):
        return False, "La contraseña debe contener al menos un número."
    if not re.search("[!@#$%^&*(),.?\":{}|<>]", contrasena):
        return False, "La contraseña debe contener al menos un carácter especial."
    return True, ""


def login(request):
    registro_exitoso = False
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Has iniciado sesión correctamente')
            registro_exitoso = True
            return redirect('usuario:Perfil')  # Redirige a la página de perfil o donde prefieras
        else:
            messages.error(request, 'Correo electrónico o contraseña incorrectos')
    return render(request, 'usuario/login.html', {'registro_exitoso': registro_exitoso})

def registro(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        email = request.POST['email']
        contrasena = request.POST['contrasena']
        contrasena_correcta = request.POST['contrasena_correcta']

        if contrasena == contrasena_correcta:
            es_valida, mensaje = validar_contrasena(contrasena)
            if not es_valida:
                messages.error(request, mensaje)
                return redirect('usuario:Registro')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está registrado')
            else:
                user = User.objects.create_user(
                    username=email,
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

# View for password reset verification
def verificacion(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/password-reset/{uid}/{token}/')
            email_subject = 'Restablecimiento de contraseña'
            email_body = render_to_string('usuario/email_template.html', {
                'user': user,
                'reset_link': reset_link,
            })
            email = EmailMessage(
                email_subject,
                email_body,
                'wraithjmz@outlook.com',  # Reemplaza con tu correo electrónico configurado
                [user.email],
            )
            email.content_subtype = "html"  # Esto asegura que el correo se envíe como HTML
            email.send(fail_silently=False)
            messages.success(request, 'Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico.')
            return redirect('usuario:Login')
        except User.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo electrónico.')
            return redirect('usuario:Verificacion')
    return render(request, 'usuario/verificacion.html')

# View for password reset
def password(request, uidb64=None, token=None):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        token = request.POST.get('token')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect(f'/password-reset/{uid}/{token}/')

        # Validar la nueva contraseña
        es_valida, mensaje = validar_contrasena(password)
        if not es_valida:
            messages.error(request, mensaje)
            return redirect(f'/password-reset/{uid}/{token}/')
        
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
                return redirect('usuario:Login')
            else:
                messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha caducado.')
                return redirect('usuario:Verificacion')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'El enlace de restablecimiento de contraseña no es válido o ha caducado.')
            return redirect('usuario:Verificacion')
    else:
        context = {
            'uid': uidb64,
            'token': token
        }
        return render(request, 'usuario/password.html', context)


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
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_nueva_confirmacion = request.POST.get('password_nueva_confirmacion')
        
        user = request.user
        
        # Verificar si el nuevo correo electrónico ya está en uso por otro usuario
        if User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'El correo electrónico ya está en uso por otro usuario.')
            return redirect('usuario:UpdatePerfil')
        
        # Actualizar la información del usuario
        user.first_name = nombre
        user.last_name = apellido
        
        # Si el correo electrónico ha cambiado, actualizar username y email
        if user.email != email:
            user.email = email
            user.username = email
        
        # Actualizar la contraseña si se proporcionaron todos los campos
        if password_actual and password_nueva and password_nueva_confirmacion:
            if not check_password(password_actual, user.password):
                messages.error(request, 'La contraseña actual es incorrecta.')
                return redirect('usuario:UpdatePerfil')
            if password_nueva != password_nueva_confirmacion:
                messages.error(request, 'Las nuevas contraseñas no coinciden.')
                return redirect('usuario:UpdatePerfil')

            # Validar la nueva contraseña
            es_valida, mensaje = validar_contrasena(password_nueva)
            if not es_valida:
                messages.error(request, mensaje)
                return redirect('usuario:UpdatePerfil')
                
            user.set_password(password_nueva)
        
        user.save()

        # Actualizar la sesión del usuario
        update_session_auth_hash(request, user)

        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('usuario:Perfil')

    return render(request, 'usuario/updatePerfil.html')

@login_required
def recetas_favoritas(request):
    favoritas = Favoritos.objects.filter(usuario=request.user)
    context = {'favoritas': favoritas}
    return render(request, "usuario/recetas_favoritas.html", context)
