from .models import Usuario, Empresa, Fornecedor, Funcionario, Cargo, Categoria, Genero, FaixaEtaria, Plataforma, Preco, Produto, Venda, VendaItem
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login, Permission
from django.core.exceptions import ObjectDoesNotExist

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'primeiro_nome', 'ultimo_nome', 'email', 'is_admin', 'is_staff', 'is_active', 'date_joined')
        read_only_field = ['id', 'is_active', 'date_joined']


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['user'] = UsuarioSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UsuarioSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)

    class Meta:
        model = Usuario
        fields = ('email', 'password', 'username', 'primeiro_nome', 'ultimo_nome')

    def create(self, validated_data):
        try:
            usuario = Usuario.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            usuario = Usuario.objects.create_user(**validated_data)
        return usuario


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = '__all__'


class FuncionarioSerializer(UsuarioSerializer):

    class Meta:
        model = Funcionario
        fields = '__all__'


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


class PlataformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plataforma
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

    
class FaixaEtariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaixaEtaria
        fields = '__all__'


class PrecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preco
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'


class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'


class VendaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendaItem
        fields = '__all__'