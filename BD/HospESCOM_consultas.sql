use HospESCOM

select * from Usuario
select * from TipoUsuario
select * from HorarioEmpleado
select * from Paciente
select * from Doctor
select * from Dia_Semana
select * from cita
select * from bitacora_Estatus
select * from Especialidad
select * from Receta

INSERT INTO bitacora_Estatus (
    estatus_cita,
    fecha_cita,
    hora_cita,
    monto_Dev,
    Politica_cancela,
    Id_cita
)
VALUES (
    'Cita registrada',
    '2025-11-14',
    '14:18:00',
    NULL,
    NULL,
    1
);


SET IDENTITY_INSERT Paciente ON;
INSERT INTO Paciente (Id_Paciente, edad, peso, estatura, sexo, Id_usuario)
VALUES
(3, 40, 85.3, 1.80, 'Masculino', 3);  
SET IDENTITY_INSERT Paciente OFF;-- Miguel Ruiz López

INSERT INTO HorarioEmpleado (id_Empleado, Id_Dia, hora_entrada, hora_salida)
VALUES
(1, 1, '08:00', '16:00'),  -- Lunes
(1, 2, '08:00', '16:00'),  -- Martes
(1, 3, '08:00', '16:00'),  -- Miércoles
(1, 4, '08:00', '16:00'),  -- Jueves
(1, 5, '08:00', '16:00'),  -- Viernes
(1, 6, '08:00', '14:00');  -- Sábado

-------------------------------------------------------------
-- 1? TABLA: TipoUsuario
-------------------------------------------------------------
INSERT INTO TipoUsuario (NombreUsuario)
VALUES
('Doctor'),
('Recepcionista'),
('Paciente');

-------------------------------------------------------------
-- 2? TABLA: Usuario
-------------------------------------------------------------
INSERT INTO Usuario (nombre, apellido_P, apellido_M, curp, correo, contraseña, calle, colonia, CP, num_Tel, Id_tipoUsuario)
VALUES
('Edgardo', 'Hernández', 'Madrigal', 'HEME800830HDFNRD09', 'edgardo@hospescom.com', '1234', 'Av. Central 123', 'Centro', '07400', '5561283734', 1),
('Laura', 'Sánchez', 'Reyes', 'SARE920104MDFNRS07', 'laura@hospescom.com', '1234', 'Calle Sur 456', 'Roma', '03100', '5534567890', 2),
('Miguel', 'Ruiz', 'Lopez', 'RULM850215HDFNRG03', 'miguel@hospescom.com', '1234', 'Calle Norte 789', 'Del Valle', '03103', '5545678901', 3);

-------------------------------------------------------------
-- 3? TABLA: Empleado
-------------------------------------------------------------
INSERT INTO Empleado (puesto, salario, Id_usuario)
VALUES
('Doctor General', 25000.00, 1),      -- Edgardo
('Recepcionista', 12000.00, 2);       -- Laura

-------------------------------------------------------------
-- 4? TABLA: Especialidad
-------------------------------------------------------------
INSERT INTO Especialidad (tipo_Especialidad, descripcion, costo_especialidad)
VALUES
('Medicina General', 'Atención general de pacientes', 500.00),
('Cardiología', 'Estudios y diagnóstico de enfermedades del corazón', 1200.00),
('Dermatología', 'Tratamiento de enfermedades de la piel', 900.00);

-------------------------------------------------------------
-- 5? TABLA: Consultorio
-------------------------------------------------------------
INSERT INTO Consultorio (disponibilidad)
VALUES
(1),
(1);

-------------------------------------------------------------
-- 6? TABLA: Doctor
-------------------------------------------------------------
INSERT INTO Doctor (cedula_Pro, disponibilidad, Id_usuario, Id_especialidad, Id_consultorio)
VALUES
('DOC123456', 1, 1, 1, 1);

-------------------------------------------------------------
-- 7? TABLA: Recepcionista
-------------------------------------------------------------
INSERT INTO Recepcionista (Id_usuario)
VALUES
(2);

-------------------------------------------------------------
-- 8? TABLA: Dia_Semana
-- Solo ejecutar si está vacía
-------------------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM Dia_Semana)
BEGIN
    INSERT INTO Dia_Semana (Id_Dia, nombre_dia)
    VALUES
    (1, 'Lunes'),
    (2, 'Martes'),
    (3, 'Miércoles'),
    (4, 'Jueves'),
    (5, 'Viernes'),
    (6, 'Sábado'),
    (7, 'Domingo');
END;

-------------------------------------------------------------
-- 9? TABLA: HorarioEmpleado
-------------------------------------------------------------
INSERT INTO HorarioEmpleado (id_Empleado, Id_Dia, hora_entrada, hora_salida)
VALUES
(1, 1, '08:00', '16:00'),  -- Doctor lunes
(1, 2, '08:00', '16:00'),  -- Doctor martes
(2, 1, '09:00', '17:00');  -- Recepcionista lunes
