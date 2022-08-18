from django.db import models
from uuid import uuid4


class Empresa(models.Model):
    """
    Modelo das empresas com seus respectivos campos.
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    razao_social            = models.CharField(max_length=256) 
    nome_fantasia           = models.CharField(max_length=256)
    cnpj                    = models.CharField(max_length=14)
    icone                   = models.FileField(upload_to='media', blank=True)

    class Meta:
        ordering            = ["nome_fantasia"]
        verbose_name        = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.nome_fantasia


class Fornecedor(models.Model):
    """
    Modelo dos fornecedores
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    razao_social            = models.CharField(max_length=256) 
    nome_fantasia           = models.CharField(max_length=256)
    cnpj                    = models.CharField(max_length=14)
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas')

    class Meta:
        ordering            = ["nome_fantasia"]
        verbose_name        = "fornecedores"
        verbose_name_plural = "fornecedor"

    def __str__(self):
        return self.nome_fantasia


