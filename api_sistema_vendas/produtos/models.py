from django.db import models


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