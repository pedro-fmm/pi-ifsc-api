from django.urls import path
from .views import login, register, refresh

urlpatterns = [
    path('auth/login/', login),
    path('auth/register/', register),
    path('auth/refresh/', refresh),
]
