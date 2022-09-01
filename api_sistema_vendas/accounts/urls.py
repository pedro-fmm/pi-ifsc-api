from django.urls import include, path
from .views import funcionario_list, funcionario_create, funcionario_detail
from .viewsets import LoginViewSet, RegistrationViewSet, RefreshViewSet
from rest_framework.routers import SimpleRouter

routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/register', RegistrationViewSet, basename='auth-register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

urlpatterns = [

    path('funcionario/list/', funcionario_list),
    path('funcionario/create/', funcionario_create),
    path('funcionario/<uuid:pk>', funcionario_detail),
    path('', include(('accounts.routers', 'accounts'))),

]
