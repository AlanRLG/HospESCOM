from django.db import models

class TipoUsuario(models.Model):
    Id_tipoUsuario = models.AutoField(primary_key=True)
    NombreUsuario = models.CharField(max_length=100)

    class Meta:
        managed = False  # Django no intentará crear esta tabla
        db_table = 'TipoUsuario'


class Usuario(models.Model):
    Id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_P = models.CharField(max_length=100)
    apellido_M = models.CharField(max_length=100, null=True, blank=True)
    curp = models.CharField(max_length=18, unique=True)
    correo = models.CharField(max_length=150, unique=True)
    contraseña = models.CharField(max_length=255)
    Id_tipoUsuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE, db_column='Id_tipoUsuario')

    class Meta:
        managed = False  # Django no hará migraciones
        db_table = 'Usuario'
