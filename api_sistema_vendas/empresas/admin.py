from django.contrib import admin
from .models import Empresa, Fornecedor, Cliente, Cargo, Funcionario, Administrador

admin.site.register(Funcionario)
admin.site.register(Administrador)
admin.site.register(Empresa)
admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Cargo)