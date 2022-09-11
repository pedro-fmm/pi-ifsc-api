from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Empresa, Fornecedor, Cargo, Administrador, Funcionario
from .serializers import EmpresaSerializer, FornecedorSerializer, CargoSerializer, AdministradorSerializer, FuncionarioSerializer
from accounts.serializers import UsuarioSerializer
from accounts.models import Usuario

# Views - Empresa

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def empresa_list(request):
    """
    Lista as empresas.
    """
    empresas = Empresa.objects.all()
    serializer = EmpresaSerializer(empresas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def empresa_create(request):
    """
    Cria uma empresa.
    """
    serializer = EmpresaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def empresa_detail(request, pk):
    """
    Retorna, atualiza ou deleta um empresa.
    """
    try:
        empresa = Empresa.objects.get(pk=pk)
    except Empresa.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmpresaSerializer(empresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        empresa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Fornecedor

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fornecedor_list(request):
    """
    Lista os fornecedores.
    """
    fornecedores = Fornecedor.objects.all()
    serializer = FornecedorSerializer(fornecedores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fornecedor_create(request):
    """
    Cria um fornecedor.
    """
    serializer = FornecedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def fornecedor_detail(request, pk):
    """
    Retorna, atualiza ou deleta um fornecedor.
    """
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FornecedorSerializer(fornecedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Cargo

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cargo_list(request):
    """
    Lista os cargos.
    """
    cargo = Cargo.objects.all()
    serializer = CargoSerializer(cargo, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cargo_create(request):
    """
    Cria um cargo.
    """
    serializer = CargoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cargo_detail(request, pk):
    """
    Retorna, atualiza ou deleta um cargo.
    """
    try:
        cargo = Cargo.objects.get(pk=pk)
    except Cargo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CargoSerializer(cargo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CargoSerializer(cargo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cargo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Administrador

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def administrador_list(request):
    """
    Lista os administradores
    """
    adm = Administrador.objects.all()
    serializer = AdministradorSerializer(adm, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def administrador_create(request):
    """
    Cria um Administrador
    """
    serializer = AdministradorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    func = Funcionario.objects.all()
    serializer = FuncionarioSerializer(func, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def funcionario_create(request):
    """
    Cria um Funcionário
    """
    request.data['empresa'] = request.user.empresa.id
    serializer = FuncionarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
