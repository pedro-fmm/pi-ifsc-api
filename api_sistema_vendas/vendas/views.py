from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Venda, VendaItem
from .serializers import VendaSerializer, VendaItemSerializer


# Views - Venda

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def venda_list(request):
    """
    Lista as vendas.
    """
    vendas = Venda.objects.all()
    serializer = VendaSerializer(vendas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def venda_create(request):
    """
    Cria uma venda.
    """
    serializer = VendaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def venda_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma venda.
    """
    try:
        venda = Venda.objects.get(pk=pk)
    except Venda.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendaSerializer(venda)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendaSerializer(venda, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - VendaItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendaitem_list(request):
    """
    Lista os itens de uma venda.
    """
    vendaitens = VendaItem.objects.all()
    serializer = VendaItemSerializer(vendaitens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vendaitem_create(request):
    """
    Cria um item de uma venda.
    """
    serializer = VendaItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def vendaitem_detail(request, pk):
    """
    Retorna, atualiza ou deleta um item de uma venda.
    """
    try:
        vendaitem = VendaItem.objects.get(pk=pk)
    except VendaItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendaItemSerializer(vendaitem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = VendaItemSerializer(vendaitem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        vendaitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

