from django.urls import path, re_path
from .views import login, register, refresh, permissao_list, is_authenticated
from .views import fornecedor_list, funcionario_list, cargo_list, preco_list, faixa_list, genero_list, produto_list, categoria_list, plataforma_list, venda_list, vendaitem_list
from .views import empresa_create, fornecedor_create, funcionario_create, cargo_create, preco_create, faixa_create, genero_create, produto_create, categoria_create, plataforma_create, venda_create, vendaitem_create
from .views import empresa_detail, fornecedor_detail, funcionario_detail, cargo_detail, preco_detail, faixa_detail, genero_detail, produto_detail, categoria_detail, plataforma_detail, venda_detail, vendaitem_detail
from .views import search

urlpatterns = [
    # Auth
    path('auth/login/', login),
    path('auth/register/', register),
    path('auth/refresh/', refresh),
    path('auth/is-authenticated/', is_authenticated),
    path('permissao/list/', permissao_list),
    # List
    path('fornecedor/list/', fornecedor_list),
    path('funcionario/list/', funcionario_list),
    path('cargo/list/', cargo_list),
    path('categoria/list/', categoria_list),
    path('preco/list/', preco_list),
    path('faixa/list/', faixa_list),
    path('genero/list/', genero_list),
    path('produto/list/', produto_list),
    path('plataforma/list/', plataforma_list),
    path('venda/list/', venda_list),
    path('vendaitem/list/', vendaitem_list),
     # Create
    path('empresa/create/', empresa_create),
    path('fornecedor/create/', fornecedor_create),
    path('funcionario/create/', funcionario_create),
    path('cargo/create/', cargo_create),
    path('categoria/create/', categoria_create),
    path('preco/create/', preco_create),
    path('faixa/create/', faixa_create),
    path('genero/create/', genero_create),
    path('produto/create/', produto_create),
    path('plataforma/create/', plataforma_create),
    path('venda/create/', venda_create),
    path('vendaitem/create/', vendaitem_create),
    # Detail
    path('empresa/<uuid:pk>', empresa_detail),
    path('fornecedor/<uuid:pk>', fornecedor_detail),
    path('funcionario/<uuid:pk>', funcionario_detail),
    path('cargo/<uuid:pk>', cargo_detail),
    path('categoria/<uuid:pk>', categoria_detail),
    path('preco/<uuid:pk>', preco_detail),
    path('faixa/<uuid:pk>', faixa_detail),
    path('genero/<uuid:pk>', genero_detail),
    path('produto/<uuid:pk>', produto_detail),
    path('plataforma/<uuid:pk>', plataforma_detail),
    path('venda/detail/', venda_detail),
    path('vendaitem/detail/', vendaitem_detail),
    # Pesquisa
    re_path(r'^pesquisa/$', search),
]