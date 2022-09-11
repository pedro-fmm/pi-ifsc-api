from rest_framework import serializers
from .models import Empresa, Fornecedor, Cargo, Administrador, Funcionario
from accounts.serializers import UsuarioSerializer

class FuncionarioSerializer(UsuarioSerializer):

    class Meta:
        model = Funcionario
        fields = UsuarioSerializer.Meta.fields + ('usuario', 'empresa', 'cargo',)


class AdministradorSerializer(UsuarioSerializer):

    class Meta:
        model = Administrador
        fields = UsuarioSerializer.Meta.fields + ('usuario',)


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

