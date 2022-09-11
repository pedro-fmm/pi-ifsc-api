from .models import Usuario
from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'primeiro_nome', 'ultimo_nome', 'email', 'is_admin', 'is_staff', 'is_active', 'date_joined')
        read_only_field = ['is_active', 'date_joined']


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
        fields = '__all__'

    def create(self, validated_data):
        try:
            usuario = Usuario.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            usuario = Usuario.objects.create_user(**validated_data)
        return usuario

