from .models import Funcionario
from rest_framework import serializers


class FuncionarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Funcionario
        fields = ['id', 'username', 'primeiro_nome', 'ultimo_nome', 'email', 'is_admin', 'is_staff', 'date_joined']
        read_only_field = ['is_active', 'date_joined']
