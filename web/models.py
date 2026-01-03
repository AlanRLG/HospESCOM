from django.db import models

# ==============================================
# TABLAS PRINCIPALES
# ==============================================

class TipoUsuario(models.Model):
    Id_tipoUsuario = models.AutoField(primary_key=True)
    NombreUsuario = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'TipoUsuario'


class Usuario(models.Model):
    Id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_P = models.CharField(max_length=100)
    apellido_M = models.CharField(max_length=100, null=True, blank=True)
    curp = models.CharField(max_length=18, unique=True)
    correo = models.CharField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=255)
    calle = models.CharField(max_length=150, null=True, blank=True)
    colonia = models.CharField(max_length=100, null=True, blank=True)
    CP = models.CharField(max_length=10, null=True, blank=True)
    num_Tel = models.CharField(max_length=20, null=True, blank=True)
    Id_tipoUsuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, db_column='Id_tipoUsuario')

    class Meta:
        managed = False
        db_table = 'Usuario'


class Empleado(models.Model):
    id_Empleado = models.AutoField(primary_key=True)
    puesto = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Id_usuario')

    class Meta:
        managed = False
        db_table = 'Empleado'


class Recepcionista(models.Model):
    id_Recepcionista = models.AutoField(primary_key=True)
    Id_usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='Id_usuario')

    class Meta:
        managed = False
        db_table = 'Recepcionista'


class Especialidad(models.Model):
    Id_Especialidad = models.AutoField(primary_key=True)
    tipo_Especialidad = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    costo_especialidad = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Especialidad'


class Consultorio(models.Model):
    Id_consultorio = models.AutoField(primary_key=True)
    disponibilidad = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Consultorio'


class Doctor(models.Model):
    Id_doctor = models.AutoField(primary_key=True)
    cedula_Pro = models.CharField(max_length=50, unique=True)
    disponibilidad = models.BooleanField(default=True)
    Id_usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='Id_usuario')
    Id_especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, db_column='Id_especialidad')
    Id_consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, db_column='Id_consultorio')

    class Meta:
        managed = False
        db_table = 'Doctor'


class Paciente(models.Model):
    Id_Paciente = models.AutoField(primary_key=True)
    edad = models.IntegerField()
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    estatura = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    Tipo_sangre = models.CharField(max_length=10, null=True, blank=True)
    contacto_Emer = models.CharField(max_length=100, null=True, blank=True)
    fecha_Regis = models.DateTimeField()
    Id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Id_usuario')

    class Meta:
        managed = False
        db_table = 'Paciente'


class Cita(models.Model):
    Id_cita = models.AutoField(primary_key=True)
    fecha_limite = models.DateTimeField(null=True, blank=True)
    Id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='Id_paciente')
    Id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column='Id_doctor')
    linea_pago = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Cita'


class BitacoraEstatus(models.Model):
    Id_bitacoraEstatus = models.AutoField(primary_key=True)
    fecha_mov = models.DateTimeField()
    estatus_cita = models.CharField(max_length=50, null=True, blank=True)
    fecha_cita = models.DateField()
    hora_cita = models.TimeField()
    monto_Dev = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Politica_cancela = models.CharField(max_length=500, null=True, blank=True)
    Id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE, db_column='Id_cita')

    class Meta:
        managed = False
        db_table = 'bitacora_Estatus'


# ==============================================
# TABLAS DE PAGO, RECETAS Y FARMACIA
# ==============================================

class PagoCita(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateTimeField()
    estado_pago = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pagoC = models.CharField(max_length=50)
    des_pago = models.CharField(max_length=500, null=True, blank=True)
    Id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='Id_usuario')
    Id_cita = models.ForeignKey(Cita, on_delete=models.CASCADE, db_column='Id_cita')

    class Meta:
        managed = False
        db_table = 'pago_Cita'


class Receta(models.Model):
    Id_Receta = models.AutoField(primary_key=True)
    fecha_receta = models.DateField()
    cantidad_receta = models.IntegerField(null=True, blank=True)
    diagnostico = models.CharField(max_length=500, null=True, blank=True)
    tratamiento = models.CharField(max_length=500, null=True, blank=True)
    observaciones = models.CharField(max_length=500, null=True, blank=True)
    duracion = models.CharField(max_length=100, null=True, blank=True)
    frecuencia = models.CharField(max_length=100, null=True, blank=True)
    Id_Cita = models.ForeignKey(Cita, on_delete=models.CASCADE, db_column='Id_Cita')

    class Meta:
        managed = False
        db_table = 'Receta'

class RecetaMedicamento(models.Model):
    Id_Receta_Medicamento = models.AutoField(primary_key=True, db_column="Id_Receta_Medicamento")
    Id_Receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="detalle_medicamentos", db_column="Id_Receta") 
    medicamento = models.CharField(max_length=200)
    frecuencia = models.CharField(max_length=100)
    duracion = models.CharField(max_length=100)
    indicaciones = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Receta_Medicamento'


class FarmaciaMedicamentos(models.Model):
    Id_medicamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    precio_med = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateField(null=True, blank=True)
    lote = models.CharField(max_length=50, null=True, blank=True)
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Farmacia_Medicamentos'


# ==============================================
# TABLAS DE SERVICIOS Y PAGOS
# ==============================================

class Servicio(models.Model):
    Id_Servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Servicio'



# ==============================================
# CLIENTES Y RELACIONES M:M
# ==============================================

class Cliente(models.Model):
    Id_Cliente = models.AutoField(primary_key=True)
    nombreC = models.CharField(max_length=200)
    numeroC = models.CharField(max_length=20, null=True, blank=True)
    correoC = models.CharField(max_length=150, null=True, blank=True)
    genero = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Cliente'


# ==============================================
# ALERGIAS Y PADECIMIENTOS
# ==============================================

class Alergia(models.Model):
    Id_Alergia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        managed = False
        db_table = 'Alergia'


class PacienteAlergia(models.Model):
    Id_Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='Id_Paciente')
    Id_Alergia = models.ForeignKey(Alergia, on_delete=models.CASCADE, db_column='Id_Alergia')

    class Meta:
        managed = False
        db_table = 'Paciente_Alergia'
        unique_together = (('Id_Paciente', 'Id_Alergia'),)


class Padecimiento(models.Model):
    Id_Padecimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150, unique=True)

    class Meta:
        managed = False
        db_table = 'Padecimiento'


class PacientePadecimiento(models.Model):
    Id_Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='Id_Paciente')
    Id_Padecimiento = models.ForeignKey(Padecimiento, on_delete=models.CASCADE, db_column='Id_Padecimiento')

    class Meta:
        managed = False
        db_table = 'Paciente_Padecimiento'
        unique_together = (('Id_Paciente', 'Id_Padecimiento'),)


# ==============================================
# EQUIPO MÉDICO Y CONSULTORIOS
# ==============================================

class EquipoMedico(models.Model):
    Id_Equipo = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Equipo_Medico'


class ConsultorioEquipo(models.Model):
    Id_consultorio = models.ForeignKey(Consultorio, on_delete=models.CASCADE, db_column='Id_consultorio')
    Id_Equipo = models.ForeignKey(EquipoMedico, on_delete=models.CASCADE, db_column='Id_Equipo')
    cantidad_asignada = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'Consultorio_Equipo'
        unique_together = (('Id_consultorio', 'Id_Equipo'),)


# ==============================================
# DÍAS DE SEMANA Y HORARIOS
# ==============================================

class DiaSemana(models.Model):
    Id_Dia = models.IntegerField(primary_key=True)
    nombre_dia = models.CharField(max_length=20, unique=True)

    class Meta:
        managed = False
        db_table = 'Dia_Semana'


class HorarioEmpleado(models.Model):
    Id_HorarioEmpleado = models.AutoField(primary_key=True)
    id_Empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='id_Empleado')
    Id_Dia = models.ForeignKey(DiaSemana, on_delete=models.CASCADE, db_column='Id_Dia')
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()

    class Meta:
        managed = False
        db_table = 'HorarioEmpleado'


class HorarioServicio(models.Model):
    Id_HorarioServicio = models.AutoField(primary_key=True)
    id_Servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, db_column='id_Servicio')
    Id_Dia = models.ForeignKey(DiaSemana, on_delete=models.CASCADE, db_column='Id_Dia')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        managed = False
        db_table = 'Horario_Servicio'

class VistaDetalleReceta(models.Model):
    Id_Receta = models.IntegerField(primary_key=True)
    fecha_receta = models.DateField()
    diagnostico = models.CharField(max_length=500)
    medicamentos = models.CharField(max_length=500)
    tratamiento = models.CharField(max_length=500)
    observaciones = models.CharField(max_length=500)
    duracion = models.CharField(max_length=100)
    Nombre_Paciente = models.CharField(max_length=200)
    Nombre_Doctor = models.CharField(max_length=200)
    tipo_Especialidad = models.CharField(max_length=100)
    cedula_Pro = models.CharField(max_length=50)

    class Meta:
        managed = False  
        db_table = 'Vista_Detalle_Receta'


class Ticket(models.Model):
    Id_Ticket = models.AutoField(primary_key=True)
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    Id_Recepcionista = models.ForeignKey('Recepcionista', on_delete=models.CASCADE, db_column='Id_Recepcionista')
    Id_Paciente = models.ForeignKey('Paciente', on_delete=models.SET_NULL, null=True, blank=True, db_column='Id_Paciente')
    Id_Cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True, db_column='Id_Cliente')

    class Meta:
        managed = False
        db_table = 'Ticket'

class TicketMedicamento(models.Model):
    Id_TicketMed = models.AutoField(primary_key=True)
    Id_Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='Id_Ticket')
    Id_Medicamento = models.ForeignKey( 'FarmaciaMedicamentos', on_delete=models.CASCADE, db_column='Id_Medicamento')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Ticket_Medicamento'

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

class TicketServicio(models.Model):
    Id_TicketServicio = models.AutoField(primary_key=True)
    Id_Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='Id_Ticket')
    Id_Servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE, db_column='Id_Servicio')
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'Ticket_Servicio'

class PagoTicket(models.Model):
    Id_PagoTicket = models.AutoField(primary_key=True)
    Id_Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='Id_Ticket')
    fecha_pago = models.DateTimeField()
    metodo_pago = models.CharField(max_length=50)
    estado_pago = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'Pago_Ticket'

