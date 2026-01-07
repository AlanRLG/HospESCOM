USE HospESCOM;
GO

-- Primero elimina las funciones si existen
DROP FUNCTION IF EXISTS dbo.DoctorEnJornada;
DROP FUNCTION IF EXISTS dbo.DoctorOcupado;
DROP FUNCTION IF EXISTS dbo.PacienteCita;
DROP FUNCTION IF EXISTS dbo.CalcularReembolso;
DROP FUNCTION IF EXISTS dbo.ValidarLogin;
GO

/*Verifica si una fecha y hora está dentro de la jornada laboral de un doctor.*/
CREATE FUNCTION dbo.DoctorEnJornada (@Id_doctor INT, @FechaHoraCita DATETIME)
RETURNS BIT
AS
BEGIN
    DECLARE @EstaEnJornada BIT = 0;
    DECLARE @HoraCita TIME = CAST(@FechaHoraCita AS TIME);
    DECLARE @DiaSemana INT = DATEPART(WEEKDAY, @FechaHoraCita);
    DECLARE @IdEmpleado INT;
    DECLARE @HoraInicio TIME;
    DECLARE @HoraFin TIME;

	SELECT @IdEmpleado = Id_usuario
    FROM Doctor
    WHERE Id_doctor = @Id_doctor;

	SELECT @HoraInicio = hora_entrada, @HoraFin = hora_salida
    FROM HorarioEmpleado
    WHERE id_Empleado = @IdEmpleado
      AND Id_Dia = @DiaSemana;

    IF (@HoraCita >= @HoraInicio AND @HoraCita < @HoraFin)
        SET @EstaEnJornada = 1;

    RETURN @EstaEnJornada;
END;
GO



/*Verifica si un doctor ya tiene una cita a una hora específica.*/
CREATE FUNCTION dbo.DoctorOcupado (@Id_doctor INT, @FechaCita DATE,@HoraCita TIME)
RETURNS BIT
AS
BEGIN
    DECLARE @EstaOcupado BIT = 0;

    IF EXISTS (
        SELECT 1
        FROM Cita AS C
		INNER JOIN bitacora_Estatus AS B ON C.Id_cita = B.Id_cita
        WHERE C.Id_doctor = @Id_doctor
          AND B.fecha_cita = @FechaCita
          AND B.hora_cita = @HoraCita
          AND B.estatus_cita NOT IN ('Cancelada Paciente', 'Cancelada Doctor', 'Cancelada Falta de pago')
    )
        SET @EstaOcupado = 1;

    RETURN @EstaOcupado;
END;
GO

/*Verifica si un paciente ya tiene una cita pendiente con el mismo doctor.*/
CREATE FUNCTION dbo.PacienteCita (@Id_paciente INT, @Id_doctor INT)
RETURNS BIT
AS
BEGIN
    DECLARE @TienePendiente BIT = 0;

    IF EXISTS (
        SELECT 1
        FROM Cita AS C
        INNER JOIN bitacora_Estatus AS B ON C.Id_cita = B.Id_cita
        WHERE C.Id_paciente = @Id_paciente
          AND C.Id_doctor = @Id_doctor
          AND B.estatus_cita IN ('Agendada pendiente de pago', 'Pagada pendiente por atender')
    )
        SET @TienePendiente = 1;

    RETURN @TienePendiente;
END;
GO


/*Calcula el monto a reembolsar por la política de cancelación.*/
CREATE FUNCTION dbo.CalcularReembolso (@Id_cita INT, @FechaCancelacion DATETIME)
RETURNS DECIMAL(10, 2)
AS
BEGIN
    DECLARE @MontoReembolso DECIMAL(10, 2) = 0.00;
    DECLARE @MontoTotalCita DECIMAL(10, 2);
    DECLARE @FechaCita DATE;
    DECLARE @HoraCita TIME;
    DECLARE @FechaHoraCita DATETIME;
    DECLARE @HorasAnticipacion INT;

    SELECT @MontoTotalCita = monto
    FROM pago_Cita
    WHERE Id_cita = @Id_cita;

	SELECT TOP 1 @FechaCita = fecha_cita, @HoraCita = hora_cita
    FROM bitacora_Estatus
    WHERE Id_cita = @Id_cita
	ORDER BY fecha_mov DESC;

    IF @MontoTotalCita IS NOT NULL AND @FechaCita IS NOT NULL
    BEGIN
		SET @FechaHoraCita = DATEADD(MINUTE, DATEDIFF(MINUTE, 0, @HoraCita), CAST(@FechaCita AS DATETIME));
        SET @HorasAnticipacion = DATEDIFF(HOUR, @FechaCancelacion, @FechaHoraCita);
        SET @MontoReembolso = CASE
            WHEN @HorasAnticipacion >= 48 THEN @MontoTotalCita*1.00
            WHEN @HorasAnticipacion >= 24 THEN @MontoTotalCita*0.50
            ELSE 0.00
        END;
    END

    RETURN @MontoReembolso;
END;
GO

/* Valida las credenciales de un usuario.*/
CREATE FUNCTION dbo.ValidarLogin (@Correo NVARCHAR(150), @Contraseña NVARCHAR(255))
RETURNS INT
AS
BEGIN
    DECLARE @Id_usuario_valido INT = 0;

    SELECT @Id_usuario_valido = Id_usuario
    FROM Usuario
    WHERE correo = @Correo AND contraseña = @Contraseña; 

    RETURN ISNULL(@Id_usuario_valido, 0);
END
GO


-- Verificar si el doctor con Id_doctor = 3 
SELECT dbo.DoctorEnJornada(3, '2025-11-13T10:30:00') AS EstaEnJornada;

-- Verificar si el doctor con Id_doctor = 3 
SELECT dbo.DoctorOcupado(1, '2025-11-15', '10:00:00') AS EstaOcupado;

-- Verificar si el paciente 5 tiene una cita pendiente con el doctor 5
SELECT dbo.PacienteCita(5, 5) AS TienePendiente;

-- Calcular el reembolso para la cita 8, cancelada el 2025-11-10 a las 14:00
SELECT dbo.CalcularReembolso(8, '2025-11-10T14:00:00') AS MontoReembolso;

-- Validar si existe un usuario con correo y contraseña dados
SELECT dbo.ValidarLogin('juanp@gmail.com', '1234') AS IdUsuarioValido;


