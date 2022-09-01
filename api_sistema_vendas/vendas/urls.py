from django.urls import path
from .views import venda_create, venda_detail, venda_list
from .views import vendaitem_create, vendaitem_detail, vendaitem_list

urlpatterns = [
    # List
    path('venda/list/', venda_list),
    path('vendaitem/list/', vendaitem_list),
    # Detail
    path('venda/detail/', venda_detail),
    path('vendaitem/detail/', vendaitem_detail),
    # Create
    path('venda/create/', venda_create),
    path('vendaitem/create/', vendaitem_create),
]
