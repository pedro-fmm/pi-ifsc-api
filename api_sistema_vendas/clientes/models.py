import uuid
from django.db import models

# Create your models here.

class Cliente(models.Model):
    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome      = models.CharField(max_length=256)
    cpf       = models.CharField(max_length=11)
    rg        = models.CharField(max_length=7)
    email     = models.CharField(max_length=256)
    telefone  = models.CharField(max_length=11)
    endereco  = models.CharField(max_length=256)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nome

    
