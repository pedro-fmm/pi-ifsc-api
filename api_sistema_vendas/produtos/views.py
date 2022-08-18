from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Produto, FaixaEtaria, Categoria, Genero, Plataforma, Preco
from .serializers import CategoriaSerializer, FaixaEtariaSerializer, GeneroSerializer, PlataformaSerializer, PrecoSerializer, ProdutoSerializer

# Views - Produto

@api_view(['GET'])
def produto_list(request):
    """
    Lista os produtos
    """
    produtos = Produto.objects.all()
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def produto_create(request):
    """
    Cria um produto
    """
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views - Categoria

@api_view(['GET'])
def categoria_list(request):
    """
    Lista as categorias
    """
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def categoria_create(request):
    """
    Cria uma categoria
    """
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views - Faixa Etária

@api_view(['GET'])
def faixa_list(request):
    """
    Lista as faixas etárias
    """
    faixas = FaixaEtaria.objects.all()
    serializer = FaixaEtariaSerializer(faixas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def faixa_create(request):
    """
    Cria uma faixa etária
    """
    serializer = FaixaEtariaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views - Gênero

@api_view(['GET'])
def genero_list(request):
    """
    Lista os gêneros
    """
    generos = Genero.objects.all()
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def genero_create(request):
    """
    Cria um gênero
    """
    serializer = GeneroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views - Plataforma

@api_view(['GET'])
def plataforma_list(request):
    """
    Lista as plataformas
    """
    plataformas = Plataforma.objects.all()
    serializer = PlataformaSerializer(plataformas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def plataforma_create(request):
    """
    Cria um plataforma
    """
    serializer = PlataformaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Views - Preço

@api_view(['GET'])
def preco_list(request):
    """
    Lista os preços
    """
    precos = Preco.objects.all()
    serializer = PrecoSerializer(precos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def preco_create(request):
    """
    Cria um preço
    """
    serializer = PrecoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)