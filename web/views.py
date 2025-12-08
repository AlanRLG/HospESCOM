from urllib import request
from django.shortcuts import render, redirect
from .decorators import login_required_custom
from django.contrib import messages
from datetime import datetime, timedelta
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .models import Especialidad, Doctor, Paciente, Cita, HorarioEmpleado, Usuario, BitacoraEstatus
import re
from django.utils import timezone




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
    usuario_id = request.session.get('usuario_id')

    try:
        paciente = Paciente.objects.get(Id_usuario=usuario_id)
    except Paciente.DoesNotExist:
        messages.error(request, "No se encontró el registro del paciente.")
        return redirect('login')

    citas_proximas = Cita.objects.filter(
        Id_paciente=paciente,
        fecha_limite__gte=datetime.now()
    ).order_by('fecha_limite')

    return render(request, 'web/panel_paciente.html', {
        'nombre_paciente': f"{paciente.Id_usuario.nombre}",
        'citas_proximas': citas_proximas
    })

def datos_personales(request):
    # Validar que haya sesión de usuario
    if "usuario_id" not in request.session:
        return redirect('login')

    usuario_id = request.session["usuario_id"]

    # Obtener datos del usuario
    usuario = Usuario.objects.get(Id_usuario=usuario_id)

    # Obtener datos del paciente relacionado
    paciente = Paciente.objects.get(Id_usuario=usuario)

    contexto = {
        "usuario": usuario,
        "paciente": paciente,
    }

    return render(request, "web/datos_personales.html", contexto)


@login_required_custom
@never_cache
def citas_agendadas(request):
    usuario_id = request.session.get('usuario_id')
    usuario_tipo = request.session.get('usuario_tipo')

    if usuario_tipo != 'paciente':
        messages.error(request, "Solo los pacientes pueden acceder a esta sección.")
        return redirect('login')

    try:
        paciente = Paciente.objects.get(Id_usuario=usuario_id)
    except Paciente.DoesNotExist:
        messages.error(request, "No se encontró el registro del paciente.")
        return redirect('login')

    # Traer todas las citas del paciente
    citas = (
        Cita.objects.filter(Id_paciente=paciente)
        .select_related('Id_doctor__Id_usuario', 'Id_doctor__Id_especialidad')
        .order_by('-fecha_limite')
    )

    # Traer bitácoras asociadas
    bitacoras = {
        b.Id_cita_id: b for b in BitacoraEstatus.objects.filter(Id_cita__in=[c.Id_cita for c in citas])
    }

    return render(request, 'web/citas_agendadas.html', {
        'citas': citas,
        'bitacoras': bitacoras
    })


@login_required_custom
def panel_doctor(request):
    usuario_id = request.session.get('usuario_id')
    nombre_doctor = None

    if usuario_id:
        try:
            usuario = Usuario.objects.get(Id_usuario=usuario_id)
            nombre_doctor = usuario.nombre
        except Usuario.DoesNotExist:
            pass

    return render(request, 'web/panel_doctor.html', {
        'nombre_doctor': nombre_doctor
    })


@login_required_custom
def panel_recepcionista(request):
    usuario_id = request.session.get('usuario_id')
    nombre_recepcionista = None

    if usuario_id:
        try:
            usuario = Usuario.objects.get(Id_usuario=usuario_id)
            nombre_recepcionista = usuario.nombre
        except Usuario.DoesNotExist:
            pass

    return render(request, 'web/panel_recepcionista.html', {
        'nombre_recepcionista': nombre_recepcionista
    })


def logout_view(request):
    request.session.flush()
    return redirect('login')


@login_required_custom
@never_cache
def agendar_cita(request):
    usuario_id = request.session.get('usuario_id')
    usuario_tipo = request.session.get('usuario_tipo')

    if usuario_tipo != 'paciente':
        messages.error(request, "Solo los pacientes pueden agendar citas.")
        return redirect('panel_paciente')

    try:
        paciente = Paciente.objects.get(Id_usuario=usuario_id)
    except Paciente.DoesNotExist:
        messages.error(request, "No se encontró el registro del paciente.")
        return redirect('panel_paciente')

    especialidades = Especialidad.objects.all().order_by('tipo_Especialidad')

    if request.method == 'POST':
        especialidad_id = request.POST.get('especialidad')
        doctor_id = request.POST.get('doctor')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        # Validar fecha y hora
        try:
            fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            messages.error(request, "Formato de fecha u hora inválido.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        ahora = datetime.now()

        if fecha_hora <= ahora:
            messages.error(request, "No se puede agendar una cita en el pasado.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})
        elif fecha_hora < ahora + timedelta(hours=48):
            messages.error(request, "Debes agendar la cita con al menos 48 horas de anticipación.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})
        elif fecha_hora > ahora + timedelta(days=90):
            messages.error(request, "No puedes agendar una cita con más de 3 meses de anticipación.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        try:
            doctor = Doctor.objects.get(Id_doctor=doctor_id, Id_especialidad=especialidad_id)
        except Doctor.DoesNotExist:
            messages.error(request, "El doctor seleccionado no pertenece a esa especialidad.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if not doctor.disponibilidad:
            messages.error(request, "El doctor no está disponible actualmente.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        horarios = HorarioEmpleado.objects.filter(id_Empleado=doctor.Id_usuario)
        if not horarios.exists():
            messages.error(request, "El doctor no tiene un horario laboral registrado.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        dias_map = {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
        }
        dia_semana = dias_map[fecha_hora.strftime("%A").lower()]
        hora_cita = fecha_hora.time()

        # Buscar si el doctor trabaja ese día
        horario_dia = horarios.filter(Id_Dia__nombre_dia__iexact=dia_semana).first()

        if not horario_dia:
            messages.error(request, f"El doctor no trabaja los días {dia_semana}.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if not (horario_dia.hora_entrada <= hora_cita <= horario_dia.hora_salida):
            messages.error(
                request,
                f"El doctor solo atiende de {horario_dia.hora_entrada.strftime('%H:%M')} "
                f"a {horario_dia.hora_salida.strftime('%H:%M')} el día {dia_semana}."
            )
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if Cita.objects.filter(Id_doctor=doctor, fecha_limite=fecha_hora).exists():
            messages.error(request, "El doctor ya tiene una cita en esa fecha y hora.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        rango_inicio = fecha_hora - timedelta(hours=1)
        rango_fin = fecha_hora + timedelta(hours=1)
        conflicto = Cita.objects.filter(
            Id_doctor=doctor,
            fecha_limite__gte=rango_inicio,
            fecha_limite__lte=rango_fin
        ).first()

        if conflicto:
            messages.error(
                request,
                f"El doctor tiene otra cita a las {conflicto.fecha_limite.strftime('%H:%M')}. Debes agendar con al menos 1 hora de diferencia."
            )
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if Cita.objects.filter(Id_paciente=paciente, Id_doctor=doctor).exists():
            messages.error(request, "Ya tienes una cita pendiente con este doctor.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        Cita.objects.create(
            fecha_limite=fecha_hora,
            Id_paciente=paciente,
            Id_doctor=doctor
        )
        messages.success(request, "Cita agendada correctamente.")
        return redirect('agendar_cita')

    return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})


@login_required_custom
def obtener_doctores(request, especialidad_id):
    doctores = Doctor.objects.filter(Id_especialidad=especialidad_id, disponibilidad=True).select_related(
        'Id_usuario__Id_usuario__Id_tipoUsuario'
    ).filter(Id_usuario__Id_usuario__Id_tipoUsuario__NombreUsuario__iexact='Doctor')

    data = [
        {
            "id": d.Id_doctor,
            "nombre": f"{d.Id_usuario.Id_usuario.nombre} {d.Id_usuario.Id_usuario.apellido_P}"
        }
        for d in doctores
    ]
    return JsonResponse(data, safe=False)

REGEX_CURP = r'^[A-Z][AEIOUX][A-Z]{2}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])[HM](AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d$'


def registro_paciente(request):
    edades = range(1, 121)  
    
    if request.method == 'POST':

        # Datos usuario
        nombre = request.POST.get('nombre')
        apellido_P = request.POST.get('apellido_P')
        apellido_M = request.POST.get('apellido_M')
        calle = request.POST.get('calle')
        colonia = request.POST.get('colonia')
        cp = request.POST.get('cp')
        curp = request.POST.get('curp').upper()
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        contraseña2 = request.POST.get('contraseña2')
        tel = request.POST.get('tel')

        # Datos paciente
        edad = request.POST.get('edad')
        peso = request.POST.get('peso')
        estatura = request.POST.get('estatura')
        sexo = request.POST.get('sexo').upper()
        tipo_sangre = request.POST.get('tipo_sangre')
        contacto_emer = request.POST.get('contacto_emer')

        # Validar CURP
        if not re.match(REGEX_CURP, curp):
            messages.error(request, "La CURP no tiene un formato válido.")
            return redirect('registro_paciente')

        # Validar contraseñas
        if contraseña != contraseña2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('registro_paciente')

        # Validar correo no repetido
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "El correo ya está registrado.")
            return redirect('registro_paciente')

        # Crear usuario
        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido_P=apellido_P,
            apellido_M=apellido_M,
            curp=curp,
            correo=correo,
            contraseña=contraseña,
            num_Tel=tel,
            calle=calle,
            colonia=colonia,
            CP=cp,
            Id_tipoUsuario_id=3
        )

        # Crear paciente
        Paciente.objects.create(
            edad=edad,
            peso=peso or None,
            estatura=estatura or None,
            sexo=sexo,
            Tipo_sangre=tipo_sangre,
            contacto_Emer=contacto_emer,
            fecha_Regis=timezone.now(),  
            Id_usuario=usuario
        )

        messages.success(request, "Registro exitoso. Ya puedes iniciar sesión.")
        return redirect('login')

    return render(request, "web/registro_paciente.html", {"edades": edades})

def validar_correo(request):
    correo = request.GET.get('correo', None)
    existe = Usuario.objects.filter(correo=correo).exists()
    return JsonResponse({'existe': existe})
