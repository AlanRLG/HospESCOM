USE master;
GO

IF DB_ID('HospESCOM') IS NOT NULL
BEGIN
    ALTER DATABASE HospESCOM SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE HospESCOM;
END
GO

-- Creación de la Base de Datos
CREATE DATABASE HospESCOM;
GO

USE HospESCOM;
GO

-- Tabla: TipoUsuario
CREATE TABLE TipoUsuario (
    Id_tipoUsuario INT PRIMARY KEY IDENTITY(1,1),
    NombreUsuario NVARCHAR(100) NOT NULL
);
GO

-- Tabla: Usuario
CREATE TABLE Usuario (
    Id_usuario INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido_P NVARCHAR(100) NOT NULL,
    apellido_M NVARCHAR(100),
    curp NVARCHAR(18) UNIQUE NOT NULL,
    correo NVARCHAR(150) UNIQUE NOT NULL,
    contraseña NVARCHAR(255) NOT NULL,
    calle NVARCHAR(150),
    colonia NVARCHAR(100),
    CP NVARCHAR(10),
    num_Tel NVARCHAR(20),
    Id_tipoUsuario INT NOT NULL,
    FOREIGN KEY (Id_tipoUsuario) REFERENCES TipoUsuario(Id_tipoUsuario)
);
GO

-- Tabla: Empleado
CREATE TABLE Empleado (
    id_Empleado INT PRIMARY KEY IDENTITY(1,1),
    puesto NVARCHAR(100) NOT NULL,
    salario DECIMAL(10,2),
    Id_usuario INT NOT NULL,
    FOREIGN KEY (Id_usuario) REFERENCES Usuario(Id_usuario)
);
GO

-- Tabla: Recepcionista
CREATE TABLE Recepcionista (
    id_Recepcionista INT PRIMARY KEY IDENTITY(1,1),
    Id_usuario INT NOT NULL,
    FOREIGN KEY (Id_usuario) REFERENCES Empleado(id_Empleado)
);
GO

-- Tabla: Especialidad
CREATE TABLE Especialidad (
    Id_Especialidad INT PRIMARY KEY IDENTITY(1,1),
    tipo_Especialidad NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(500),
    costo_especialidad DECIMAL(10,2)
);
GO

-- Tabla: Consultorio
CREATE TABLE Consultorio (
    Id_consultorio INT PRIMARY KEY IDENTITY(1,1),
    disponibilidad BIT NOT NULL,
);
GO

-- Tabla: Doctor
CREATE TABLE Doctor (
    Id_doctor INT PRIMARY KEY IDENTITY(1,1),
    cedula_Pro NVARCHAR(50) UNIQUE NOT NULL,
    disponibilidad BIT NOT NULL,
    Id_usuario INT NOT NULL,
    Id_especialidad INT NOT NULL,
    Id_consultorio INT NOT NULL,
    FOREIGN KEY (Id_usuario) REFERENCES Empleado(id_Empleado),
    FOREIGN KEY (Id_especialidad) REFERENCES Especialidad(Id_Especialidad),
    FOREIGN KEY (Id_consultorio) REFERENCES Consultorio(Id_consultorio)
);
GO

-- Tabla: Paciente
CREATE TABLE Paciente (
    Id_Paciente INT PRIMARY KEY IDENTITY(1,1),
    edad INT NOT NULL,
    peso DECIMAL(5,2),
    estatura DECIMAL(5,2),
    sexo NVARCHAR(10),
    Tipo_sangre NVARCHAR(10),
    contacto_Emer NVARCHAR(100),
    fecha_Regis DATETIME DEFAULT GETDATE(),
    Id_usuario INT NOT NULL,
    FOREIGN KEY (Id_usuario) REFERENCES Usuario(Id_usuario)
);
GO

-- Tabla: Cita
CREATE TABLE Cita (
    Id_cita INT PRIMARY KEY IDENTITY(1,1),
    fecha_limite DATETIME,
    Id_paciente INT NOT NULL,
    Id_doctor INT NOT NULL,
    FOREIGN KEY (Id_paciente) REFERENCES Paciente(Id_Paciente),
    FOREIGN KEY (Id_doctor) REFERENCES Doctor(Id_doctor)
);
GO

-- Tabla: bitacora_Estatus
CREATE TABLE bitacora_Estatus (
    Id_bitacoraEstatus INT PRIMARY KEY IDENTITY(1,1),
    fecha_mov DATETIME DEFAULT GETDATE(),
    estatus_cita NVARCHAR(50),
    fecha_cita DATE NOT NULL,
    hora_cita TIME NOT NULL,
    monto_Dev DECIMAL(10,2),
    Politica_cancela NVARCHAR(500),
    Id_cita INT NOT NULL,
    FOREIGN KEY (Id_cita) REFERENCES Cita(Id_cita)
);
GO

-- Tabla: pago_Cita
CREATE TABLE pago_Cita (
    id_pago INT PRIMARY KEY IDENTITY(1,1),
    fecha_pago DATETIME DEFAULT GETDATE(),
    estado_pago NVARCHAR(50),
    monto DECIMAL(10,2),
    metodo_pagoC NVARCHAR(50),
    des_pago NVARCHAR(500),
    Id_usuario INT NOT NULL,
    Id_cita INT NOT NULL,
    FOREIGN KEY (Id_usuario) REFERENCES Usuario(Id_usuario),
    FOREIGN KEY (Id_cita) REFERENCES Cita(Id_cita)
);
GO

-- Tabla: Receta
CREATE TABLE Receta (
    Id_Receta INT PRIMARY KEY IDENTITY(1,1),
    fecha_receta DATE DEFAULT CAST(GETDATE() AS DATE),
    cantidad_receta INT,
    diagnostico NVARCHAR(500),
    tratamiento NVARCHAR(500),
    observaciones NVARCHAR(500),
    duracion NVARCHAR(100),
    frecuencia NVARCHAR(100),
    Id_Cita INT NOT NULL,
    FOREIGN KEY (Id_Cita) REFERENCES Cita(Id_cita)
);
GO

-- Tabla: Farmacia_Medicamentos
CREATE TABLE Farmacia_Medicamentos (
    Id_medicamento INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(200) NOT NULL,
    precio_med DECIMAL(10,2) NOT NULL,
    fecha_caducidad DATE,
    lote NVARCHAR(50),
    cantidad INT NOT NULL
);
GO

-- Tabla: Venta_Med
CREATE TABLE Venta_Med (
    Id_VentaMed INT PRIMARY KEY IDENTITY(1,1),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal AS (cantidad * precio_unitario) PERSISTED,
    Id_Medicamento INT NOT NULL,
    Id_recepcionista INT NOT NULL,
    FOREIGN KEY (Id_Medicamento) REFERENCES Farmacia_Medicamentos(Id_medicamento),
    FOREIGN KEY (Id_recepcionista) REFERENCES Recepcionista(id_Recepcionista)
);
GO

-- Tabla: Servicio
CREATE TABLE Servicio (
    Id_Servicio INT PRIMARY KEY IDENTITY(1,1),
    nombre_servicio NVARCHAR(200) NOT NULL,
    costo DECIMAL(10,2) NOT NULL,
    descripcion NVARCHAR(500),
);
GO

-- Tabla: Venta_servicio
CREATE TABLE Venta_servicio (
    id_VentaServicio INT PRIMARY KEY IDENTITY(1,1),
    tipo_servicio NVARCHAR(100),
    subtotal DECIMAL(10,2), 
    id_Servicio INT NOT NULL,
    Id_recepcionista INT NOT NULL,
    FOREIGN KEY (id_Servicio) REFERENCES Servicio(Id_Servicio),
    FOREIGN KEY (Id_recepcionista) REFERENCES Recepcionista(id_Recepcionista)
);
GO

-- Tabla: Ticket
CREATE TABLE Ticket (
    id_ticket INT PRIMARY KEY IDENTITY(1,1),
    costo_total DECIMAL(10,2) NOT NULL,
    id_VentaServicio INT,
    id_VentaMed INT,
    FOREIGN KEY (id_VentaServicio) REFERENCES Venta_servicio(id_VentaServicio),
    FOREIGN KEY (id_VentaMed) REFERENCES Venta_Med(Id_VentaMed)
);
GO

-- Tabla: pago_Ticket
CREATE TABLE pago_Ticket (
    id_pagoTicket INT PRIMARY KEY IDENTITY(1,1),
    fecha_pago DATETIME DEFAULT GETDATE(),
    estado_pagoT NVARCHAR(50),
    metodo_pagoT NVARCHAR(50),
    des_pagoT NVARCHAR(500),
    id_ticket INT NOT NULL,
    FOREIGN KEY (id_ticket) REFERENCES Ticket(id_ticket)
);
GO

-- Tabla: Cliente
CREATE TABLE Cliente (
    Id_Cliente INT PRIMARY KEY IDENTITY(1,1),
    nombreC NVARCHAR(200) NOT NULL,
    numeroC NVARCHAR(20),
    correoC NVARCHAR(150),
    genero NVARCHAR(20)
);
GO

-- Tabla intermedia: Cliente_Venta_servicio (relación M:M entre Cliente y Venta_servicio)
CREATE TABLE Cliente_Venta_servicio (
    Id_Cliente INT NOT NULL,
    id_VentaServicio INT NOT NULL,
    PRIMARY KEY (Id_Cliente, id_VentaServicio),
    FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente),
    FOREIGN KEY (id_VentaServicio) REFERENCES Venta_servicio(id_VentaServicio)
);
GO

-- Tabla intermedia: Cliente_Venta_Med (relación M:M entre Cliente y Venta_Med)
CREATE TABLE Cliente_Venta_Med (
    Id_Cliente INT NOT NULL,
    Id_VentaMed INT NOT NULL,
    PRIMARY KEY (Id_Cliente, Id_VentaMed),
    FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente),
    FOREIGN KEY (Id_VentaMed) REFERENCES Venta_Med(Id_VentaMed)
);
GO

-- Tabla: Alergia
CREATE TABLE Alergia (
    Id_Alergia INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(150) UNIQUE NOT NULL
);
GO

-- Tabla Paciente_Alergia
CREATE TABLE Paciente_Alergia (
    Id_Paciente INT NOT NULL,
    Id_Alergia INT NOT NULL,
    PRIMARY KEY (Id_Paciente, Id_Alergia),
    FOREIGN KEY (Id_Paciente) REFERENCES Paciente(Id_Paciente),
    FOREIGN KEY (Id_Alergia) REFERENCES Alergia(Id_Alergia)
);
GO

-- Tabla Padecimiento
CREATE TABLE Padecimiento (
    Id_Padecimiento INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(150) UNIQUE NOT NULL
);
GO

-- Tabla Paciente_padefimiento
CREATE TABLE Paciente_Padecimiento (
    Id_Paciente INT NOT NULL,
    Id_Padecimiento INT NOT NULL,
    PRIMARY KEY (Id_Paciente, Id_Padecimiento),
    FOREIGN KEY (Id_Paciente) REFERENCES Paciente(Id_Paciente),
    FOREIGN KEY (Id_Padecimiento) REFERENCES Padecimiento(Id_Padecimiento)
);
GO

-- Tablas para Consultorio (Equipamento)
CREATE TABLE Equipo_Medico (
    Id_Equipo INT PRIMARY KEY IDENTITY(1,1),
    nombre_equipo NVARCHAR(150) UNIQUE NOT NULL,
    descripcion NVARCHAR(500)
);
GO

-- Tabla: Consultorio_Equipo
CREATE TABLE Consultorio_Equipo (
    Id_consultorio INT NOT NULL,
    Id_Equipo INT NOT NULL,
    cantidad_asignada INT NOT NULL DEFAULT 1,
    PRIMARY KEY (Id_consultorio, Id_Equipo),
    FOREIGN KEY (Id_consultorio) REFERENCES Consultorio(Id_consultorio),
    FOREIGN KEY (Id_Equipo) REFERENCES Equipo_Medico(Id_Equipo)
);
GO

-- Tablas para Empleado y Servicio (Horarios)
CREATE TABLE Dia_Semana (
    Id_Dia INT PRIMARY KEY, 
    nombre_dia NVARCHAR(20) UNIQUE NOT NULL
);
GO

-- Tabla: Horario Empleado
CREATE TABLE HorarioEmpleado (
    Id_HorarioEmpleado INT PRIMARY KEY IDENTITY(1,1),
    id_Empleado INT NOT NULL,
    Id_Dia INT NOT NULL,
    hora_entrada TIME NOT NULL,
    hora_salida TIME NOT NULL,
    FOREIGN KEY (id_Empleado) REFERENCES Empleado(id_Empleado),
    FOREIGN KEY (Id_Dia) REFERENCES Dia_Semana(Id_Dia)
);
GO

-- Tabla Horario_Servicio
CREATE TABLE Horario_Servicio (
    Id_HorarioServicio INT PRIMARY KEY IDENTITY(1,1),
    id_Servicio INT NOT NULL,
    Id_Dia INT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (id_Servicio) REFERENCES Servicio(Id_Servicio),
    FOREIGN KEY (Id_Dia) REFERENCES Dia_Semana(Id_Dia)
);
GO
