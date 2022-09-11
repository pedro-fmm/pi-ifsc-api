from django.urls import path
from .views import empresa_list, fornecedor_list, cargo_list, funcionario_list, administrador_list
from .views import empresa_create, fornecedor_create, cargo_create, funcionario_create, administrador_create
from .views import empresa_detail, fornecedor_detail, cargo_detail, funcionario_detail, administrador_detail

urlpatterns = [
    # List
    path('empresa/list/', empresa_list),
    path('fornecedor/list/', fornecedor_list),
    path('cargo/list/', cargo_list),
    path('funcionario/list/', funcionario_list),
    path('administrador/list/', administrador_list),
    # Create
    path('empresa/create/', empresa_create),
    path('fornecedor/create/', fornecedor_create),
    path('cargo/create/', cargo_create),
    path('funcionario/create/', funcionario_create),
    path('administrador/create/', administrador_create),
    # Detail
    path('empresa/<uuid:pk>', empresa_detail),
    path('fornecedor/<uuid:pk>', fornecedor_detail),
    path('cargo/<uuid:pk>', cargo_detail),
    path('funcionario/<uuid:pk>', funcionario_detail),
    path('administrador/<uuid:pk>', administrador_detail),
]