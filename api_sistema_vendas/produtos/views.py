from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Produto, FaixaEtaria, Categoria, Genero, Plataforma, Preco
from .serializers import CategoriaSerializer, FaixaEtariaSerializer, GeneroSerializer, PlataformaSerializer, PrecoSerializer, ProdutoSerializer

# Views - Produto

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def produto_list(request):
    """
    Lista os produtos.
    """
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def produto_create(request):
    """
    Cria um produto.
    """
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def produto_detail(request, pk):
    """
    Retorna, atualiza ou deleta um produto.
    """
    try:
        produto = Produto.objects.get(pk=pk)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Categoria

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def categoria_list(request):
    """
    Lista as categorias.
    """
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def categoria_create(request):
    """
    Cria uma categoria.
    """
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def categoria_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma categoria.
    """
    try:
        categoria = Categoria.objects.get(pk=pk)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Faixa Etária

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def faixa_list(request):
    """
    Lista as faixas etárias.
    """
    faixas = FaixaEtaria.objects.all()
    serializer = FaixaEtariaSerializer(faixas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def faixa_create(request):
    """
    Cria uma faixa etária.
    """
    serializer = FaixaEtariaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def faixa_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma faixa etária.
    """
    try:
        faixa = FaixaEtaria.objects.get(pk=pk)
    except FaixaEtaria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FaixaEtariaSerializer(faixa)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FaixaEtariaSerializer(faixa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        faixa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Gênero

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genero_list(request):
    """
    Lista os gêneros.
    """
    generos = Genero.objects.all()
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def genero_create(request):
    """
    Cria um gênero.
    """
    serializer = GeneroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def genero_detail(request, pk):
    """
    Retorna, atualiza ou deleta um gênero.
    """
    try:
        genero = Genero.objects.get(pk=pk)
    except Genero.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GeneroSerializer(genero)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Plataforma

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plataforma_list(request):
    """
    Lista as plataformas.
    """
    plataformas = Plataforma.objects.all()
    serializer = PlataformaSerializer(plataformas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def plataforma_create(request):
    """
    Cria um plataforma.
    """
    serializer = PlataformaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def plataforma_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma plataforma.
    """
    try:
        plataforma = Plataforma.objects.get(pk=pk)
    except Plataforma.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlataformaSerializer(plataforma)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlataformaSerializer(plataforma, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plataforma.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Preço

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preco_list(request):
    """
    Lista os preços.
    """
    precos = Preco.objects.all()
    serializer = PrecoSerializer(precos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def preco_create(request):
    """
    Cria um preço.
    """
    serializer = PrecoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def preco_detail(request, pk):
    """
    Retorna, atualiza ou deleta um preço.
    """
    try:
        preco = Preco.objects.get(pk=pk)
    except Preco.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PrecoSerializer(preco)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PrecoSerializer(preco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        preco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def search(request):
    search_value = request.GET.get('search')
    produtos = Produto.objects.filter(nome__iregex=rf'((?i)\b{search_value}\b)', descricao__iregex=rf'((?i)\b{search_value}\b)')
    serializer = ProdutoSerializer(produtos, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)