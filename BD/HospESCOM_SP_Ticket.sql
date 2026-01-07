CREATE PROCEDURE sp_crear_ticket
    @IdRecepcionista INT,
    @IdPaciente INT = NULL,
    @IdCliente INT = NULL,
    @IdTicket INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Ticket (total, fecha, Id_Recepcionista, Id_Paciente, Id_Cliente)
    VALUES (0 ,GETDATE(),  @IdRecepcionista, @IdPaciente, @IdCliente);

    SET @IdTicket = SCOPE_IDENTITY();
END
GO


CREATE PROCEDURE sp_agregar_medicamento_ticket
    @IdTicket INT,
    @IdMedicamento INT,
    @Cantidad INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Stock INT, @Precio DECIMAL(10,2);

    SELECT 
        @Stock = cantidad,
        @Precio = precio_med
    FROM Farmacia_Medicamentos
    WHERE Id_medicamento = @IdMedicamento;

    IF @Cantidad > @Stock
    BEGIN
        RAISERROR('Stock insuficiente', 16, 1);
        RETURN;
    END


    INSERT INTO Ticket_Medicamento
    (Id_Ticket, Id_Medicamento, cantidad, precio_unitario)
    VALUES
    (@IdTicket, @IdMedicamento, @Cantidad, @Precio);

    UPDATE Farmacia_Medicamentos
    SET cantidad = cantidad - @Cantidad
    WHERE Id_medicamento = @IdMedicamento;
END
GO

CREATE PROCEDURE sp_agregar_servicio_ticket
    @IdTicket INT,
    @IdServicio INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Precio DECIMAL(10,2);

    SELECT @Precio = costo
    FROM Servicio
    WHERE Id_Servicio = @IdServicio;

    INSERT INTO Ticket_Servicio
    (Id_Ticket, Id_Servicio, precio)
    VALUES
    (@IdTicket, @IdServicio, @Precio);
END
GO

CREATE PROCEDURE sp_calcular_total_ticket
    @IdTicket INT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Total DECIMAL(10,2);

    SELECT @Total = ISNULL(SUM(cantidad * precio_unitario), 0)
    FROM Ticket_Medicamento
    WHERE Id_Ticket = @IdTicket;

    SELECT @Total = @Total + ISNULL(SUM(precio), 0)
    FROM Ticket_Servicio
    WHERE Id_Ticket = @IdTicket;

    UPDATE Ticket
    SET total = @Total
    WHERE Id_Ticket = @IdTicket;

    SELECT @Total AS total;
END
GO

CREATE PROCEDURE sp_pagar_ticket
    @IdTicket INT,
    @Metodo VARCHAR(50),
    @Descripcion VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Pago_Ticket
    (Id_Ticket, metodo_pago, estado_pago, descripcion)
    VALUES
    (@IdTicket, @Metodo, 'Pagado', @Descripcion);
END
GO
