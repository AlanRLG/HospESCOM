from django.shortcuts import render, redirect
from .decorators import login_required_custom
from django.contrib import messages
from .models import Usuario
from datetime import datetime
from django.views.decorators.cache import never_cache

def index(request):
    context = {'year': datetime.now().year}
    return render(request, 'web/index.html', context)

@never_cache
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.select_related('Id_tipoUsuario').get(correo=correo, contraseña=password)
            tipo = usuario.Id_tipoUsuario.NombreUsuario.lower()

            # Guardar usuario en la sesión
            request.session['usuario_id'] = usuario.Id_usuario
            request.session['usuario_tipo'] = tipo

            # Redirigir según tipo
            if tipo == 'doctor':
                return redirect('panel_doctor')
            elif tipo == 'recepcionista':
                return redirect('panel_recepcionista')
            else:
                return redirect('panel_paciente')

        except Usuario.DoesNotExist:
            messages.error(request, 'Correo o contraseña incorrectos.')

    return render(request, 'web/login.html')

@login_required_custom
def panel_paciente(request):
    return render(request, 'web/panel_paciente.html')

@login_required_custom
def panel_doctor(request):
    return render(request, 'web/panel_doctor.html')

@login_required_custom
def panel_recepcionista(request):
    return render(request, 'web/panel_recepcionista.html')

def logout_view(request):
    request.session.flush()  # borra toda la sesión
    return redirect('login')