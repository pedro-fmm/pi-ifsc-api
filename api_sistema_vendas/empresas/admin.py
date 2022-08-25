from curses.ascii import EM
from django.contrib import admin
from .models import Empresa, Fornecedor, Cliente, Cargo

admin.site.register(Empresa)
admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Cargo)