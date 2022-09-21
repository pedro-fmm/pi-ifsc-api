from django.contrib import admin
from .models import Empresa, Fornecedor, Cliente, Funcionario, Cargo, Usuario, Plataforma, FaixaEtaria, Genero, Categoria, Preco, Produto, Venda, VendaItem

admin.site.register(Usuario)
admin.site.register(Funcionario)
admin.site.register(Empresa)
admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Cargo)
admin.site.register(Plataforma)
admin.site.register(FaixaEtaria)
admin.site.register(Genero)
admin.site.register(Categoria)
admin.site.register(Preco)
admin.site.register(Produto)
admin.site.register(Venda)
admin.site.register(VendaItem)