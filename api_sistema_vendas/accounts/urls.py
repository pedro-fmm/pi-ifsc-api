from django.urls import path
from .views import funcionario_list, funcionario_create, funcionario_detail, administrador_list, administrador_create, administrador_detail
from .views import login, register, refresh

urlpatterns = [
    path('funcionario/list/', funcionario_list),
    path('funcionario/create/', funcionario_create),
    path('funcionario/<uuid:pk>', funcionario_detail),
    path('administrador/list/', administrador_list),
    path('administrador/create/', administrador_create),
    path('administrador/<uuid:pk>', administrador_detail),
    path('auth/login/', login),
    path('auth/register/', register),
    path('auth/refresh/', refresh),
]
