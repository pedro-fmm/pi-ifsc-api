from django.urls import path
from .views import preco_list, faixa_list, genero_list, produto_list, categoria_list, plataforma_list

urlpatterns = [
    path('categoria/', categoria_list)
]