from django.urls import path
from .views import preco_list, faixa_list, genero_list, produto_list, categoria_list, plataforma_list
from .views import preco_create, faixa_create, genero_create, produto_create, categoria_create, plataforma_create
from .views import preco_detail, faixa_detail, genero_detail, produto_detail, categoria_detail, plataforma_detail

urlpatterns = [
    # List
    path('list/categoria/', categoria_list),
    path('list/preco/', preco_list),
    path('list/faixa/', faixa_list),
    path('list/genero/', genero_list),
    path('list/produto/', produto_list),
    path('list/plataforma/', plataforma_list),
    # Create
    path('create/categoria/', categoria_create),
    path('create/preco/', preco_create),
    path('create/faixa/', faixa_create),
    path('create/genero/', genero_create),
    path('create/produto/', produto_create),
    path('create/plataforma/', plataforma_create),
    # Detail
    path('categoria/<uuid:pk>', categoria_detail),
    path('preco/<uuid:pk>', preco_detail),
    path('faixa/<uuid:pk>', faixa_detail),
    path('genero/<uuid:pk>', genero_detail),
    path('produto/<uuid:pk>', produto_detail),
    path('plataforma/<uuid:pk>', plataforma_detail),
]