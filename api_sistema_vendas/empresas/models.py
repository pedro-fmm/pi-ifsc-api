from pyexpat import model
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
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas_fornecedor', null=True)

    class Meta:
        ordering            = ["nome_fantasia"]
        verbose_name        = "fornecedores"
        verbose_name_plural = "fornecedor"

    def __str__(self):
        return self.nome_fantasia


class Cargo(models.Model):
    """
    Modelo dos cargos
    """
    CHOICES = [
        ("Pode", True), 
        ("Não pode", False)
    ]
    
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas_cargo', null=True)
    is_admin                = models.BooleanField(choices=CHOICES, default=False)
    manage_produtos         = models.BooleanField(choices=CHOICES, default=False)
    manage_clientes         = models.BooleanField(choices=CHOICES, default=False)
    manage_fornecedores     = models.BooleanField(choices=CHOICES, default=False)
    manage_product          = models.BooleanField(choices=CHOICES, default=False)
    manage_cargos           = models.BooleanField(choices=CHOICES, default=False)
    manage_funcionarios     = models.BooleanField(choices=CHOICES, default=False)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "cargo"
        verbose_name_plural = "cargos"

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    """
    Modelo dos clientes
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    cpf                     = models.CharField(max_length=11)
    rg                      = models.CharField(max_length=7, blank=True)
    email                   = models.CharField(max_length=256)
    telefone                = models.CharField(max_length=11)
    endereco                = models.CharField(max_length=256)
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas_cliente')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nome

