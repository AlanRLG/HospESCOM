from django.shortcuts import get_object_or_404, render, redirect
from .decorators import login_required_custom
from django.contrib import messages
from datetime import date, datetime, timedelta
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from .models import Consultorio, Especialidad, Doctor, Paciente, Cita, RecetaMedicamento, Servicio, Ticket, PagoTicket, TicketServicio
from .models import HorarioEmpleado, TipoUsuario, Usuario, BitacoraEstatus, Empleado, Receta, TicketMedicamento
from .models import VistaDetalleReceta, Alergia, Padecimiento, Recepcionista, DiaSemana, FarmaciaMedicamentos, Cliente
import re
from django.utils import timezone
from django.http import HttpResponse
from web.pdf_cita import generar_comprobante_cita
from django.db.models import OuterRef, Subquery, CharField, F
from django.db import DatabaseError, connection 
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.utils.timezone import now


def index(request):
    
    context = {'year': datetime.now().year}
    return render(request, 'web/index.html', context)

@never_cache
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.select_related('Id_tipoUsuario').get(correo=correo)

            # VALIDAR CONTRASEÑA HASHEADA
            if not check_password(password, usuario.contraseña):
                raise Usuario.DoesNotExist

            tipo = usuario.Id_tipoUsuario.NombreUsuario.lower()

            # Guardar sesión
            request.session['usuario_id'] = usuario.Id_usuario
            request.session['usuario_tipo'] = tipo

            # Redirección
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

    # Obtener SOLO las citas del paciente con estatus permitido
    citas = Cita.objects.filter(Id_paciente=paciente)

    # Filtrar bitácoras que solo sean los estatus válidos
    bitacoras_validas = BitacoraEstatus.objects.filter(
        Id_cita__in=citas,
        estatus_cita__in=[
            "Agendada pendiente de pago",
            "Pagada pendiente por atender"
        ]
    )

    # Crear diccionario (cita_id -> bitácora)
    bitacoras = {
        b.Id_cita_id: b
        for b in bitacoras_validas
    }

    ahora = datetime.now()

    # Filtrar solo citas futuras
    citas_proximas = []
    for c in citas:
        b = bitacoras.get(c.Id_cita)
        if b:
            fecha_completa = datetime.combine(b.fecha_cita, b.hora_cita)
            if fecha_completa >= ahora:
                citas_proximas.append(c)

    # Ordenarlas por fecha completa real
    citas_proximas.sort(
        key=lambda c: datetime.combine(
            bitacoras[c.Id_cita].fecha_cita,
            bitacoras[c.Id_cita].hora_cita
        )
    )

    return render(request, 'web/panel_paciente.html', {
        'nombre_paciente': paciente.Id_usuario.nombre,
        'citas_proximas': citas_proximas,
        'bitacoras': bitacoras
    })


@login_required_custom
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

    citas = (
        Cita.objects.filter(Id_paciente=paciente)
        .select_related('Id_doctor__Id_usuario', 'Id_doctor__Id_especialidad')
        .order_by('-fecha_limite')
    )

    # 🔎 FILTROS
    fecha = request.GET.get('fecha')
    estatus = request.GET.get('estatus')

    if fecha:
        citas = citas.filter(
            bitacoraestatus__fecha_cita=fecha
        )

    if estatus:
        citas = citas.filter(
            bitacoraestatus__estatus_cita=estatus
        )

    # Bitácoras
    bitacoras = {
        b.Id_cita_id: b
        for b in BitacoraEstatus.objects.filter(Id_cita__in=[c.Id_cita for c in citas])
    }

    return render(request, 'web/citas_agendadas.html', {
        'citas': citas,
        'bitacoras': bitacoras
    })


@login_required_custom
def panel_doctor(request):
    usuario_id = request.session.get('usuario_id')

    try:
        # 1. Obtener usuario
        usuario = Usuario.objects.get(Id_usuario=usuario_id)

        # 2. Obtener empleado
        empleado = Empleado.objects.get(Id_usuario=usuario)

        # 3. Obtener doctor
        doctor = Doctor.objects.get(Id_usuario=empleado)

        nombre_doctor = usuario.nombre
        doctor_id = doctor.Id_doctor

    except (Usuario.DoesNotExist, Empleado.DoesNotExist, Doctor.DoesNotExist):
        nombre_doctor = None
        doctor_id = None

    return render(request, 'web/panel_doctor.html', {
        'nombre_doctor': nombre_doctor,
        'doctor_id': doctor_id
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

    # --- Descarga de PDF ---
    if request.GET.get('descargar_pdf') == 'true' and 'pdf_descarga' in request.session:
        import base64
        pdf_base64 = request.session.pop('pdf_descarga')
        pdf_nombre = request.session.pop('pdf_nombre', 'comprobante.pdf')
        
        pdf_bytes = base64.b64decode(pdf_base64)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_nombre}"'
        return response

    # --- Procesamiento POST ---
    if request.method == 'POST':
        especialidad_id = request.POST.get('especialidad')
        doctor_id = request.POST.get('doctor')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        try:
            fecha_hora_cita = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        except ValueError:
            messages.error(request, "Formato de fecha u hora inválido.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        ahora = datetime.now()

        # --- Validaciones de fecha ---
        if fecha_hora_cita <= ahora:
            messages.error(request, "No se puede agendar una cita en el pasado.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if fecha_hora_cita < ahora + timedelta(hours=48):
            messages.error(request, "Debes agendar con 48 horas de anticipación.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if fecha_hora_cita > ahora + timedelta(days=90):
            messages.error(request, "No puedes agendar con más de 3 meses de anticipación.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        # --- Validación doctor ---
        try:
            doctor = Doctor.objects.get(Id_doctor=doctor_id, Id_especialidad=especialidad_id)
        except Doctor.DoesNotExist:
            messages.error(request, "El doctor no pertenece a esa especialidad.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if not doctor.disponibilidad:
            messages.error(request, "El doctor no está disponible actualmente.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        horarios = HorarioEmpleado.objects.filter(id_Empleado=doctor.Id_usuario)
        if not horarios.exists():
            messages.error(request, "El doctor no tiene horario registrado.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        # --- Validación horario ---
        dias_map = {
            "monday": "Lunes",
            "tuesday": "Martes",
            "wednesday": "Miércoles",
            "thursday": "Jueves",
            "friday": "Viernes",
            "saturday": "Sábado",
            "sunday": "Domingo",
        }

        dia_semana = dias_map[fecha_hora_cita.strftime("%A").lower()]
        hora_cita = fecha_hora_cita.time()

        horario_dia = horarios.filter(Id_Dia__nombre_dia__iexact=dia_semana).first()
        if not horario_dia:
            messages.error(request, f"El doctor no trabaja los días {dia_semana}.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        if not (horario_dia.hora_entrada <= hora_cita <= horario_dia.hora_salida):
            messages.error(request, f"El doctor atiende de {horario_dia.hora_entrada} a {horario_dia.hora_salida}.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        # =========================================================
        # VALIDACIÓN 1: Paciente ya tiene una cita pendiente con ese doctor
        # =========================================================
        if BitacoraEstatus.objects.filter(
            Id_cita__Id_paciente=paciente,
            Id_cita__Id_doctor=doctor,
            estatus_cita__in=[
                "Agendada pendiente de pago",
                "Pagada pendiente por atender"
            ]
        ).exists():
            messages.error(request, "Ya tienes una cita pendiente con este doctor.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})

        # =========================================================
        # VALIDACIÓN 2: El doctor ya tiene una cita en esa fecha/hora
        # =========================================================
        if BitacoraEstatus.objects.filter(
            fecha_cita=fecha_hora_cita.date(),
            hora_cita=fecha_hora_cita.time(),
            Id_cita__Id_doctor=doctor,
            estatus_cita__in=[
                "Agendada pendiente de pago",
                "Pagada pendiente por atender"
            ]
        ).exists():
            messages.error(request, "El doctor ya tiene una cita agendada en esa fecha y hora.")
            return render(request, 'web/agendar_cita.html', {'especialidades': especialidades})


        # --- Crear cita ---
        fecha_limite_pago = ahora + timedelta(hours=8)
        

        nueva_cita = Cita.objects.create(
            fecha_limite=fecha_limite_pago,
            Id_paciente=paciente,
            Id_doctor=doctor,
        )

        linea_pago = f"PAY-{nueva_cita.Id_cita}-{int(nueva_cita.fecha_limite.timestamp())}"

        # Guardarla en BD
        nueva_cita.linea_pago = linea_pago
        nueva_cita.save()

        # --- Crear bitácora ---
        bitacora = BitacoraEstatus.objects.create(
            estatus_cita="Agendada pendiente de pago",
            fecha_cita=fecha_hora_cita.date(),
            hora_cita=hora_cita,
            monto_Dev=None,
            Politica_cancela=None,
            Id_cita=nueva_cita
        )

        # --- Generar PDF ---
        pdf_stream = generar_comprobante_cita(nueva_cita, bitacora, nueva_cita.linea_pago)


        import base64
        pdf_base64 = base64.b64encode(pdf_stream.getvalue()).decode('utf-8')
        request.session['pdf_descarga'] = pdf_base64
        request.session['pdf_nombre'] = f"comprobante_cita_{nueva_cita.Id_cita}.pdf"

        messages.success(request, "Cita agendada correctamente. Descargando comprobante...")

        return render(request, 'web/agendar_cita.html', {
            'especialidades': especialidades,
            'descargar_y_redirigir': True
        })

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
            contraseña=make_password(contraseña),
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

@never_cache
@login_required_custom
def pagar_cita(request, id_cita):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "title": "Error",
            "message": "Método no permitido."
        })

    try:
        cita = Cita.objects.get(Id_cita=id_cita)
    except Cita.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "title": "Error",
            "message": "La cita no existe."
        })

    try:
        bitacora = BitacoraEstatus.objects.get(Id_cita=cita)
    except BitacoraEstatus.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "title": "Error",
            "message": "No existe estatus para esta cita."
        })

    if bitacora.estatus_cita != "Agendada pendiente de pago":
        return JsonResponse({
            "status": "error",
            "title": "Error",
            "message": "Esta cita no se puede pagar."
        })

    import json
    data = json.loads(request.body)
    linea_usuario = data.get("linea_pago", "").strip()

    # ✔ Ahora si valida contra la BD
    linea_real = cita.linea_pago.strip()

    if linea_usuario != linea_real:
        return JsonResponse({
            "status": "error",
            "title": "Línea inválida",
            "message": "La línea de pago es incorrecta."
        })

    # Cambiar estatus
    bitacora.estatus_cita = "Pagada pendiente por atender"
    bitacora.fecha_mov = datetime.now()
    bitacora.save()

    return JsonResponse({
        "status": "success",
        "title": "Pago exitoso",
        "message": "La cita ha sido pagada correctamente."
    })


@login_required_custom
@never_cache
def cancelar_cita(request, id_cita):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido."})

    usuario_id = request.session.get('usuario_id')

    # 1. Obtener cita
    try:
        cita = Cita.objects.select_related(
            'Id_doctor__Id_especialidad'
        ).get(
            Id_cita=id_cita,
            Id_paciente__Id_usuario=usuario_id
        )
    except Cita.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No se encontró la cita."})

    # 2. Obtener bitácora
    try:
        bitacora = BitacoraEstatus.objects.get(Id_cita=cita)
    except BitacoraEstatus.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No se encontró el estatus actual."})

    estatus_actual = bitacora.estatus_cita

    # 3. Validar cancelación
    if estatus_actual not in [
        "Agendada pendiente de pago",
        "Pagada pendiente por atender"
    ]:
        return JsonResponse({
            "status": "error",
            "message": "Esta cita no se puede cancelar."
        })

    ahora = datetime.now()
    fecha_cita = datetime.combine(bitacora.fecha_cita, bitacora.hora_cita)
    horas_faltantes = (fecha_cita - ahora).total_seconds() / 3600

    monto_devolucion = 0
    politica_texto = ""

    # --------------------------------------------------
    # COSTO REAL DE LA ESPECIALIDAD
    # --------------------------------------------------
    costo = cita.Id_doctor.Id_especialidad.costo_especialidad or 0

    if estatus_actual == "Agendada pendiente de pago":
        nuevo_estatus = "Cancelada Falta de pago"
        politica_texto = "No aplica devolución."
        monto_devolucion = 0

    elif estatus_actual == "Pagada pendiente por atender":
        nuevo_estatus = "Cancelada por paciente"

        if horas_faltantes >= 48:
            monto_devolucion = costo
            politica_texto = (
                f"Devolución del 100% (${costo}) por cancelar con más de 48 horas."
            )

        elif horas_faltantes >= 24:
            monto_devolucion = round(costo * 0.5, 2)
            politica_texto = (
                f"Devolución del 50% (${monto_devolucion}) por cancelar entre 24 y 48 horas."
            )

        else:
            monto_devolucion = 0
            politica_texto = "Sin devolución (cancelación con menos de 24 horas)."

    # --------------------------------------------------
    # ACTUALIZAR BITÁCORA
    # --------------------------------------------------
    bitacora.estatus_cita = nuevo_estatus
    bitacora.Politica_cancela = politica_texto
    bitacora.monto_Dev = monto_devolucion
    bitacora.fecha_mov = ahora
    bitacora.save()

    return JsonResponse({
        "status": "ok",
        "message": (
            f"La cita ha sido cancelada. "
            f"{politica_texto}"
        )
    })

@login_required_custom
@never_cache
def citas_medico(request):

    usuario_id = request.session.get('usuario_id')
    usuario_tipo = request.session.get('usuario_tipo')

    # SOLO los doctores pueden entrar
    if usuario_tipo != "doctor":
        return redirect('login')

    # 1. Obtener el usuario
    try:
        usuario = Usuario.objects.get(Id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        return redirect('login')

    # 2. Obtener el empleado correspondiente
    try:
        empleado = Empleado.objects.get(Id_usuario=usuario)
    except Empleado.DoesNotExist:
        return redirect('panel_doctor')

    # 3. Obtener el doctor correspondiente al empleado
    try:
        doctor = Doctor.objects.get(Id_usuario=empleado)
    except Doctor.DoesNotExist:
        return redirect('panel_doctor')

    nombre_real = f"{usuario.nombre} {usuario.apellido_P} {usuario.apellido_M}"

    # -------- SUBQUERIES --------
    ultimo_estatus = Subquery(
        BitacoraEstatus.objects.filter(Id_cita=OuterRef('Id_cita'))
        .order_by('-fecha_mov')
        .values('estatus_cita')[:1],
        output_field=CharField()
    )

    ultimo_fecha = Subquery(
        BitacoraEstatus.objects.filter(Id_cita=OuterRef('Id_cita'))
        .order_by('-fecha_mov')
        .values('fecha_cita')[:1]
    )

    ultimo_hora = Subquery(
        BitacoraEstatus.objects.filter(Id_cita=OuterRef('Id_cita'))
        .order_by('-fecha_mov')
        .values('hora_cita')[:1]
    )

    # -------- CONSULTA FINAL --------
    citas_qs = (
        Cita.objects.filter(Id_doctor=doctor)
        .annotate(
            ultimo_estatus=ultimo_estatus,
            ultimo_fecha=ultimo_fecha,
            ultimo_hora=ultimo_hora,
            nombre_paciente=F("Id_paciente__Id_usuario__nombre"),
            apellido_paciente=F("Id_paciente__Id_usuario__apellido_P"),
            id_bitacora=F("bitacoraestatus__Id_bitacoraEstatus"),

        )
        .filter(
            ultimo_estatus__in=[
                "Pagada pendiente por atender",
                "Atendida"
            ]
        )
        .order_by('ultimo_fecha', 'ultimo_hora')
    )

    return render(request, "web/citas_medico.html", {
        "medico": doctor,
        "citas": citas_qs,
        "nombre_real": nombre_real
    })

@login_required_custom
@never_cache
def solicitar_cancelacion_medico(request, id_cita):
    if request.method != "POST":
        return redirect("citas_medico")

    if request.session.get("usuario_tipo") != "doctor":
        return redirect("login")

    try:
        cita = Cita.objects.get(Id_cita=id_cita)
    except Cita.DoesNotExist:
        messages.error(request, "Cita no encontrada.")
        return redirect("citas_medico")

    # 🔹 Obtener el ÚLTIMO estatus de la cita
    bitacora = BitacoraEstatus.objects.filter(
        Id_cita=cita
    ).order_by('-fecha_mov').first()

    if not bitacora:
        messages.error(request, "No se encontró historial de la cita.")
        return redirect("citas_medico")

    # 🔹 Actualizar el estatus (NO crear uno nuevo)
    bitacora.estatus_cita = "Solicitud de cancelación por médico"
    bitacora.Politica_cancela = (
        "Solicitud enviada por el médico. Requiere autorización de recepción."
    )
    bitacora.save()

    messages.success(request, "Solicitud de cancelación enviada a recepción.")
    return redirect("citas_medico")




@login_required_custom
def historial_recetas(request):
    busqueda = request.GET.get('q', '')
    recetas = []

    if busqueda:
        # Usa el SP de búsqueda para filtrar por Doctor o Cédula
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_BuscarHistorialMedico %s", [busqueda])
            columns = [col[0] for col in cursor.description]
            recetas = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'web/historial_recetas.html', {
        'recetas': recetas, 
        'busqueda': busqueda
    })


@login_required_custom
def datos_paciente_medico(request, id_paciente):

    if request.session.get("usuario_tipo") != "doctor":
        return redirect("login")

    paciente = get_object_or_404(Paciente, Id_Paciente=id_paciente)
    usuario = paciente.Id_usuario

    alergias = Alergia.objects.filter(pacientealergia__Id_Paciente=paciente)
    padecimientos = Padecimiento.objects.filter(pacientepadecimiento__Id_Paciente=paciente)

    # ---------- HISTORIAL ----------
    citas = (
        Cita.objects
        .filter(Id_paciente=paciente)
        .annotate(
            id_bitacora=F("bitacoraestatus__Id_bitacoraEstatus"),
            fecha_cita=F("bitacoraestatus__fecha_cita"),
            nombre_medico=F("Id_doctor__Id_usuario__Id_usuario__nombre"),
            apellido_medico=F("Id_doctor__Id_usuario__Id_usuario__apellido_P"),
            especialidad=F("Id_doctor__Id_especialidad__tipo_Especialidad"),
            consultorio=F("Id_doctor__Id_consultorio__Id_consultorio"),
            diagnostico=F("receta__diagnostico"),
        )
        .order_by("-fecha_cita")
    )

    return render(request, "web/datos_paciente_medico.html", {
        "paciente": paciente,
        "usuario": usuario,
        "alergias": alergias,
        "padecimientos": padecimientos,
        "citas": citas
    })

@login_required_custom
def generar_receta(request, id_paciente):

    if request.session.get('usuario_tipo') != 'doctor':
        return redirect('index')

    datos_cita = None
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_ObtenerDatosParaReceta %s", [id_paciente])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            datos_cita = dict(zip(columns, row))

    if not datos_cita:
        messages.error(request, "El paciente no tiene cita hoy.")
        return redirect('historial_recetas')

    if request.method == 'POST':
        try:
            # 1️⃣ Guardar receta
            receta = Receta.objects.create(
                fecha_receta=timezone.now().date(),
                diagnostico=request.POST.get('diagnostico'),
                observaciones=request.POST.get('observaciones'),
                Id_Cita_id=datos_cita['Id_cita']
            )

            # 2️⃣ Obtener listas de medicamentos
            medicamentos = request.POST.getlist('medicamento[]')
            frecuencias = request.POST.getlist('frecuencia[]')
            duraciones = request.POST.getlist('duracion[]')
            indicaciones = request.POST.getlist('indicaciones[]')

            # 3️⃣ Guardar cada medicamento
            for i in range(len(medicamentos)):
                if medicamentos[i].strip():  # evita registros vacíos
                    RecetaMedicamento.objects.create(
                        Id_Receta=receta,
                        medicamento=medicamentos[i],
                        frecuencia=frecuencias[i],
                        duracion=duraciones[i],
                        indicaciones=indicaciones[i]
                    )

            messages.success(request, "Receta generada correctamente.")
            return redirect('ver_receta_detalle', id_receta=receta.Id_Receta)

        except Exception as e:
                messages.error(request, f"Error al guardar receta: {e}")


    return render(request, 'web/generar_receta.html', {
        'nombre_paciente': datos_cita['Nombre_Paciente'],
        'nombre_medico': datos_cita['Nombre_Medico'],
        'fecha': timezone.now().date(),
        'cita_id': datos_cita['Id_cita']
    })

@login_required_custom
def ver_receta_detalle(request, id_receta):
    receta = Receta.objects.get(Id_Receta=id_receta)
    medicamentos = receta.detalle_medicamentos.all()

    return render(request, 'web/ver_receta.html', {
        'receta': receta,
        'medicamentos': medicamentos
    })

@login_required_custom
def atender_cita(request, id_cita):

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

    if request.session.get("usuario_tipo") != "doctor":
        return JsonResponse({"status": "error", "message": "No autorizado"}, status=403)

    cita = get_object_or_404(Cita, Id_cita=id_cita)

    bitacora = (
        BitacoraEstatus.objects
        .filter(Id_cita=cita)
        .order_by("-fecha_mov")
        .first()
    )

    if bitacora.estatus_cita != "Pagada pendiente por atender":
        return JsonResponse({
            "status": "error",
            "message": "La cita no puede ser atendida."
        })

    #  VALIDAR FECHA Y HORA
    fecha_hora_cita = datetime.combine(bitacora.fecha_cita, bitacora.hora_cita)
    ahora = timezone.localtime()

    if ahora < timezone.make_aware(fecha_hora_cita):
        return JsonResponse({
            "status": "error",
            "message": "No puedes atender la cita antes de la fecha y hora programadas."
        })

    
    bitacora.estatus_cita = "Atendida"
    bitacora.fecha_mov = ahora
    bitacora.save()

    return JsonResponse({
        "status": "ok",
        "message": "La cita ha sido marcada como atendida correctamente."
    })

@login_required_custom
def datos_doctor(request):

    if request.session.get("usuario_tipo") != "doctor":
        return redirect("login")

    usuario_id = request.session.get("usuario_id")

    # Usuario
    usuario = get_object_or_404(Usuario, Id_usuario=usuario_id)

    # Empleado
    empleado = get_object_or_404(Empleado, Id_usuario=usuario)

    # Doctor
    doctor = get_object_or_404(Doctor, Id_usuario=empleado)

    return render(request, "web/datos_doctor.html", {
        "usuario": usuario,
        "empleado": empleado,
        "doctor": doctor
    })

@login_required_custom
def gestionar_doctores(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    doctores = (
        Doctor.objects
        .select_related("Id_usuario__Id_usuario", "Id_especialidad")
        .all()
    )

    return render(request, "web/gestionar_doctores.html", {
        "doctores": doctores
    })

@login_required_custom
def cambiar_estado_doctor(request, id_doctor):

    if request.method != "POST":
        return redirect("gestionar_doctores")

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    doctor = get_object_or_404(Doctor, Id_doctor=id_doctor)

    # Verificar citas activas
    citas_activas = BitacoraEstatus.objects.filter(
        Id_cita__Id_doctor=doctor,
        estatus_cita__in=[
            "Agendada pendiente de pago",
            "Pagada pendiente por atender"
        ]
    ).exists()

    if citas_activas and doctor.disponibilidad:
        messages.error(
            request,
            "No se puede dar de baja al doctor porque tiene citas asignadas."
        )
        return redirect("gestionar_doctores")

    # Cambiar estado
    doctor.disponibilidad = not doctor.disponibilidad
    doctor.save()

    estado = "activado" if doctor.disponibilidad else "desactivado"
    messages.success(request, f"Doctor {estado} correctamente.")

    return redirect("gestionar_doctores")

@login_required_custom
def alta_doctor(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        with transaction.atomic():

            usuario = Usuario.objects.create(
                nombre=request.POST["nombre"],
                apellido_P=request.POST["apellido_p"],
                apellido_M=request.POST.get("apellido_m"),
                curp=request.POST["curp"],
                correo=request.POST["correo"],
                contraseña=make_password(request.POST["password"]),
                calle=request.POST.get("calle"),
                colonia=request.POST.get("colonia"),
                CP=request.POST.get("cp"),
                num_Tel=request.POST.get("telefono"),
                Id_tipoUsuario=TipoUsuario.objects.get(NombreUsuario="doctor")
            )

            empleado = Empleado.objects.create(
                puesto="Doctor",
                salario=0,
                Id_usuario=usuario
            )

            doctor = Doctor.objects.create(
                cedula_Pro=request.POST["cedula"],
                disponibilidad=True,
                Id_usuario=empleado,
                Id_especialidad_id=request.POST["especialidad"],
                Id_consultorio_id=request.POST["consultorio"]
            )

            # ---------- HORARIOS ----------
            dias_seleccionados = request.POST.getlist("dias")

            if not dias_seleccionados:
                messages.error(request, "Debes asignar al menos un día de trabajo.")
                raise Exception("Sin horario")

            for dia_id in dias_seleccionados:
                entrada = request.POST.get(f"entrada_{dia_id}")
                salida = request.POST.get(f"salida_{dia_id}")

                if not entrada or not salida:
                    messages.error(request, "Debes indicar horas completas.")
                    raise Exception("Horario incompleto")

                HorarioEmpleado.objects.create(
                    id_Empleado=empleado,
                    Id_Dia_id=dia_id,
                    hora_entrada=entrada,
                    hora_salida=salida
                )

        messages.success(request, "Doctor y horario registrados correctamente.")
        return redirect("gestionar_doctores")

    return render(request, "web/alta_doctor.html", {
        "especialidades": Especialidad.objects.all(),
        "consultorios": Consultorio.objects.all(),
        "dias": DiaSemana.objects.all()
    })


@login_required_custom
def gestionar_recepcionistas(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    recepcionistas = (
        Recepcionista.objects
        .select_related("Id_usuario__Id_usuario")
        .all()
    )

    return render(request, "web/gestionar_recepcionistas.html", {
        "recepcionistas": recepcionistas
    })

@login_required_custom
def alta_recepcionista(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        # Tipo usuario recepcionista
        tipo = TipoUsuario.objects.get(NombreUsuario="recepcionista")

        usuario = Usuario.objects.create(
            nombre=request.POST["nombre"],
            apellido_P=request.POST["apellido_p"],
            apellido_M=request.POST.get("apellido_m"),
            curp=request.POST["curp"],
            correo=request.POST["correo"],
            contraseña=make_password(request.POST["password"]),
            calle=request.POST.get("calle"),
            colonia=request.POST.get("colonia"),
            CP=request.POST.get("cp"),
            num_Tel=request.POST.get("telefono"),
            Id_tipoUsuario=tipo
        )

        empleado = Empleado.objects.create(
            puesto="Recepcionista",
            salario=1000,
            Id_usuario=usuario
        )

        Recepcionista.objects.create(
            Id_usuario=empleado
        )

        messages.success(request, "Recepcionista dado de alta correctamente.")
        return redirect("gestionar_recepcionistas")

    return render(request, "web/alta_recepcionista.html")


from django.db.models import OuterRef, Subquery, Max

from django.db.models import OuterRef, Subquery, Max

@login_required_custom
def bitacora_citas_recepcionista(request):

    # Subconsulta: última fecha_mov por cita
    ultima_bitacora = (
        BitacoraEstatus.objects
        .filter(Id_cita=OuterRef('Id_cita'))
        .values('Id_cita')
        .annotate(max_fecha=Max('fecha_mov'))
        .values('max_fecha')
    )

    bitacoras = (
        BitacoraEstatus.objects
        .filter(fecha_mov=Subquery(ultima_bitacora))
        .select_related(
            'Id_cita',
            'Id_cita__Id_doctor',
            'Id_cita__Id_doctor__Id_usuario',
            'Id_cita__Id_doctor__Id_usuario__Id_usuario',
            'Id_cita__Id_paciente',
            'Id_cita__Id_paciente__Id_usuario',
            'Id_cita__Id_doctor__Id_especialidad'
        )
        .order_by('-fecha_mov')
    )

    return render(request, 'web/bitacora_citas_recepcionista.html', {
        'bitacoras': bitacoras
    })

@login_required_custom
def cancelar_cita_paciente(request, id_cita):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        })

    if request.session.get("usuario_tipo") != "recepcionista":
        return JsonResponse({
            "status": "error",
            "message": "No autorizado"
        })

    # 1. Obtener cita
    try:
        cita = Cita.objects.select_related(
            'Id_doctor__Id_especialidad'
        ).get(Id_cita=id_cita)
    except Cita.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Cita no encontrada"
        })

    # 2. Obtener bitácora actual
    try:
        bitacora = BitacoraEstatus.objects.filter(
            Id_cita=cita
        ).order_by("-fecha_mov").first()
    except BitacoraEstatus.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "No se encontró el estatus de la cita"
        })

    estatus_actual = bitacora.estatus_cita

    # 3. Validar estatus permitido
    if estatus_actual not in [
        "Agendada pendiente de pago",
        "Pagada pendiente por atender"
    ]:
        return JsonResponse({
            "status": "error",
            "message": "La cita no puede cancelarse en este estado"
        })

    # --------------------------------------------------
    # CÁLCULO DE DEVOLUCIÓN (MISMA LÓGICA QUE PACIENTE)
    # --------------------------------------------------
    ahora = datetime.now()
    fecha_cita = datetime.combine(bitacora.fecha_cita, bitacora.hora_cita)
    horas_faltantes = (fecha_cita - ahora).total_seconds() / 3600

    costo = cita.Id_doctor.Id_especialidad.costo_especialidad or 0
    monto_devolucion = 0
    politica_texto = ""

    if estatus_actual == "Agendada pendiente de pago":
        nuevo_estatus = "Cancelada Falta de pago"
        politica_texto = "No aplica devolución."
        monto_devolucion = 0

    elif estatus_actual == "Pagada pendiente por atender":
        nuevo_estatus = "Cancelada por paciente"

        if horas_faltantes >= 48:
            monto_devolucion = costo
            politica_texto = (
                f"Devolución del 100% (${costo}) por cancelar con más de 48 horas."
            )
        elif horas_faltantes >= 24:
            monto_devolucion = round(costo * 0.5, 2)
            politica_texto = (
                f"Devolución del 50% (${monto_devolucion}) por cancelar entre 24 y 48 horas."
            )
        else:
            monto_devolucion = 0
            politica_texto = (
                "Sin devolución (cancelación con menos de 24 horas)."
            )

    # 4. Actualizar bitácora
    bitacora.estatus_cita = nuevo_estatus
    bitacora.monto_Dev = monto_devolucion
    bitacora.Politica_cancela = politica_texto
    bitacora.fecha_mov = timezone.now()
    bitacora.save()

    return JsonResponse({
        "status": "ok",
        "message": "Cita cancelada correctamente por el paciente"
    })

@login_required_custom
@never_cache
def autorizar_cancelacion_medico(request, id_cita):

    if request.method != "POST":
        return JsonResponse({
            "status": "error",
            "message": "Método no permitido"
        })

    if request.session.get("usuario_tipo") != "recepcionista":
        return JsonResponse({
            "status": "error",
            "message": "No autorizado"
        })

    # 1. Obtener cita
    try:
        cita = Cita.objects.select_related(
            "Id_doctor__Id_especialidad"
        ).get(Id_cita=id_cita)
    except Cita.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Cita no encontrada"
        })

    # 2. Obtener bitácora actual
    try:
        bitacora = BitacoraEstatus.objects.get(
            Id_cita=cita,
            estatus_cita="Solicitud de cancelación por médico"
        )
    except BitacoraEstatus.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "La cita no tiene una solicitud de cancelación válida"
        })

    # 3. Calcular devolución (100%)
    costo = cita.Id_doctor.Id_especialidad.costo_especialidad or 0

    politica_texto = (
        f"Cancelación autorizada por recepción. "
        f"Devolución del 100% (${costo}) por cancelación del médico."
    )

    # 4. Actualizar bitácora (NO crear registro nuevo)
    bitacora.estatus_cita = "Cancelada por médico"
    bitacora.monto_Dev = costo
    bitacora.Politica_cancela = politica_texto
    bitacora.fecha_mov = timezone.now()
    bitacora.save()

    return JsonResponse({
        "status": "ok",
        "message": "Cancelación por médico autorizada. Devolución del 100% aplicada."
    })

@login_required_custom
def farmacia(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    medicamentos = FarmaciaMedicamentos.objects.all().order_by("nombre")


    return render(request, "web/farmacia.html", {
        "medicamentos": medicamentos
    })

@login_required_custom
def alta_medicamento(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        FarmaciaMedicamentos.objects.create(
            nombre=request.POST["nombre"],
            precio_med=request.POST["precio"],
            fecha_caducidad=request.POST.get("caducidad") or None,
            lote=request.POST.get("lote"),
            cantidad=request.POST["cantidad"]
        )

        messages.success(request, "Medicamento agregado correctamente.")
        return redirect("farmacia")

    return render(request, "web/alta_medicamento.html")

@login_required_custom
def editar_medicamento(request, id_medicamento):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    try:
        medicamento = FarmaciaMedicamentos.objects.get(
            Id_medicamento=id_medicamento
        )
    except FarmaciaMedicamentos.DoesNotExist:
        messages.error(request, "Medicamento no encontrado.")
        return redirect("farmacia")

    if request.method == "POST":
        medicamento.nombre = request.POST.get("nombre")
        medicamento.precio_med = request.POST.get("precio")
        medicamento.fecha_caducidad = request.POST.get("fecha_caducidad") or None
        medicamento.lote = request.POST.get("lote")
        medicamento.cantidad = request.POST.get("cantidad")

        medicamento.save()

        messages.success(request, "Medicamento actualizado correctamente.")
        return redirect("farmacia")

    return render(request, "web/editar_medicamento.html", {
        "medicamento": medicamento
    })

@login_required_custom
def servicios_recepcionista(request):
    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    servicios = Servicio.objects.all()

    return render(request, "web/servicios_recepcionista.html", {
        "servicios": servicios
    })

@login_required_custom
def alta_servicio(request):
    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        Servicio.objects.create(
            nombre_servicio=request.POST["nombre"],
            costo=request.POST["costo"],
            descripcion=request.POST.get("descripcion")
        )

        messages.success(request, "Servicio registrado correctamente.")
        return redirect("servicios_recepcionista")

    return render(request, "web/alta_servicio.html")

@login_required_custom
def editar_servicio(request, id_servicio):
    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    servicio = get_object_or_404(Servicio, Id_Servicio=id_servicio)

    if request.method == "POST":
        servicio.nombre_servicio = request.POST["nombre"]
        servicio.costo = request.POST["costo"]
        servicio.descripcion = request.POST.get("descripcion")
        servicio.save()

        messages.success(request, "Servicio actualizado correctamente.")
        return redirect("servicios_recepcionista")

    return render(request, "web/editar_servicio.html", {
        "servicio": servicio
    })

@login_required_custom
def cobro_inicio(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        id_paciente = request.POST.get("paciente")
        id_cliente = request.POST.get("cliente")

        if id_paciente and id_cliente:
            messages.error(request, "Seleccione solo paciente o cliente externo.")
            return redirect("cobro")

        if not id_paciente and not id_cliente:
            messages.error(request, "Debe seleccionar un paciente o un cliente externo.")
            return redirect("cobro")

        empleado = Empleado.objects.get(
            Id_usuario_id=request.session["usuario_id"]
        )

        recepcionista = Recepcionista.objects.get(
            Id_usuario=empleado
        )

        #  CREAR TICKET CON SP
        with connection.cursor() as cursor:
            cursor.execute("""
                DECLARE @IdTicket INT;
                EXEC sp_crear_ticket %s, %s, %s, @IdTicket OUTPUT;
                SELECT @IdTicket;
            """, [
                recepcionista.id_Recepcionista,
                id_paciente if id_paciente else None,
                id_cliente if id_cliente else None
            ])

            id_ticket = cursor.fetchone()[0]

        return redirect("cobro_ticket", id_ticket)

    return render(request, "web/cobro_inicio.html", {
        "pacientes": Paciente.objects.select_related("Id_usuario"),
        "clientes": Cliente.objects.all()
    })

@login_required_custom
def cobro_ticket(request, id_ticket):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    ticket = Ticket.objects.filter(Id_Ticket=id_ticket).first()
    if not ticket:
        return redirect("cobro")

    medicamentos = FarmaciaMedicamentos.objects.all()
    servicios = Servicio.objects.all()

    meds_ticket = TicketMedicamento.objects.filter(Id_Ticket=ticket)
    servs_ticket = TicketServicio.objects.filter(Id_Ticket=ticket)

    #  CALCULAR TOTAL CON SP
    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_calcular_total_ticket %s", [id_ticket])
        total = cursor.fetchone()[0]

    ticket.total = total

    return render(request, "web/cobro_ticket.html", {
        "ticket": ticket,
        "medicamentos": medicamentos,
        "servicios": servicios,
        "meds_ticket": meds_ticket,
        "servs_ticket": servs_ticket,
        "total": total
    })

@login_required_custom
def agregar_medicamento_ticket(request):

    if request.method != "POST":
        return JsonResponse({"status": "error"})

    ticket_id = request.POST["ticket_id"]
    medicamento_id = request.POST["medicamento"]
    cantidad = int(request.POST["cantidad"])

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC sp_agregar_medicamento_ticket %s, %s, %s",
                [ticket_id, medicamento_id, cantidad]
            )
    except DatabaseError as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

    return JsonResponse({"status": "ok"})

@login_required_custom
def agregar_servicio_ticket(request):

    if request.method != "POST":
        return JsonResponse({"status": "error"})

    ticket_id = request.POST["ticket_id"]
    servicio_id = request.POST["servicio"]

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_agregar_servicio_ticket %s, %s",
            [ticket_id, servicio_id]
        )

    return JsonResponse({"status": "ok"})

@login_required_custom
def resumen_ticket(request, id_ticket):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    ticket = Ticket.objects.filter(Id_Ticket=id_ticket).first()
    if not ticket:
        return redirect("cobro")

    meds_ticket = TicketMedicamento.objects.filter(Id_Ticket_id=id_ticket)
    servs_ticket = TicketServicio.objects.filter(Id_Ticket_id=id_ticket)

    with connection.cursor() as cursor:
        cursor.execute("EXEC sp_calcular_total_ticket %s", [id_ticket])
        total = cursor.fetchone()[0]

    return render(request, "web/resumen_ticket.html", {
        "ticket": ticket,
        "meds_ticket": meds_ticket,
        "servs_ticket": servs_ticket,
        "total": total
    })


@login_required_custom
def pagar_ticket(request, id_ticket):

    if request.method != "POST":
        return JsonResponse({"status": "error"})

    metodo = request.POST["metodo"]
    descripcion = request.POST.get("descripcion", "")

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC sp_pagar_ticket %s, %s, %s",
            [id_ticket, metodo, descripcion]
        )

    return JsonResponse({
        "status": "ok",
        "message": "Pago registrado correctamente"
    })


@login_required_custom
def alta_cliente(request):

    if request.session.get("usuario_tipo") != "recepcionista":
        return redirect("login")

    if request.method == "POST":
        cliente = Cliente.objects.create(
            nombreC=request.POST["nombre"],
            numeroC=request.POST.get("telefono"),
            correoC=request.POST.get("correo"),
            genero=request.POST.get("genero")
        )

        empleado = Empleado.objects.get(
            Id_usuario_id=request.session["usuario_id"]
        )

        recepcionista = Recepcionista.objects.get(
            Id_usuario=empleado
        )

        # 🔹 Crear ticket con SP
        with connection.cursor() as cursor:
            cursor.execute("""
                DECLARE @IdTicket INT;
                EXEC sp_crear_ticket %s, NULL, %s, @IdTicket OUTPUT;
                SELECT @IdTicket;
            """, [
                recepcionista.id_Recepcionista,
                cliente.Id_Cliente
            ])

            id_ticket = cursor.fetchone()[0]

        messages.success(request, "Cliente registrado correctamente.")
        return redirect("cobro_ticket", id_ticket)

    return render(request, "web/alta_cliente.html")
