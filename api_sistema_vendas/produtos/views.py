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


# Views - Categoria

@api_view(['GET'])
def categoria_list(request):
    """
    Lista as categorias
    """
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Faixa Etária

@api_view(['GET'])
def faixa_list(request):
    """
    Lista as faixas etárias
    """
    faixas = FaixaEtaria.objects.all()
    serializer = FaixaEtariaSerializer(faixas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Gênero

@api_view(['GET'])
def genero_list(request):
    """
    Lista os gêneros
    """
    generos = Genero.objects.all()
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Plataforma

@api_view(['GET'])
def plataforma_list(request):
    """
    Lista as plataformas
    """
    plataformas = Plataforma.objects.all()
    serializer = PlataformaSerializer(plataformas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Preço

@api_view(['GET'])
def preco_list(request):
    """
    Lista os preços
    """
    precos = Preco.objects.all()
    serializer = PrecoSerializer(precos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)