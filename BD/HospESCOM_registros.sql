USE HospESCOM;
GO

-- 1️ TipoUsuario
INSERT INTO TipoUsuario (NombreUsuario) VALUES
('Doctor'),
('Recepcionista'),
('Paciente'),
('Farmacéutico'),
('Limpieza'),
('Técnico'),
('Contador'),
('Seguridad'),
('Gerente'),
('Otro');
GO

-- 2️ Usuario
INSERT INTO Usuario (nombre, apellido_P, apellido_M, curp, correo, contraseña, calle, colonia, CP, num_Tel, Id_tipoUsuario) VALUES
('Diego','Alonso','González','CURPDR0001','doc1@hosp.com','docpass1','Calle 1','Col A','01000','5510000001',1),
('Mariana','Beltrán','Ruiz','CURPDR0002','doc2@hosp.com','docpass2','Calle 2','Col A','01001','5510000002',1),
('Luis','Carera','Sánchez','CURPDR0003','doc3@hosp.com','docpass3','Calle 3','Col A','01002','5510000003',1),
('Ana','Díaz','Ortiz','CURPDR0004','doc4@hosp.com','docpass4','Calle 4','Col A','01003','5510000004',1),
('Pablo','Echeverría','Morales','CURPDR0005','doc5@hosp.com','docpass5','Calle 5','Col B','01004','5510000005',1),
('Sofía','Fernández','Lima','CURPDR0006','doc6@hosp.com','docpass6','Calle 6','Col B','01005','5510000006',1),
('Raúl','Gómez','Soto','CURPDR0007','doc7@hosp.com','docpass7','Calle 7','Col B','01006','5510000007',1),
('Carla','Hernández','Paz','CURPDR0008','doc8@hosp.com','docpass8','Calle 8','Col B','01007','5510000008',1),
('Iván','Ibarra','Núñez','CURPDR0009','doc9@hosp.com','docpass9','Calle 9','Col C','01008','5510000009',1),
('Lucía','Juárez','Campos','CURPDR0010','doc10@hosp.com','docpass10','Calle 10','Col C','01009','5510000010',1),
('Fernando','Klein','Ramos','CURPDR0011','doc11@hosp.com','docpass11','Calle 11','Col C','01010','5510000011',1),
('María','Lara','Vega','CURPDR0012','doc12@hosp.com','docpass12','Calle 12','Col C','01011','5510000012',1),
('Jorge','Mendoza','Lopez','CURPDR0013','doc13@hosp.com','docpass13','Calle 13','Col D','01012','5510000013',1),
('Valeria','Noriega','Reyes','CURPDR0014','doc14@hosp.com','docpass14','Calle 14','Col D','01013','5510000014',1),
('Diego','Ocampo','Roldán','CURPDR0015','doc15@hosp.com','docpass15','Calle 15','Col D','01014','5510000015',1),
('Elena','Paredes','Sáenz','CURPDR0016','doc16@hosp.com','docpass16','Calle 16','Col D','01015','5510000016',1),
('Antonio','Quijano','Blanco','CURPDR0017','doc17@hosp.com','docpass17','Calle 17','Col E','01016','5510000017',1),
('Marta','Rentería','Alarcón','CURPDR0018','doc18@hosp.com','docpass18','Calle 18','Col E','01017','5510000018',1),
('Sergio','Salinas','Molina','CURPDR0019','doc19@hosp.com','docpass19','Calle 19','Col E','01018','5510000019',1),
('Patricia','Torres','Paz','CURPDR0020','doc20@hosp.com','docpass20','Calle 20','Col E','01019','5510000020',1),
('Ricardo','Ugalde','Herrera','CURPDR0021','doc21@hosp.com','docpass21','Calle 21','Col F','01020','5510000021',1),
('Sonia','Vargas','Gallo','CURPDR0022','doc22@hosp.com','docpass22','Calle 22','Col F','01021','5510000022',1),
('Marco','Wong','Ruiz','CURPDR0023','doc23@hosp.com','docpass23','Calle 23','Col F','01022','5510000023',1),
('Paola','Xochitl','Cervantes','CURPDR0024','doc24@hosp.com','docpass24','Calle 24','Col F','01023','5510000024',1),
('Óscar','Yáñez','Pineda','CURPDR0025','doc25@hosp.com','docpass25','Calle 25','Col G','01024','5510000025',1),
('Claudia','Zamora','León','CURPDR0026','doc26@hosp.com','docpass26','Calle 26','Col G','01025','5510000026',1),
('Hugo','Ávila','Ríos','CURPDR0027','doc27@hosp.com','docpass27','Calle 27','Col G','01026','5510000027',1),
('Gabriela','Benítez','Márquez','CURPDR0028','doc28@hosp.com','docpass28','Calle 28','Col G','01027','5510000028',1),
('Nicolás','Cano','Reina','CURPDR0029','doc29@hosp.com','docpass29','Calle 29','Col H','01028','5510000029',1),
('Adriana','Domínguez','Sosa','CURPDR0030','doc30@hosp.com','docpass30','Calle 30','Col H','01029','5510000030',1),
('Andrés','Espinosa','Torres','CURPDR0031','doc31@hosp.com','docpass31','Calle 31','Col H','01030','5510000031',1),
('Isabel','Flores','Jiménez','CURPDR0032','doc32@hosp.com','docpass32','Calle 32','Col H','01031','5510000032',1),
('Víctor','Guerra','Nava','CURPDR0033','doc33@hosp.com','docpass33','Calle 33','Col I','01032','5510000033',1),
('Teresa','Herrera','Cruz','CURPDR0034','doc34@hosp.com','docpass34','Calle 34','Col I','01033','5510000034',1),
('Emilio','Iglesias','Villar','CURPDR0035','doc35@hosp.com','docpass35','Calle 35','Col I','01034','5510000035',1),
('Natalia','Jiménez','Paz','CURPDR0036','doc36@hosp.com','docpass36','Calle 36','Col I','01035','5510000036',1),
('Félix','Kuri','Salcedo','CURPDR0037','doc37@hosp.com','docpass37','Calle 37','Col J','01036','5510000037',1),
('Renata','Lugo','Delgado','CURPDR0038','doc38@hosp.com','docpass38','Calle 38','Col J','01037','5510000038',1),
('Gonzalo','Muri','Vargas','CURPDR0039','doc39@hosp.com','docpass39','Calle 39','Col J','01038','5510000039',1),
('Paula','Noriega','Sánchez','CURPDR0040','doc40@hosp.com','docpass40','Calle 40','Col J','01039','5510000040',1),
('Rocio','Perez','Martínez','CURPREC0041','recep1@hosp.com','recpass1','Av 1','Col R','02000','5520000041',2),
('Hector','Salas','Gómez','CURPREC0042','recep2@hosp.com','recpass2','Av 2','Col R','02001','5520000042',2),
('Mónica','Ortiz','Vera','CURPREC0043','recep3@hosp.com','recpass3','Av 3','Col R','02002','5520000043',2),
('Ivette','Quintana','López','CURPREC0044','recep4@hosp.com','recpass4','Av 4','Col R','02003','5520000044',2),
('Diego','Ramos','Pineda','CURPREC0045','recep5@hosp.com','recpass5','Av 5','Col R','02004','5520000045',2),
('Karina','Sosa','Delgado','CURPREC0046','recep6@hosp.com','recpass6','Av 6','Col R','02005','5520000046',2),
('Mario','Tovar','Mendoza','CURPREC0047','recep7@hosp.com','recpass7','Av 7','Col R','02006','5520000047',2),
('Luz','Urbina','Castro','CURPREC0048','recep8@hosp.com','recpass8','Av 8','Col R','02007','5520000048',2),
('Brenda','Vega','Paz','CURPREC0049','recep9@hosp.com','recpass9','Av 9','Col R','02008','5520000049',2),
('Raul','Zambrano','Ruiz','CURPREC0050','recep10@hosp.com','recpass10','Av 10','Col R','02009','5520000050',2),
('Andres','Pac','Uno','CURPPAC0051','pac1@hosp.com','pacpass1','Calle P1','Col P','03000','5530000051',3),
('Beatriz','Pac','Dos','CURPPAC0052','pac2@hosp.com','pacpass2','Calle P2','Col P','03001','5530000052',3),
('Cesar','Pac','Tres','CURPPAC0053','pac3@hosp.com','pacpass3','Calle P3','Col P','03002','5530000053',3),
('Denise','Pac','Cuatro','CURPPAC0054','pac4@hosp.com','pacpass4','Calle P4','Col P','03003','5530000054',3),
('Esteban','Pac','Cinco','CURPPAC0055','pac5@hosp.com','pacpass5','Calle P5','Col P','03004','5530000055',3),
('Fabiana','Pac','Seis','CURPPAC0056','pac6@hosp.com','pacpass6','Calle P6','Col P','03005','5530000056',3),
('Guillermo','Pac','Siete','CURPPAC0057','pac7@hosp.com','pacpass7','Calle P7','Col P','03006','5530000057',3),
('Helena','Pac','Ocho','CURPPAC0058','pac8@hosp.com','pacpass8','Calle P8','Col P','03007','5530000058',3),
('Ignacio','Pac','Nueve','CURPPAC0059','pac9@hosp.com','pacpass9','Calle P9','Col P','03008','5530000059',3),
('Julieta','Pac','Diez','CURPPAC0060','pac10@hosp.com','pacpass10','Calle P10','Col P','03009','5530000060',3);
GO

-- 3️ Empleado
INSERT INTO Empleado (puesto, salario, Id_usuario) VALUES
('Doctor General',15000.00,1),
('Doctor General',15000.00,2),
('Doctor General',15000.00,3),
('Doctor General',15000.00,4),
('Cardiólogo',20000.00,5),
('Cardiólogo',20000.00,6),
('Cardiólogo',20000.00,7),
('Cardiólogo',20000.00,8),
('Pediatra',18000.00,9),
('Pediatra',18000.00,10),
('Pediatra',18000.00,11),
('Pediatra',18000.00,12),
('Dermatólogo',16000.00,13),
('Dermatólogo',16000.00,14),
('Dermatólogo',16000.00,15),
('Dermatólogo',16000.00,16),
('Oftalmólogo',17000.00,17),
('Oftalmólogo',17000.00,18),
('Oftalmólogo',17000.00,19),
('Oftalmólogo',17000.00,20),
('Neurólogo',22000.00,21),
('Neurólogo',22000.00,22),
('Neurólogo',22000.00,23),
('Neurólogo',22000.00,24),
('Gastroenterólogo',19000.00,25),
('Gastroenterólogo',19000.00,26),
('Gastroenterólogo',19000.00,27),
('Gastroenterólogo',19000.00,28),
('Psiquiatra',20000.00,29),
('Psiquiatra',20000.00,30),
('Psiquiatra',20000.00,31),
('Psiquiatra',20000.00,32),
('Oncólogo',26000.00,33),
('Oncólogo',26000.00,34),
('Oncólogo',26000.00,35),
('Oncólogo',26000.00,36),
('Ortopedista',18000.00,37),
('Ortopedista',18000.00,38),
('Ortopedista',18000.00,39),
('Ortopedista',18000.00,40),
('Recepcionista',10000.00,41),
('Recepcionista',10000.00,42),
('Recepcionista',9500.00,43),
('Recepcionista',9500.00,44),
('Recepcionista',9000.00,45),
('Recepcionista',9000.00,46),
('Recepcionista',9200.00,47),
('Recepcionista',9200.00,48),
('Recepcionista',9000.00,49),
('Recepcionista',9000.00,50);
GO

-- 4️ Recepcionista (usa id_Empleado)
INSERT INTO Recepcionista (Id_usuario) VALUES
(41),(42),(43),(44),(45),(46),(47),(48),(49),(50);
GO

-- 5️ Especialidad
INSERT INTO Especialidad (tipo_Especialidad, descripcion, costo_especialidad) VALUES
('Medicina General','Consultas básicas',500.00),
('Cardiología','Corazón y sistema circulatorio',900.00),
('Pediatría','Niños y adolescentes',700.00),
('Dermatología','Piel',650.00),
('Oftalmología','Vista y ojos',800.00),
('Neurología','Sistema nervioso',1200.00),
('Gastroenterología','Sistema digestivo',950.00),
('Psiquiatría','Salud mental',1000.00),
('Oncología','Cáncer y tumores',1500.00),
('Ortopedia','Huesos y músculos',850.00);
GO

-- 6️ Consultorio
INSERT INTO Consultorio (disponibilidad) VALUES
(1),(1),(1),(0),(1),(1),(0),(1),(1),(1);
GO

-- 7️ Doctor
INSERT INTO Doctor (cedula_Pro, disponibilidad, Id_usuario, Id_especialidad, Id_consultorio) VALUES
('CED-D001',1,1,1,1),
('CED-D002',1,2,1,2),
('CED-D003',1,3,1,3),
('CED-D004',1,4,1,4),
('CED-D005',1,5,2,5),
('CED-D006',1,6,2,6),
('CED-D007',1,7,2,7),
('CED-D008',1,8,2,8),
('CED-D009',1,9,3,9),
('CED-D010',1,10,3,10),
('CED-D011',1,11,3,1),
('CED-D012',1,12,3,2),
('CED-D013',1,13,4,3),
('CED-D014',1,14,4,4),
('CED-D015',1,15,4,5),
('CED-D016',1,16,4,6),
('CED-D017',1,17,5,7),
('CED-D018',1,18,5,8),
('CED-D019',1,19,5,9),
('CED-D020',1,20,5,10),
('CED-D021',1,21,6,1),
('CED-D022',1,22,6,2),
('CED-D023',1,23,6,3),
('CED-D024',1,24,6,4),
('CED-D025',1,25,7,5),
('CED-D026',1,26,7,6),
('CED-D027',1,27,7,7),
('CED-D028',1,28,7,8),
('CED-D029',1,29,8,9),
('CED-D030',1,30,8,10),
('CED-D031',1,31,8,1),
('CED-D032',1,32,8,2),
('CED-D033',1,33,9,3),
('CED-D034',1,34,9,4),
('CED-D035',1,35,9,5),
('CED-D036',1,36,9,6),
('CED-D037',1,37,10,7),
('CED-D038',1,38,10,8),
('CED-D039',1,39,10,9),
('CED-D040',1,40,10,10);
GO

-- 8️ Paciente
INSERT INTO Paciente (edad, peso, estatura, sexo, Tipo_sangre, contacto_Emer, Id_usuario) VALUES
(25,60.50,1.65,'F','O+','Contacto A',51),
(30,80.20,1.70,'M','A+','Contacto B',52),
(28,70.00,1.68,'F','B+','Contacto C',53),
(35,90.30,1.75,'M','O-','Contacto D',54),
(45,72.50,1.62,'F','A-','Contacto E',55),
(19,55.00,1.60,'F','O+','Contacto F',56),
(50,95.00,1.80,'M','B-','Contacto G',57),
(40,68.00,1.66,'F','AB+','Contacto H',58),
(33,85.20,1.73,'M','A+','Contacto I',59),
(60,78.10,1.70,'F','O-','Contacto J',60);
GO

-- 9️ Alergia
INSERT INTO Alergia (nombre)
VALUES ('Polen'),('Penicilina'),('Mariscos'),('Lácteos'),('Polvo'),('Frutos secos'),('Pescado'),('Latex'),('Gluten'),('Ninguna');
GO

--10 Paciente_Alergia
INSERT INTO Paciente_Alergia (Id_Paciente, Id_Alergia)
VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);
GO

-- 11️ Padecimiento
INSERT INTO Padecimiento (nombre)
VALUES ('Asma'),('Diabetes'),('Hipertensión'),('Gastritis'),('Migraña'),
       ('Alergia crónica'),('Artritis'),('Anemia'),('Depresión'),('Ninguno');
GO

-- 12️ Paciente_Padecimiento
INSERT INTO Paciente_Padecimiento (Id_Paciente, Id_Padecimiento)
VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);
GO

-- 13️ Cita
INSERT INTO Cita (fecha_limite, Id_paciente, Id_doctor) VALUES
('2025-11-17 09:00',1,1),
('2025-11-17 10:00',2,2),
('2025-11-17 11:00',3,3),
('2025-11-17 12:00',4,4),
('2025-11-17 13:00',5,5),
('2025-11-17 14:00',6,6),
('2025-11-17 15:00',7,7),
('2025-11-17 16:00',8,8),
('2025-11-18 09:00',9,9),
('2025-11-18 10:00',10,10);
GO

-- 14️ bitacora_Estatus
INSERT INTO bitacora_Estatus (estatus_cita, fecha_cita, hora_cita, monto_Dev, Politica_cancela, Id_cita)
VALUES
('Agendada','2025-11-15','10:00',0,'24h antes sin penalización',1),
('Agendada','2025-11-16','11:00',0,'24h antes sin penalización',2),
('Agendada','2025-11-17','12:00',0,'24h antes sin penalización',3),
('Cancelada','2025-11-18','13:00',100,'Reembolso parcial',4),
('Completada','2025-11-19','14:00',0,'N/A',5),
('Completada','2025-11-20','15:00',0,'N/A',6),
('Reprogramada','2025-11-21','09:00',0,'N/A',7),
('Agendada','2025-11-22','10:00',0,'N/A',8),
('Cancelada','2025-11-23','11:00',50,'N/A',9),
('Completada','2025-11-24','12:00',0,'N/A',10);
GO

-- 15️ pago_Cita
INSERT INTO pago_Cita (estado_pago, monto, metodo_pagoC, des_pago, Id_usuario, Id_cita)
VALUES
('Pagado',500,'Tarjeta','Pago online',41,1),
('Pagado',700,'Efectivo','En recepción',42,2),
('Pendiente',600,'Tarjeta','Pago fallido',43,3),
('Pagado',800,'Transferencia','Pago directo',44,4),
('Pagado',900,'Tarjeta','En línea',45,5),
('Pendiente',550,'Efectivo','Esperando',46,6),
('Pagado',500,'Tarjeta','Listo',47,7),
('Pagado',750,'Efectivo','Caja',48,8),
('Pendiente',650,'Tarjeta','Verificación',49,9),
('Pagado',600,'Transferencia','Pagado',50,10);
GO

-- 16️ Receta
INSERT INTO Receta (cantidad_receta, diagnostico, tratamiento, observaciones, duracion, frecuencia, Id_Cita)
VALUES
(1,'Gripe','Paracetamol','Descanso','5 días','8h',1),
(1,'Dolor cabeza','Ibuprofeno','Hidratación','3 días','12h',2),
(1,'Fiebre','Tempra','Descanso','4 días','8h',3),
(1,'Tos','Jarabe','No fumar','7 días','12h',4),
(1,'Gastritis','Omeprazol','Ayuno parcial','10 días','24h',5),
(1,'Alergia','Loratadina','Evitar polvo','5 días','8h',6),
(1,'Asma','Salbutamol','Uso diario','15 días','12h',7),
(1,'Migraña','Naproxeno','Evitar luz fuerte','3 días','12h',8),
(1,'Colesterol','Atorvastatina','Control médico','30 días','24h',9),
(1,'Dolor muscular','Diclofenaco','Ejercicio leve','5 días','8h',10);
GO

-- 17️ Farmacia_Medicamentos
INSERT INTO Farmacia_Medicamentos (nombre, precio_med, fecha_caducidad, lote, cantidad)
VALUES
('Paracetamol',50,'2026-01-01','L1',100),
('Ibuprofeno',60,'2026-02-01','L2',200),
('Tempra',55,'2026-03-01','L3',150),
('Jarabe Cough',70,'2026-04-01','L4',80),
('Omeprazol',90,'2026-05-01','L5',120),
('Loratadina',45,'2026-06-01','L6',300),
('Salbutamol',110,'2026-07-01','L7',50),
('Naproxeno',65,'2026-08-01','L8',75),
('Atorvastatina',130,'2026-09-01','L9',60),
('Diclofenaco',75,'2026-10-01','L10',90);
GO

-- 18️ Venta_Med
INSERT INTO Venta_Med (cantidad, precio_unitario, Id_Medicamento, Id_recepcionista)
VALUES
(2,50,1,1),(1,60,2,2),(3,55,3,3),(2,70,4,4),(1,90,5,5),
(2,45,6,6),(1,110,7,7),(3,65,8,8),(1,130,9,9),(2,75,10,10);
GO

-- 19️ Servicio
INSERT INTO Servicio (nombre_servicio, costo, descripcion)
VALUES
('Chequeo General',300,'Revisión básica'),
('Electrocardiograma',800,'Examen cardíaco'),
('Rayos X',700,'Imagen diagnóstica'),
('Ultrasonido',900,'Diagnóstico abdominal'),
('Análisis de Sangre',500,'Estudio clínico'),
('Vacunación',200,'Aplicación de vacuna'),
('Consulta Nutrición',400,'Asesoría alimenticia'),
('Consulta Psicológica',600,'Atención emocional'),
('Fisioterapia',650,'Rehabilitación física'),
('Odontología',750,'Atención dental');
GO

-- 20️ Venta_servicio
INSERT INTO Venta_servicio (tipo_servicio, subtotal, id_Servicio, Id_recepcionista)
VALUES
('Chequeo',300,1,1),('Electro',800,2,2),('RayosX',700,3,3),('Ultra',900,4,4),
('Sangre',500,5,5),('Vacuna',200,6,6),('Nutrición',400,7,7),('Psico',600,8,8),
('Fisio',650,9,9),('Denta',750,10,10);
GO

-- 21️ Ticket
INSERT INTO Ticket (costo_total, id_VentaServicio, id_VentaMed)
VALUES (600,1,1),(860,2,2),(755,3,3),(970,4,4),(590,5,5),(245,6,6),(510,7,7),(665,8,8),(780,9,9),(825,10,10);
GO

-- 22️ pago_Ticket
INSERT INTO pago_Ticket (estado_pagoT, metodo_pagoT, des_pagoT, id_ticket)
VALUES
('Pagado','Tarjeta','Online',1),('Pagado','Efectivo','Mostrador',2),
('Pendiente','Tarjeta','Error',3),('Pagado','Transferencia','Hecho',4),
('Pagado','Efectivo','Caja',5),('Pendiente','Tarjeta','Verificar',6),
('Pagado','Efectivo','Recibido',7),('Pagado','Tarjeta','Online',8),
('Pagado','Transferencia','Ok',9),('Pagado','Efectivo','Completado',10);
GO

-- 23️ Cliente
INSERT INTO Cliente (nombreC, numeroC, correoC, genero)
VALUES
('Luis Torres','5512340001','ltorres@gmail.com','M'),
('Ana Ruiz','5512340002','aruiz@gmail.com','F'),
('Carlos Díaz','5512340003','cdiaz@gmail.com','M'),
('María Soto','5512340004','msoto@gmail.com','F'),
('Pablo Rojas','5512340005','projas@gmail.com','M'),
('Lucía Vega','5512340006','lvega@gmail.com','F'),
('Jorge León','5512340007','jleon@gmail.com','M'),
('Sofía Cruz','5512340008','scruz@gmail.com','F'),
('Daniel Méndez','5512340009','dmendez@gmail.com','M'),
('Elena Torres','5512340010','et@gmail.com','F');
GO

-- 24️ Cliente_Venta_servicio
INSERT INTO Cliente_Venta_servicio (Id_Cliente, id_VentaServicio)
VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);
GO

-- 25️ Cliente_Venta_Med
INSERT INTO Cliente_Venta_Med (Id_Cliente, Id_VentaMed)
VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10);
GO

-- 26️ Equipo_Medico
INSERT INTO Equipo_Medico (nombre_equipo, descripcion)
VALUES
('Estetoscopio','Para auscultación'),
('Tensiómetro','Mide presión arterial'),
('Termómetro','Temperatura corporal'),
('Oxímetro','Nivel de oxígeno'),
('Báscula','Peso corporal'),
('Microscopio','Análisis biológico'),
('Rayos X','Diagnóstico por imagen'),
('Ultrasonido','Exploración interna'),
('Monitor cardíaco','Control cardíaco'),
('Camilla','Atención de pacientes');
GO

-- 27️ Consultorio_Equipo
INSERT INTO Consultorio_Equipo (Id_consultorio, Id_Equipo, cantidad_asignada)
VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1);
GO

--28 Dia_Semana
INSERT INTO Dia_Semana (Id_Dia, nombre_dia) VALUES
(1,'Lunes'),
(2,'Martes'),
(3,'Miércoles'),
(4,'Jueves'),
(5,'Viernes'),
(6,'Sábado'),
(7,'Domingo');
GO

--29 HorarioEmpleado
INSERT INTO HorarioEmpleado (id_Empleado, Id_Dia, hora_entrada, hora_salida) VALUES
(1,1,'08:00','16:00'),(1,2,'08:00','16:00'),(1,3,'08:00','16:00'),(1,4,'08:00','16:00'),(1,5,'08:00','16:00'),
(2,1,'08:00','16:00'),(2,2,'08:00','16:00'),(2,3,'08:00','16:00'),(2,4,'08:00','16:00'),(2,5,'08:00','16:00'),
(3,1,'08:00','16:00'),(3,2,'08:00','16:00'),(3,3,'08:00','16:00'),(3,4,'08:00','16:00'),(3,5,'08:00','16:00'),
(4,1,'08:00','16:00'),(4,2,'08:00','16:00'),(4,3,'08:00','16:00'),(4,4,'08:00','16:00'),(4,5,'08:00','16:00'),
(5,1,'08:00','16:00'),(5,2,'08:00','16:00'),(5,3,'08:00','16:00'),(5,4,'08:00','16:00'),(5,5,'08:00','16:00'),
(6,1,'08:00','16:00'),(6,2,'08:00','16:00'),(6,3,'08:00','16:00'),(6,4,'08:00','16:00'),(6,5,'08:00','16:00'),
(7,1,'08:00','16:00'),(7,2,'08:00','16:00'),(7,3,'08:00','16:00'),(7,4,'08:00','16:00'),(7,5,'08:00','16:00'),
(8,1,'08:00','16:00'),(8,2,'08:00','16:00'),(8,3,'08:00','16:00'),(8,4,'08:00','16:00'),(8,5,'08:00','16:00'),
(9,1,'08:00','16:00'),(9,2,'08:00','16:00'),(9,3,'08:00','16:00'),(9,4,'08:00','16:00'),(9,5,'08:00','16:00'),
(10,1,'08:00','16:00'),(10,2,'08:00','16:00'),(10,3,'08:00','16:00'),(10,4,'08:00','16:00'),(10,5,'08:00','16:00'),
(11,1,'08:00','16:00'),(11,2,'08:00','16:00'),(11,3,'08:00','16:00'),(11,4,'08:00','16:00'),(11,5,'08:00','16:00'),
(12,1,'08:00','16:00'),(12,2,'08:00','16:00'),(12,3,'08:00','16:00'),(12,4,'08:00','16:00'),(12,5,'08:00','16:00'),
(13,1,'08:00','16:00'),(13,2,'08:00','16:00'),(13,3,'08:00','16:00'),(13,4,'08:00','16:00'),(13,5,'08:00','16:00'),
(14,1,'08:00','16:00'),(14,2,'08:00','16:00'),(14,3,'08:00','16:00'),(14,4,'08:00','16:00'),(14,5,'08:00','16:00'),
(15,1,'08:00','16:00'),(15,2,'08:00','16:00'),(15,3,'08:00','16:00'),(15,4,'08:00','16:00'),(15,5,'08:00','16:00'),
(16,1,'08:00','16:00'),(16,2,'08:00','16:00'),(16,3,'08:00','16:00'),(16,4,'08:00','16:00'),(16,5,'08:00','16:00'),
(17,1,'08:00','16:00'),(17,2,'08:00','16:00'),(17,3,'08:00','16:00'),(17,4,'08:00','16:00'),(17,5,'08:00','16:00'),
(18,1,'08:00','16:00'),(18,2,'08:00','16:00'),(18,3,'08:00','16:00'),(18,4,'08:00','16:00'),(18,5,'08:00','16:00'),
(19,1,'08:00','16:00'),(19,2,'08:00','16:00'),(19,3,'08:00','16:00'),(19,4,'08:00','16:00'),(19,5,'08:00','16:00'),
(20,1,'08:00','16:00'),(20,2,'08:00','16:00'),(20,3,'08:00','16:00'),(20,4,'08:00','16:00'),(20,5,'08:00','16:00'),
(21,1,'08:00','16:00'),(21,2,'08:00','16:00'),(21,3,'08:00','16:00'),(21,4,'08:00','16:00'),(21,5,'08:00','16:00'),
(22,1,'08:00','16:00'),(22,2,'08:00','16:00'),(22,3,'08:00','16:00'),(22,4,'08:00','16:00'),(22,5,'08:00','16:00'),
(23,1,'08:00','16:00'),(23,2,'08:00','16:00'),(23,3,'08:00','16:00'),(23,4,'08:00','16:00'),(23,5,'08:00','16:00'),
(24,1,'08:00','16:00'),(24,2,'08:00','16:00'),(24,3,'08:00','16:00'),(24,4,'08:00','16:00'),(24,5,'08:00','16:00'),
(25,1,'08:00','16:00'),(25,2,'08:00','16:00'),(25,3,'08:00','16:00'),(25,4,'08:00','16:00'),(25,5,'08:00','16:00'),
(26,1,'08:00','16:00'),(26,2,'08:00','16:00'),(26,3,'08:00','16:00'),(26,4,'08:00','16:00'),(26,5,'08:00','16:00'),
(27,1,'08:00','16:00'),(27,2,'08:00','16:00'),(27,3,'08:00','16:00'),(27,4,'08:00','16:00'),(27,5,'08:00','16:00'),
(28,1,'08:00','16:00'),(28,2,'08:00','16:00'),(28,3,'08:00','16:00'),(28,4,'08:00','16:00'),(28,5,'08:00','16:00'),
(29,1,'08:00','16:00'),(29,2,'08:00','16:00'),(29,3,'08:00','16:00'),(29,4,'08:00','16:00'),(29,5,'08:00','16:00'),
(30,1,'08:00','16:00'),(30,2,'08:00','16:00'),(30,3,'08:00','16:00'),(30,4,'08:00','16:00'),(30,5,'08:00','16:00'),
(31,1,'08:00','16:00'),(31,2,'08:00','16:00'),(31,3,'08:00','16:00'),(31,4,'08:00','16:00'),(31,5,'08:00','16:00'),
(32,1,'08:00','16:00'),(32,2,'08:00','16:00'),(32,3,'08:00','16:00'),(32,4,'08:00','16:00'),(32,5,'08:00','16:00'),
(33,1,'08:00','16:00'),(33,2,'08:00','16:00'),(33,3,'08:00','16:00'),(33,4,'08:00','16:00'),(33,5,'08:00','16:00'),
(34,1,'08:00','16:00'),(34,2,'08:00','16:00'),(34,3,'08:00','16:00'),(34,4,'08:00','16:00'),(34,5,'08:00','16:00'),
(35,1,'08:00','16:00'),(35,2,'08:00','16:00'),(35,3,'08:00','16:00'),(35,4,'08:00','16:00'),(35,5,'08:00','16:00'),
(36,1,'08:00','16:00'),(36,2,'08:00','16:00'),(36,3,'08:00','16:00'),(36,4,'08:00','16:00'),(36,5,'08:00','16:00'),
(37,1,'08:00','16:00'),(37,2,'08:00','16:00'),(37,3,'08:00','16:00'),(37,4,'08:00','16:00'),(37,5,'08:00','16:00'),
(38,1,'08:00','16:00'),(38,2,'08:00','16:00'),(38,3,'08:00','16:00'),(38,4,'08:00','16:00'),(38,5,'08:00','16:00'),
(39,1,'08:00','16:00'),(39,2,'08:00','16:00'),(39,3,'08:00','16:00'),(39,4,'08:00','16:00'),(39,5,'08:00','16:00'),
(40,1,'08:00','16:00'),(40,2,'08:00','16:00'),(40,3,'08:00','16:00'),(40,4,'08:00','16:00'),(40,5,'08:00','16:00');
GO

--30 Horario_Servicio
INSERT INTO Horario_Servicio (id_Servicio, Id_Dia, hora_inicio, hora_fin)
VALUES
(1, 1, '08:00', '14:00'),
(2, 2, '09:00', '15:00'),
(3, 3, '10:00', '16:00'),
(4, 4, '11:00', '17:00'),
(5, 5, '08:00', '12:00'),
(6, 6, '09:00', '13:00'),
(7, 7, '10:00', '14:00'),
(8, 1, '07:00', '11:00'),
(9, 2, '08:30', '14:30'),
(10, 3, '09:00', '15:00');
GO

SELECT * FROM TipoUsuario;
SELECT * FROM Usuario;
SELECT * FROM Empleado;
SELECT * FROM Recepcionista;
SELECT * FROM Especialidad;
SELECT * FROM Consultorio;
SELECT * FROM Doctor;
SELECT * FROM Paciente;
SELECT * FROM Cita;
SELECT * FROM bitacora_Estatus;
SELECT * FROM pago_Cita;
SELECT * FROM Receta;
SELECT * FROM Farmacia_Medicamentos;
SELECT * FROM Venta_Med;
SELECT * FROM Servicio;
SELECT * FROM Venta_servicio;
SELECT * FROM Ticket;
SELECT * FROM pago_Ticket;
SELECT * FROM Cliente;
SELECT * FROM Cliente_Venta_servicio;
SELECT * FROM Cliente_Venta_Med;
SELECT * FROM Alergia;
SELECT * FROM Paciente_Alergia;
SELECT * FROM Padecimiento;
SELECT * FROM Paciente_Padecimiento;
SELECT * FROM Equipo_Medico;
SELECT * FROM Consultorio_Equipo;
SELECT * FROM Dia_Semana;
SELECT * FROM HorarioEmpleado;
SELECT * FROM Horario_Servicio;
