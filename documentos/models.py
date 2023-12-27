from django.db import models

from base.models import CustomUser

# Create your models here.

class Documento(models.Model):
    nome = models.CharField(max_length=100)
    corpo = models.TextField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assinado = models.BooleanField(default=False)

    def __str__(self):
        return self.nome 
