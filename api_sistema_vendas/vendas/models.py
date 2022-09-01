from django.db import models
import uuid
from empresas.models import Cliente, Empresa
from produtos.models import Produto
from accounts.models import Funcionario

def contador():
    numero = Venda.objects.count()
    if not numero:
        return 1
    else:
        return numero + 1


class Venda(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente                 = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vendas')
    vendedor                = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vendas')
    valor                   = models.DecimalField(max_digits=12, decimal_places=2)
    data                    = models.DateTimeField(auto_now_add=True)
    numero                  = models.IntegerField(default=contador, unique=True, editable=False)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vendas')

    class Meta:
        ordering            = ["data"]
        verbose_name        = "venda"
        verbose_name_plural = "vendas"

    def __str__(self):
        return self.numero


class VendaItem(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produto                 = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='vendaitens')
    venda                   = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='vendaitens')
    valor_produto           = models.DecimalField(max_digits=12, decimal_places=2)
