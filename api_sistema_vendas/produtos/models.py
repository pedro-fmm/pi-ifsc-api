from django.db import models


class Plataforma(models.Model):
    """
    Modelo das plataformas com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)

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
    id                      = models.UUIDField(primary_key=True)
    faixa                   = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "faixa etária"
        verbose_name_plural = "faixas etárias"

    def __str__(self):
        return self.faixa

 
class Produto(models.Model):
    """
    Modelo dos produtos com seus respectivos campos.

    Tags tornam a pesquisa mais fácil.
    """
    id                      = models.UUIDField(primary_key=True)
    nome                    = models.CharField(max_length=256)
    descricao               = models.TextField()
    preco                   = models.DecimalField(max_digits=12, decimal_places=2)
    imagem                  = models.FileField(upload_to='media')
    categoria               = models.ForeignKey(Categorias, on_delete=models.CASCADE, related_name='produtos')
    tags                    = models.ManyToManyField(Tag, related_name='produtos')
    data_criacao            = models.DateField(auto_now_add=True)
    visualizacoes           = models.IntegerField()
    vendas                  = models.IntegerField()
    is_disponivel           = models.BooleanField(default=True)
    estoque                 = models.IntegerField(default=0) 

    def __str__(self):
        return self.nome