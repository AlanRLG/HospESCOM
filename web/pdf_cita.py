from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO

def generar_comprobante_cita(cita, bitacora, linea_pago):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, 750, "COMPROBANTE DE CITA - HospESCOM")

    p.setFont("Helvetica", 12)
    p.drawString(50, 720, f"Folio de cita: {cita.Id_cita}")
    p.drawString(50, 700, f"Paciente: {cita.Id_paciente.Id_usuario.nombre} {cita.Id_paciente.Id_usuario.apellido_P}")
    p.drawString(50, 680, f"Doctor: {cita.Id_doctor.Id_usuario.Id_usuario.nombre} {cita.Id_doctor.Id_usuario.Id_usuario.apellido_P}")
    p.drawString(50, 660, f"Especialidad: {cita.Id_doctor.Id_especialidad.tipo_Especialidad}")
    p.drawString(50, 640, f"Consultorio: {cita.Id_doctor.Id_consultorio.Id_consultorio}")

    p.drawString(50, 610, f"Fecha de cita: {bitacora.fecha_cita}")
    p.drawString(50, 590, f"Hora de cita: {bitacora.hora_cita}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 560, f"LÍNEA DE PAGO:")
    p.setFont("Helvetica", 12)
    p.drawString(50, 540, linea_pago)

    p.drawString(50, 500, f"Fecha límite de pago: {cita.fecha_limite.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(50, 480, "Tiempo para pagar: 8 horas después de generar la cita")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 450, "Política de cancelación:")
    p.setFont("Helvetica", 11)
    p.drawString(50, 430, "48 hrs antes → 100% devolución")
    p.drawString(50, 415, "24 hrs antes → 50% devolución")
    p.drawString(50, 400, "Menos de 24 hrs → 0% devolución")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
