from django.urls import path
from .views import preco_list, faixa_list, genero_list, produto_list, categoria_list, plataforma_list
from .views import preco_create, faixa_create, genero_create, produto_create, categoria_create, plataforma_create
from .views import preco_detail, faixa_detail, genero_detail, produto_detail, categoria_detail, plataforma_detail

urlpatterns = [
    # List
    path('categoria/list/', categoria_list),
    path('preco/list/', preco_list),
    path('faixa/list/', faixa_list),
    path('genero/list/', genero_list),
    path('produto/list/', produto_list),
    path('plataforma/list/', plataforma_list),
    # Create
    path('categoria/create/', categoria_create),
    path('preco/create/', preco_create),
    path('faixa/create/', faixa_create),
    path('genero/create/', genero_create),
    path('produto/create/', produto_create),
    path('plataforma/create/', plataforma_create),
    # Detail
    path('categoria/<uuid:pk>', categoria_detail),
    path('preco/<uuid:pk>', preco_detail),
    path('faixa/<uuid:pk>', faixa_detail),
    path('genero/<uuid:pk>', genero_detail),
    path('produto/<uuid:pk>', produto_detail),
    path('plataforma/<uuid:pk>', plataforma_detail),
]