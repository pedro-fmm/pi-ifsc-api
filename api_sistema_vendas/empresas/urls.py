from django.urls import path
from .views import empresa_list, fornecedor_list
from .views import empresa_create, fornecedor_create
from .views import empresa_detail, fornecedor_detail

urlpatterns = [
    # List
    path('empresa/list/', empresa_list),
    path('fornecedor/list/', fornecedor_list),
    # Create
    path('empresa/create/', empresa_create),
    path('fornecedor/create/', fornecedor_create),
    # Detail
    path('empresa/<uuid:pk>', empresa_detail),
    path('fornecedor/<uuid:pk>', fornecedor_detail),
]