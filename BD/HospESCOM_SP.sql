USE HospESCOM;
GO

--Valida si hay cita hoy y devuelve datos
CREATE PROCEDURE sp_ObtenerDatosParaReceta
    @IdPaciente INT
AS
BEGIN
     SET NOCOUNT ON;

    SELECT TOP 1
        C.Id_cita,
        CONCAT(UP.nombre, ' ', UP.apellido_P, ' ', ISNULL(UP.apellido_M, '')) AS Nombre_Paciente,
        CONCAT(UD.nombre, ' ', UD.apellido_P, ' ', ISNULL(UD.apellido_M, '')) AS Nombre_Medico,
        E.tipo_Especialidad,
        C.fecha_limite,

        ISNULL((
            SELECT TOP 1 estatus_cita
            FROM bitacora_Estatus
            WHERE Id_cita = C.Id_cita
            ORDER BY fecha_mov DESC
        ), 'Agendada') AS Estatus_Actual

    FROM Cita C
    INNER JOIN Paciente P ON C.Id_paciente = P.Id_Paciente
    INNER JOIN Usuario UP ON P.Id_usuario = UP.Id_usuario
    INNER JOIN Doctor D ON C.Id_doctor = D.Id_doctor
    INNER JOIN Empleado Emp ON D.Id_usuario = Emp.Id_Empleado
    INNER JOIN Usuario UD ON Emp.Id_usuario = UD.Id_usuario
    INNER JOIN Especialidad E ON D.Id_especialidad = E.Id_Especialidad

    WHERE 
        C.Id_paciente = @IdPaciente
        AND CAST(C.fecha_limite AS DATE) = CAST(GETDATE() AS DATE)

    ORDER BY C.fecha_limite DESC;
END;
GO

--SP para buscar recetas por nombre médico o cédula
CREATE PROCEDURE sp_BuscarHistorialMedico
    @Busqueda NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT * FROM Vista_Detalle_Receta
    WHERE 
        Nombre_Doctor LIKE '%' + @Busqueda + '%' 
        OR 
        cedula_Pro LIKE '%' + @Busqueda + '%'
    ORDER BY fecha_receta DESC;
END;
GO

EXEC sp_BuscarHistorialMedico 'Pablo';