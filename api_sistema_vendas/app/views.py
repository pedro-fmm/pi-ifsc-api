from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Permission, AnonymousUser
from django.contrib.auth.decorators import permission_required
from .serializers import LoginSerializer, RegisterSerializer, PermissionSerializer, EmpresaSerializer, FornecedorSerializer, FuncionarioSerializer, CategoriaSerializer, FaixaEtariaSerializer, GeneroSerializer, PlataformaSerializer, PrecoSerializer, ProdutoSerializer, VendaSerializer, VendaItemSerializer, ClienteSerializer, CompraEstoqueSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Empresa, Fornecedor, Funcionario, Produto, FaixaEtaria, Categoria, Genero, Plataforma, Preco, Usuario, Venda, VendaItem, Cliente, CompraEstoque
import logging

logger = logging.getLogger(__name__)

def get_user_empresa(request):
    if isinstance(request.user, AnonymousUser):
        return None
    try:
        empresa = request.user.funcionario.empresa.id
    except:
        empresa = request.user.empresa.id
    return empresa


def return_date():
    from datetime import datetime
    from calendar import monthrange

    ano = datetime.now().year
    mes = datetime.now().month
    primeiro_dia = "01"
    ultimo_dia = str(monthrange(ano, mes)[1])
    ano = str(ano)
    mes = str(mes)
    if len(mes) == 1:
        mes = "0" + mes
    data_comeco = ano + "-" + mes + "-" + primeiro_dia + " 00:00-03:00"
    data_fim = ano + "-" + mes + "-" + ultimo_dia + " 23:59-03:00"

    return (data_comeco, data_fim)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    """
    Testa autenticação
    """
    response = {"status": "token valido"}
    return Response(response, status=status.HTTP_200_OK)


# Views - Permissão

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def permissao_list(request):
    """
    Lista os funcionarios
    """
    perm = Permission.objects.all()
    serializer = PermissionSerializer(perm, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Empresa

@api_view(['POST'])
def empresa_create(request):
    """
    Cria uma empresa.
    """
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['icone'] = request.FILES["icone"]
    request.POST._mutable = _mutable
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        request_copy = request.data.copy()
        request_copy['administrador'] = user.pk
        empresa_serializer = EmpresaSerializer(data=request_copy)
        if empresa_serializer.is_valid():   
            empresa_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(empresa_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_empresa', 'change_empresa', 'delete_empresa'])
def empresa_detail(request, pk):
    """
    Retorna, atualiza ou deleta um empresa.
    """
    try:
        empresa = Empresa.objects.get(pk=pk, administrador__id=request.user.id)
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
@permission_required(['view_fornecedor'])
def fornecedor_list(request):
    """
    Lista os fornecedores.
    """
    empresa = get_user_empresa(request)
    fornecedores = Fornecedor.objects.filter(empresa__id=empresa)
    serializer = FornecedorSerializer(fornecedores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_fornecedor'])
def fornecedor_create(request):
    """
    Cria um fornecedor.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = FornecedorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_fornecedor', 'change_fornecedor', 'delete_fornecedor'])
def fornecedor_detail(request, pk):
    """
    Retorna, atualiza ou deleta um fornecedor.
    """
    try:
        empresa = get_user_empresa(request)
        fornecedor = Fornecedor.objects.get(pk=pk, empresa__id=empresa)
    except Fornecedor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FornecedorSerializer(fornecedor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = FornecedorSerializer(fornecedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Funcionário

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_funcionario'])
def funcionario_list(request):
    """
    Lista os funcionarios
    """
    empresa = get_user_empresa(request)
    func = Funcionario.objects.filter(empresa__id=empresa)
    serializer = FuncionarioSerializer(func, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_funcionario'])
def funcionario_create(request):
    """
    Cria um Funcionário
    """
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid():
        empresa = get_user_empresa(request)
        user = user_serializer.save()
        request_copy = request.data.copy()
        request_copy['empresa'] = empresa
        request_copy['usuario'] = user.pk
        func_serializer = FuncionarioSerializer(data=request_copy)
        if func_serializer.is_valid():
            func_serializer.save()    
            return Response(func_serializer.data, status=status.HTTP_201_CREATED)
        return Response(func_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_funcionario', 'change_funcionario', 'delete_funcionario'])
def funcionario_detail(request, pk):
    """
    Retorna, atualiza ou deleta um funcionário.
    """
    try:
        empresa = get_user_empresa(request)
        funcionario = Funcionario.objects.get(pk=pk, empresa__id=empresa)
    except Funcionario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FuncionarioSerializer(funcionario)
        return Response(serializer.data)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = FuncionarioSerializer(funcionario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        funcionario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_funcionario'])
def funcionario_logged(request):
    """
    Retorna, atualiza ou deleta um funcionário.
    """
    try:
        empresa = get_user_empresa(request)
        funcionario = Funcionario.objects.get(usuario=request.user.id, empresa__id=empresa)
    except Funcionario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FuncionarioSerializer(funcionario)
    return Response(serializer.data)

# Views - Produto

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_produto'])
def produto_list(request):
    """
    Lista os produtos.
    """
    empresa = get_user_empresa(request)
    produtos = Produto.objects.filter(empresa__id=empresa)
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_produto'])
def produto_create(request):
    """
    Cria um produto.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.data['imagem'] = request.FILES['imagem']
    request.POST._mutable = _mutable
    serializer = ProdutoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_produto', 'change_produto', 'delete_produto'])
def produto_detail(request, pk):
    """
    Retorna, atualiza ou deleta um produto.
    """
    try:
        empresa = get_user_empresa(request) 
        produto = Produto.objects.get(pk=pk, empresa__id=empresa)
    except Produto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProdutoSerializer(produto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Categoria

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_categoria'])
def categoria_list(request):
    """
    Lista as categorias.
    """
    empresa = get_user_empresa(request)
    categorias = Categoria.objects.filter(empresa__id=empresa)
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_categoria'])
def categoria_create(request):
    """
    Cria uma categoria.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = CategoriaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_categoria', 'change_categoria', 'delete_categoria'])
def categoria_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma categoria.
    """
    try:
        empresa = get_user_empresa(request)
        categoria = Categoria.objects.get(pk=pk, empresa__id=empresa)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Faixa Etária

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_faixaetaria'])
def faixa_list(request):
    """
    Lista as faixas etárias.
    """
    empresa = get_user_empresa(request)
    faixas = FaixaEtaria.objects.filter(empresa__id=empresa)
    serializer = FaixaEtariaSerializer(faixas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_faixaetaria'])
def faixa_create(request):
    """
    Cria uma faixa etária.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = FaixaEtariaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_faixaetaria', 'change_faixaetaria', 'delete_faixaetaria'])
def faixa_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma faixa etária.
    """
    try:
        empresa = get_user_empresa(request)
        faixa = FaixaEtaria.objects.get(pk=pk, empresa__id=empresa)
    except FaixaEtaria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FaixaEtariaSerializer(faixa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = FaixaEtariaSerializer(faixa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        faixa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Gênero

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_genero'])
def genero_list(request):
    """
    Lista os gêneros.
    """
    empresa = get_user_empresa(request)
    generos = Genero.objects.filter(empresa__id=empresa)
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_genero'])
def genero_create(request):
    """
    Cria um gênero.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = GeneroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_genero', 'change_genero', 'delete_categoria'])
def genero_detail(request, pk):
    """
    Retorna, atualiza ou deleta um gênero.
    """
    try:
        empresa = get_user_empresa(request)
        genero = Genero.objects.get(pk=pk, empresa__id=empresa)
    except Genero.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GeneroSerializer(genero)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Plataforma

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_plataforma'])
def plataforma_list(request):
    """
    Lista as plataformas.
    """
    empresa = get_user_empresa(request)
    plataformas = Plataforma.objects.filter(empresa__id=empresa)
    serializer = PlataformaSerializer(plataformas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_plataforma'])
def plataforma_create(request):
    """
    Cria um plataforma.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = PlataformaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_plataforma', 'change_plataforma', 'delete_plataforma'])
def plataforma_detail(request, pk):
    """
    Retorna, atualiza ou deleta uma plataforma.
    """
    try:
        empresa = get_user_empresa(request)
        plataforma = Plataforma.objects.get(pk=pk, empresa__id=empresa)
    except Plataforma.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlataformaSerializer(plataforma)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = PlataformaSerializer(plataforma, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plataforma.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Preço

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_preco'])
def preco_list(request, pk):
    """
    Lista os preços.
    """
    empresa = get_user_empresa(request)
    precos = Preco.objects.filter(empresa__id=empresa, produto=pk)
    serializer = PrecoSerializer(precos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_preco'])
def preco_create(request, produto_pk):
    """
    Cria um preço.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.data['produto'] = produto_pk
    request.POST._mutable = _mutable
    serializer = PrecoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_preco', 'change_preco', 'delete_preco'])
def preco_detail(request, pk):
    """
    Retorna, atualiza ou deleta um preço.
    """
    try:
        empresa = get_user_empresa(request)
        preco = Preco.objects.get(pk=pk, empresa__id=empresa)
    except Preco.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PrecoSerializer(preco)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = PrecoSerializer(preco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        preco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Venda

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_venda'])
def venda_list(request):
    """
    Lista as vendas.
    """
    empresa = get_user_empresa(request)
    vendas = Venda.objects.filter(empresa__id=empresa)
    serializer = VendaSerializer(vendas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_venda'])
def venda_create(request):
    """
    Cria uma venda.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = VendaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_venda', 'delete_venda'])
def venda_detail(request, pk):
    """
    Retorna ou deleta uma venda.
    """
    try:
        empresa = get_user_empresa(request)
        venda = Venda.objects.get(pk=pk, empresa__id=empresa)
    except Venda.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendaSerializer(venda)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        venda.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - VendaItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_vendaitem'])
def vendaitem_list(request):
    """
    Lista os itens de uma venda.
    """
    empresa = get_user_empresa(request)
    vendaitens = VendaItem.objects.filter(venda__empresa__id=empresa)
    serializer = VendaItemSerializer(vendaitens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_vendaitem'])
def vendaitem_create(request):
    """
    Cria um item de uma venda.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    produto = Produto.objects.get(pk=request.data['produto'])
    try:
        request.data['valor_produto'] = produto.precos.order_by('-data_alteracao')[0].id
    except:
        logger.warn('Produto sem preços definido')
    request.data['empresa'] = empresa 
    request.POST._mutable = _mutable
    serializer = VendaItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        venda = Venda.objects.get(pk=request.data['venda'])
        venda.valor += produto.precos.order_by('-data_alteracao')[0].preco_venda
        venda.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_vendaitem', 'delete_vendaitem'])
def vendaitem_detail(request, pk):
    """
    Retorna ou deleta um item de uma venda.
    """
    try:
        empresa = get_user_empresa(request)
        vendaitem = VendaItem.objects.get(pk=pk, empresa__id=empresa)
    except VendaItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendaItemSerializer(vendaitem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        vendaitem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - VendaItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_cliente'])
def cliente_list(request):
    """
    Lista os itens de um cliente.
    """
    empresa = get_user_empresa(request)
    clientes = Cliente.objects.filter(empresa__id=empresa)
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_cliente'])
def cliente_create(request):
    """
    Cria um item de um cliente.
    """
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.POST._mutable = _mutable
    serializer = ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_cliente', 'change_cliente', 'delete_cliente'])
def cliente_detail(request, pk):
    """
    Retorna, atualiza ou deleta um item de um cliente.
    """
    try:
        empresa = get_user_empresa(request)
        cliente = Cliente.objects.get(pk=pk, empresa__id=empresa)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        _mutable = request.POST._mutable
        request.POST._mutable = True
        request.data['empresa'] = empresa
        request.POST._mutable = _mutable
        serializer = ClienteSerializer(cliente, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_cliente'])
def get_cliente_by_cpf(request, cpf):
    try:
        empresa = get_user_empresa(request)
        cliente = Cliente.objects.get(cpf=cpf, empresa__id=empresa)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Views - CompraEstoque

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_compraestoque'])
def compra_estoque_list(request):
    """
    Lista os itens de uma Compra de Estoque.
    """
    empresa = get_user_empresa(request)
    compras_estoque = CompraEstoque.objects.filter(empresa__id=empresa)
    serializer = CompraEstoqueSerializer(compras_estoque, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_required(['add_compraestoque'])
def compra_estoque_create(request, produto_pk):
    """
    Cria um item de uma Compra de Estoque.
    """
    produto = Produto.objects.get(pk=produto_pk)
    empresa = get_user_empresa(request)
    _mutable = request.POST._mutable
    request.POST._mutable = True
    request.data['empresa'] = empresa
    request.data['produto'] = produto_pk
    request.data['preco'] = produto.order_by('-data_alteracao')[0].preco_custo
    request.data['valor_total'] = request.data['preco'] * request.data['qtd']
    request.POST._mutable = _mutable
    serializer = CompraEstoqueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        produto.estoque += serializer.data['qtd']
        produto.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
@permission_required(['view_compraestoque', 'delete_compraestoque'])
def compra_estoque_detail(request, pk):
    """
    Retorna, atualiza ou deleta um item de uma Compra de Estoque.
    """
    try:
        empresa = get_user_empresa(request)
        compra_estoque = CompraEstoque.objects.get(pk=pk, empresa__id=empresa)
    except CompraEstoque.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompraEstoqueSerializer(compra_estoque)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        produto = compra_estoque.produto
        produto.estoque -= compra_estoque.qtd
        produto.save()
        compra_estoque.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Views - Search

@api_view(['GET'])
def search(request):
    empresa = get_user_empresa(request)
    search_value = request.GET.get('search')
    produtos = Produto.objects.filter(nome__iregex=rf'((?i)\b{search_value}\b)', descricao__iregex=rf'((?i)\b{search_value}\b)', empresa__id=empresa)
    serializer = ProdutoSerializer(produtos, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# Views - Relatórios

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_produto'])
def relatorio_mais_vendidos(request):
    empresa = get_user_empresa(request)
    produtos = Produto.objects.filter(empresa__id=empresa).order_by('-qtd_vendas').values()
    serializer = ProdutoSerializer(produtos, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_venda'])
def relatorio_venda_mensal(request):

    def get_valor(obj):
        return obj['valor']

    data_comeco, data_fim = return_date()

    empresa = get_user_empresa(request)
    vendas = Venda.objects.filter(empresa__id=empresa, data__range=[data_comeco, data_fim])
    serializer = VendaSerializer(vendas, many=True)
    valor = sum(map(get_valor, serializer.data))

    return Response({"valor": valor}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_funcionario', 'view_venda'])
def relatorio_comissao_mensal(request):
    empresa = get_user_empresa(request)
    try: 
        pk = request.user.id
        if pk == Empresa.objects.get(pk=empresa).administrador.pk:
            comissao_adm()
        else:
            funcionario = Funcionario.objects.get(pk=pk, empresa__id=empresa)
            comissao_func(funcionario)
    except:
        return Response({"msg": "Nao e um funcionario"}, status=status.HTTP_400_BAD_REQUEST)

    data_comeco, data_fim = return_date()
    
    def get_valor_funcionarios(obj):
        valor = obj.valor
        comissao = obj.vendedor.comissao
        valor_final = valor / 100 * float(comissao)
        return valor_final

    def get_valor(obj):
        return obj['valor']

    def comissao_adm():
        vendas = Venda.objects.filter(empresa__id=empresa, data__range=[data_comeco, data_fim])
        valor = sum(map(get_valor_funcionarios, vendas))
        return Response({"valor": valor}, status=status.HTTP_200_OK)

    def comissao_func(funcionario):
        vendas = Venda.objects.filter(empresa__id=empresa, vendedor=funcionario, data__range=[data_comeco, data_fim])
        serializer = VendaSerializer(vendas, many=True)
        valor = sum(map(get_valor, serializer.data)) / 100 * float(funcionario.comissao)

        return Response({"valor": valor}, status=status.HTTP_200_OK)


# Views - Dados juntos

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@permission_required(['view_categoria', 'view_plataforma', 'view_genero', 'view_faixaetaria'])
def dados_cadastro_produto(request):
    empresa = get_user_empresa(request)
    categorias = Categoria.objects.filter(empresa__id=empresa)
    serializer_categorias = CategoriaSerializer(categorias, many=True)
    plataformas = Plataforma.objects.filter(empresa__id=empresa)
    serializer_plataformas = PlataformaSerializer(plataformas, many=True)
    generos = Genero.objects.filter(empresa__id=empresa)
    serializer_generos = GeneroSerializer(generos, many=True)
    faixasetarias = FaixaEtaria.objects.filter(empresa__id=empresa)
    serializer_faixasetarias = FaixaEtariaSerializer(faixasetarias, many=True)

    dados = {
        "categorias": serializer_categorias.data,
        "plataformas": serializer_plataformas.data,
        "generos": serializer_generos.data,
        "faixas": serializer_faixasetarias.data
    }

    return Response(dados, status=status.HTTP_200_OK)
    
