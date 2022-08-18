from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Empresa, Fornecedor
from .serializers import EmpresaSerializer, FornecedorSerializer

# Views - Empresa

@api_view(['GET'])
def empresa_list(request):
    """
    Lista as empresas.
    """
    produtos = Empresa.objects.all()
    serializer = EmpresaSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
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
def fornecedor_list(request):
    """
    Lista os fornecedores.
    """
    categorias = Fornecedor.objects.all()
    serializer = FornecedorSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
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

