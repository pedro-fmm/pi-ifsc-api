from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Administrador, Funcionario, Usuario
from .serializers import AdministradorSerializer, FuncionarioSerializer, UsuarioSerializer, LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


# Views - Usuário

def usuario_create(request):
    """
    Cria um usuário
    """
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return (user, True)
    return (serializer.errors, False)


# Views - Administrador

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def administrador_list(request):
    """
    Lista os administradores
    """
    usuario = Usuario.objects.all()
    serializer = UsuarioSerializer(usuario, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def administrador_create(request):
    """
    Cria um Administrador
    """
    resp = usuario_create(request)
    if resp[1]:
        user = resp[0]
        adm = Administrador.objects.create(usuario=user)
        serializer = AdministradorSerializer(data=adm)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(resp[0], status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def administrador_detail(request, pk):
    """
    Retorna, atualiza ou deleta um funcionário.
    """
    try:
        administrador = Administrador.objects.get(pk=pk)
    except Administrador.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AdministradorSerializer(administrador)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AdministradorSerializer(administrador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        administrador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Funcionário

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def funcionario_list(request):
    """
    Lista os funcionarios
    """
    usuario = Usuario.objects.all()
    serializer = UsuarioSerializer(usuario, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def funcionario_create(request):
    """
    Cria um Funcionário
    """
    resp = usuario_create(request)
    if resp[1]:
        user = resp[0]
        func = Funcionario.objects.create(usuario=user, empresa=request.user.empresa.id, cargo=request['cargo'])
        serializer = FuncionarioSerializer(data=func)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(resp[0], status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def funcionario_detail(request, pk):
    """
    Retorna, atualiza ou deleta um funcionário.
    """
    try:
        funcionario = Funcionario.objects.get(pk=pk)
    except Funcionario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FuncionarioSerializer(funcionario)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FuncionarioSerializer(funcionario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        funcionario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Token

@api_view(['POST'])
def refresh(request):
        serializer = TokenRefreshSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "usuario": serializer.data,
            "refresh": res["refresh"],
            "token": res["access"]
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
        serializer = LoginSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

