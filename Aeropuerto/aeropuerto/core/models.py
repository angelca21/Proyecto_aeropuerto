from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, default='example@example.com')
    patente = models.CharField(max_length=50)
    nombre_chofer = models.CharField(max_length=100)
    telefono_chofer = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Pasajero(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    chofer = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)

