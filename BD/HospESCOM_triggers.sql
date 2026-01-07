----------Trigers

CREATE OR ALTER TRIGGER InsertBitacoraHistorial
ON bitacora_Estatus
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO bitacora_Historial (
        Id_cita,
        Id_paciente,
        Id_doctor,
        Usuario,
        Especialidad,
        Consultorio,
        Fecha_cita,
        Hora_cita,
        Folio_cita,
        Estatus_consulta
    )
    SELECT
        c.Id_cita,
        c.Id_paciente,
        c.Id_doctor,

        CONCAT(u.nombre, ' ', u.apellido_P, ' ', u.apellido_M) AS Usuario,

        e.tipo_Especialidad,
        d.Id_consultorio,

        i.fecha_cita,
        i.hora_cita,

        c.Id_cita AS Folio_cita,

        i.estatus_cita
    FROM inserted i
    INNER JOIN Cita c ON i.Id_cita = c.Id_cita
    INNER JOIN Paciente p ON c.Id_paciente = p.Id_Paciente
    INNER JOIN Usuario u ON p.Id_usuario = u.Id_usuario
    INNER JOIN Doctor d ON c.Id_doctor = d.Id_doctor
    INNER JOIN Especialidad e ON d.Id_especialidad = e.Id_Especialidad;
END;
GO

CREATE OR ALTER TRIGGER Consultafin
ON Receta
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Actualizar el estatus de la cita a 'Completada' cuando se genera una receta
    INSERT INTO bitacora_Estatus (fecha_mov, estatus_cita, fecha_cita, hora_cita, Id_cita)
    SELECT 
        GETDATE(),
        'Completada',
        CAST(c.fecha_limite AS DATE),
        CAST(c.fecha_limite AS TIME),
        i.Id_Cita
    FROM inserted i
    INNER JOIN Cita c ON i.Id_Cita = c.Id_cita;
END;
GO

CREATE OR ALTER TRIGGER UpdateBitacora
ON Cita
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Registrar el cambio en la bitácora
    INSERT INTO bitacora_Estatus (fecha_mov, estatus_cita, fecha_cita, hora_cita, Id_cita)
    SELECT 
        GETDATE(),
        'Modificada',
        CAST(i.fecha_limite AS DATE),
        CAST(i.fecha_limite AS TIME),
        i.Id_cita
    FROM inserted i;
END;
GO

CREATE OR ALTER TRIGGER DeleteBitacora
ON Cita
AFTER DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Registrar la cancelación en la bitácora
    INSERT INTO bitacora_Estatus (fecha_mov, estatus_cita, fecha_cita, hora_cita, Id_cita)
    SELECT 
        GETDATE(),
        'Cancelada',
        CAST(d.fecha_limite AS DATE),
        CAST(d.fecha_limite AS TIME),
        d.Id_cita
    FROM deleted d;
END;
GO