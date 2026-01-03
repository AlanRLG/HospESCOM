from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime

from web.models import BitacoraEstatus

class Command(BaseCommand):
    help = 'Actualiza citas a "No acudió" cuando ya pasó la fecha y hora'

    def handle(self, *args, **kwargs):
        ahora = timezone.now()

        estatus_pendientes = BitacoraEstatus.objects.exclude(
            estatus_cita__in=['Atendida', 'Cancelada', 'No acudió']
        )

        contador = 0

        for estatus in estatus_pendientes:
            fecha_hora_cita = datetime.combine(
                estatus.fecha_cita,
                estatus.hora_cita
            )

            # Convertir a timezone-aware
            fecha_hora_cita = timezone.make_aware(fecha_hora_cita)

            if fecha_hora_cita < ahora:
                estatus.estatus_cita = 'No acudió'
                estatus.save(update_fields=['estatus_cita'])
                contador += 1

        self.stdout.write(
            self.style.SUCCESS(f'{contador} citas marcadas como "No acudió"')
        )
