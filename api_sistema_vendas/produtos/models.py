from django.db import models
import uuid
from empresas.models import Empresa

class Plataforma(models.Model):
    """
    Modelo das plataformas com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='plataformas')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "plataformas"
        verbose_name_plural = "plataformas"

    def __str__(self):
        return self.nome

       
class FaixaEtaria(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    faixa                   = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='faixas')

    class Meta:
        ordering            = ["faixa"]
        verbose_name        = "faixa etária"
        verbose_name_plural = "faixas etárias"

    def __str__(self):
        return self.faixa


class Genero(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='generos')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "gênero"
        verbose_name_plural = "gêneros"

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome


class Preco(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_alteracao          = models.DateTimeField(auto_now_add=True)
    preco_custo             = models.DecimalField(max_digits=8, decimal_places=2)
    preco_venda             = models.DecimalField(max_digits=8, decimal_places=2)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='precos')

    class Meta:
        ordering            = ["data_alteracao"]
        verbose_name        = "preço"
        verbose_name_plural = "preços"

    def __str__(self):
        return self.preco_venda

 
class Produto(models.Model):
    """
    Modelo dos produtos com seus respectivos campos.

    Tags tornam a pesquisa mais fácil.
    """
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.TextField()
    imagem                  = models.FileField(upload_to='media', blank=True)
    plataforma              = models.ForeignKey('Plataforma', on_delete=models.CASCADE, related_name='produtos')
    faixa_etaria            = models.ForeignKey('FaixaEtaria', on_delete=models.CASCADE, related_name='produtos')
    genero                  = models.ForeignKey('Genero', on_delete=models.CASCADE, related_name='produtos')
    categoria               = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='produtos')
    data_criacao            = models.DateField(auto_now_add=True)
    estoque                 = models.IntegerField(default=0)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome

    @property
    def is_disponivel(self):
        """
        Retorna a diponibilidade do produto.
        True    - estoque > 0
        False   - estoque <= 0 
        """
        if(self.estoque > 0):
            return True
        else:
            return False