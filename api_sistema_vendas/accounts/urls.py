from django.urls import path
from .views import funcionario_list, funcionario_create, funcionario_detail
from .views import login, register, refresh

urlpatterns = [
    path('funcionario/list/', funcionario_list),
    path('funcionario/create/', funcionario_create),
    path('funcionario/<uuid:pk>', funcionario_detail),
    path('auth/login', login),
    path('auth/register', register),
    path('auth/refresh', refresh),
]
