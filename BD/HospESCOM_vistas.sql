use HospESCOM
GO

--Vista 1
CREATE VIEW Vista_VentasTotales AS
SELECT 
    'Medicamento' AS TipoVenta,
    FM.nombre AS Producto,
    VM.cantidad,
    VM.subtotal,
    U.nombre + ' ' + U.apellido_P AS Recepcionista
FROM Venta_Med VM
JOIN Farmacia_Medicamentos FM ON VM.Id_Medicamento = FM.Id_medicamento
JOIN Recepcionista R ON VM.Id_recepcionista = R.id_Recepcionista
JOIN Empleado E ON R.Id_usuario = E.id_Empleado
JOIN Usuario U ON E.Id_usuario = U.Id_usuario
UNION ALL
SELECT 
    'Servicio',
    S.nombre_servicio,
    1 AS cantidad,
    VS.subtotal,
    U2.nombre + ' ' + U2.apellido_P
FROM Venta_servicio VS
JOIN Servicio S ON VS.id_Servicio = S.Id_Servicio
JOIN Recepcionista R2 ON VS.Id_recepcionista = R2.id_Recepcionista
JOIN Empleado E2 ON R2.Id_usuario = E2.id_Empleado
JOIN Usuario U2 ON E2.Id_usuario = U2.Id_usuario;
GO

--Vista 2
CREATE VIEW Vista_PacientesAlergiasPadecimientos AS
SELECT 
    U.nombre + ' ' + U.apellido_P AS Paciente,
    ISNULL(A.nombre, 'Sin alergias registradas') AS Alergia,
    ISNULL(PD.nombre, 'Sin padecimientos registrados') AS Padecimiento
FROM Paciente PA
JOIN Usuario U ON PA.Id_usuario = U.Id_usuario
LEFT JOIN Paciente_Alergia PALE ON PA.Id_Paciente = PALE.Id_Paciente
LEFT JOIN Alergia A ON PALE.Id_Alergia = A.Id_Alergia
LEFT JOIN Paciente_Padecimiento PPAD ON PA.Id_Paciente = PPAD.Id_Paciente
LEFT JOIN Padecimiento PD ON PPAD.Id_Padecimiento = PD.Id_Padecimiento;
GO

--Vista 3
CREATE VIEW Vista_Doctor_Atencion AS
SELECT 
    D.Id_doctor,
    -- Datos del doctor
    U.nombre + ' ' + U.apellido_P + ' ' + ISNULL(U.apellido_M, '') AS NombreDoctor,
    U.curp,
    U.correo,
    U.num_Tel,
    EM.puesto,
    CASE WHEN D.disponibilidad = 1 THEN 'Disponible' ELSE 'No disponible' END AS DisponibilidadDoctor,
    -- Especialidad
    E.tipo_Especialidad AS Especialidad,
    E.descripcion AS DescripcionEspecialidad,
    E.costo_especialidad,
    -- Consultorio
    C.Id_consultorio,
    CASE WHEN C.disponibilidad = 1 THEN 'Disponible' ELSE 'Ocupado' END AS DisponibilidadConsultorio,
    -- Datos del paciente atendido
    U2.nombre + ' ' + U2.apellido_P + ' ' + ISNULL(U2.apellido_M, '') AS Paciente,
    P.edad,
    P.estatura,
    P.peso,
    P.Tipo_sangre,
    -- Datos de la cita
    CT.Id_cita,
    CT.fecha_limite AS Fecha_Cita,
    BE.estatus_cita AS Estatus_Cita,
    BE.hora_cita AS Hora_Cita

FROM Doctor D
JOIN Empleado EM ON D.Id_usuario = EM.id_Empleado
JOIN Usuario U ON EM.Id_usuario = U.Id_usuario
JOIN Especialidad E ON D.Id_especialidad = E.Id_Especialidad
JOIN Consultorio C ON D.Id_consultorio = C.Id_consultorio

LEFT JOIN Cita CT ON CT.Id_doctor = D.Id_doctor
LEFT JOIN Paciente P ON CT.Id_paciente = P.Id_Paciente
LEFT JOIN Usuario U2 ON P.Id_usuario = U2.Id_usuario
LEFT JOIN bitacora_Estatus BE ON BE.Id_cita = CT.Id_cita;
GO

--Vista 4
CREATE VIEW Vista_CitasDetalladas1 AS
SELECT 
    C.Id_cita,
    U1.nombre + ' ' + U1.apellido_P + U1.apellido_M AS Paciente,
    U2.nombre + ' ' + U2.apellido_P AS Doctor,
    E.tipo_Especialidad AS Especialidad,
    C.fecha_limite AS FechaCita
FROM Cita C
JOIN Paciente P ON C.Id_paciente = P.Id_Paciente
JOIN Usuario U1 ON P.Id_usuario = U1.Id_usuario
JOIN Doctor D ON C.Id_doctor = D.Id_doctor
JOIN Empleado EM ON D.Id_usuario = EM.id_Empleado
JOIN Usuario U2 ON EM.Id_usuario = U2.Id_usuario
JOIN Especialidad E ON D.Id_especialidad = E.Id_Especialidad;
GO

--Para encontrar citas rápido por fecha
CREATE NONCLUSTERED INDEX IX_Cita_Fecha_Paciente 
ON Cita (fecha_limite) INCLUDE (Id_paciente, Id_doctor);
GO

--Para leer la receta completa
CREATE VIEW Vista_Detalle_Receta AS
SELECT 
    R.Id_Receta,
    R.fecha_receta,
    CONCAT(UP.nombre, ' ', UP.apellido_P, ' ', ISNULL(UP.apellido_M, '')) AS Nombre_Paciente,
    CONCAT(UD.nombre, ' ', UD.apellido_P, ' ', ISNULL(UD.apellido_M, '')) AS Nombre_Doctor,
    D.cedula_Pro,
    E.tipo_Especialidad,
    R.diagnostico,
    -- MAPEO DE COLUMNAS (Para que coincida con tu formulario)
    R.tratamiento AS medicamentos,
    R.frecuencia AS tratamiento,     
    R.observaciones,                  
    R.duracion
FROM Receta R
    INNER JOIN Cita C ON R.Id_Cita = C.Id_cita
    INNER JOIN Paciente P ON C.Id_paciente = P.Id_Paciente
    INNER JOIN Usuario UP ON P.Id_usuario = UP.Id_usuario
    INNER JOIN Doctor D ON C.Id_doctor = D.Id_doctor
    INNER JOIN Empleado Emp ON D.Id_usuario = Emp.id_Empleado
    INNER JOIN Usuario UD ON Emp.Id_usuario = UD.Id_usuario
    INNER JOIN Especialidad E ON D.Id_especialidad = E.Id_Especialidad;
GO

SELECT * FROM Vista_CitasDetalladas1;
SELECT * FROM Vista_Doctor_Atencion;
SELECT * FROM Vista_PacientesAlergiasPadecimientos;
SELECT * FROM Vista_VentasTotales;
