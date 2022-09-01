from django import views
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Funcionario
from .serializers import FuncionarioSerializer
from rest_framework.response import Response

# Views - Funcionario

@api_view
@permission_classes([IsAuthenticated])
def funcionario_list(request):
    """
    Lista os funcionarios
    """
    funcionario = Funcionario.objects.all()
    serializer = FuncionarioSerializer(funcionario, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def funcionario_create(request):
    """
    Cria um funcionário
    """
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
