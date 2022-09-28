from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Permission, AnonymousUser
from .serializers import LoginSerializer, RegisterSerializer, PermissionSerializer, EmpresaSerializer, FornecedorSerializer, FuncionarioSerializer, CargoSerializer, CategoriaSerializer, FaixaEtariaSerializer, GeneroSerializer, PlataformaSerializer, PrecoSerializer, ProdutoSerializer, VendaSerializer, VendaItemSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Empresa, Fornecedor, Funcionario, Cargo, Produto, FaixaEtaria, Categoria, Genero, Plataforma, Preco, Venda, VendaItem
from toolbox import confere_permissao
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
confere_permissao(empresa_detail, 'view_empresa')
confere_permissao(empresa_detail, 'change_empresa')
confere_permissao(empresa_detail, 'delete_empresa')


# Views - Fornecedor

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fornecedor_list(request):
    """
    Lista os fornecedores.
    """
    empresa = get_user_empresa(request)
    fornecedores = Fornecedor.objects.filter(empresa__id=empresa)
    serializer = FornecedorSerializer(fornecedores, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(fornecedor_list, 'view_fornecedor')


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
confere_permissao(fornecedor_create, 'add_fornecedor')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = FornecedorSerializer(fornecedor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fornecedor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(fornecedor_detail, 'view_fornecedor')
confere_permissao(fornecedor_detail, 'change_fornecedor')
confere_permissao(fornecedor_detail, 'delete_fornecedor')

# Views - Funcionário

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def funcionario_list(request):
    """
    Lista os funcionarios
    """
    empresa = get_user_empresa(request)
    func = Funcionario.objects.filter(empresa__id=empresa)
    serializer = FuncionarioSerializer(func, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(funcionario_list, 'view_funcionario')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def funcionario_create(request):
    """
    Cria um Funcionário
    """
    user_serializer = RegisterSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        request_copy = request.POST.copy()
        request_copy['empresa'] = request.user.empresa.id
        request_copy['usuario'] = user
        func_serializer = FuncionarioSerializer(data=request_copy)
        if func_serializer.is_valid():
            func_serializer.save()    
            return Response(func_serializer.data, status=status.HTTP_201_CREATED)
        return Response(func_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
confere_permissao(funcionario_create, 'add_funcionario')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = FuncionarioSerializer(funcionario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        funcionario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(funcionario_detail, 'view_funcionario')
confere_permissao(funcionario_detail, 'change_funcionario')
confere_permissao(funcionario_detail, 'delete_funcionario')


# Views - Cargo

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cargo_list(request):
    """
    Lista os cargos.
    """
    empresa = get_user_empresa(request)
    cargo = Cargo.objects.filter(empresa__id=empresa)
    serializer = CargoSerializer(cargo, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(cargo_list, 'view_cargo')


@api_view(['GET', 'POST'])
def cargo_create(request):
    """
    Cria um cargo.
    """
    if request.method == 'POST':
        serializer = CargoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = CargoSerializer()
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(cargo_create, 'add_cargo')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def cargo_detail(request, pk):
    """
    Retorna, atualiza ou deleta um cargo.
    """
    try:
        empresa = get_user_empresa(request)
        cargo = Cargo.objects.get(pk=pk, empresa__id=empresa)
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
confere_permissao(cargo_detail, 'view_cargo')
confere_permissao(cargo_detail, 'change_cargo')
confere_permissao(cargo_detail, 'delete_cargo')


# Views - Produto

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def produto_list(request):
    """
    Lista os produtos.
    """
    empresa = get_user_empresa(request)
    produtos = Produto.objects.filter(empresa__id=empresa)
    serializer = ProdutoSerializer(produtos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(produto_list, 'view_produto')


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
confere_permissao(produto_create, 'add_produto')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = ProdutoSerializer(produto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        produto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(produto_detail, 'view_produto')
confere_permissao(produto_detail, 'change_produto')
confere_permissao(produto_detail, 'delete_produto')


# Views - Categoria

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categoria_list(request):
    """
    Lista as categorias.
    """
    empresa = get_user_empresa(request)
    categorias = Categoria.objects.filter(empresa__id=empresa)
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(categoria_list, 'view_categoria')


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
confere_permissao(categoria_create, 'add_categoria')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(categoria_detail, 'view_categoria')
confere_permissao(categoria_detail, 'change_categoria')
confere_permissao(categoria_detail, 'delete_categoria')


# Views - Faixa Etária

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def faixa_list(request):
    """
    Lista as faixas etárias.
    """
    faixas = FaixaEtaria.objects.filter(empresa__id=request.user.empresa.id)
    serializer = FaixaEtariaSerializer(faixas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(faixa_list, 'view_faixaetaria')


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
confere_permissao(faixa_create, 'add_faixaetaria')


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
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = FaixaEtariaSerializer(faixa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        faixa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(faixa_detail, 'view_faixaetaria')
confere_permissao(faixa_detail, 'change_faixaetaria')
confere_permissao(faixa_detail, 'delete_faixaetaria')


# Views - Gênero

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genero_list(request):
    """
    Lista os gêneros.
    """
    empresa = get_user_empresa(request)
    generos = Genero.objects.filter(empresa__id=empresa)
    serializer = GeneroSerializer(generos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(genero_list, 'view_genero')


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
confere_permissao(genero_create, 'add_genero')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(genero_detail, 'view_genero')
confere_permissao(genero_detail, 'change_genero')
confere_permissao(genero_detail, 'delete_genero')


# Views - Plataforma

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plataforma_list(request):
    """
    Lista as plataformas.
    """
    empresa = get_user_empresa(request)
    plataformas = Plataforma.objects.filter(empresa__id=empresa)
    serializer = PlataformaSerializer(plataformas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(plataforma_list, 'view_plataforma')


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
confere_permissao(plataforma_create, 'add_plataforma')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = PlataformaSerializer(plataforma, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plataforma.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(plataforma_detail, 'view_plataforma')
confere_permissao(plataforma_detail, 'change_plataforma')
confere_permissao(plataforma_detail, 'delete_plataforma')


# Views - Preço

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def preco_list(request):
    """
    Lista os preços.
    """
    empresa = get_user_empresa(request)
    precos = Preco.objects.filter(empresa__id=empresa)
    serializer = PrecoSerializer(precos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(preco_list, 'view_preco')


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
confere_permissao(preco_create, 'add_preco')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        serializer = PrecoSerializer(preco, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        preco.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
confere_permissao(preco_detail, 'view_preco')
confere_permissao(preco_detail, 'change_preco')
confere_permissao(preco_detail, 'delete_preco')


@api_view(['GET'])
def search(request):
    search_value = request.GET.get('search')
    produtos = Produto.objects.filter(nome__iregex=rf'((?i)\b{search_value}\b)', descricao__iregex=rf'((?i)\b{search_value}\b)')
    serializer = ProdutoSerializer(produtos, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


# Views - Venda

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def venda_list(request):
    """
    Lista as vendas.
    """
    vendas = Venda.objects.filter(empresa=request.user.funcionario.empresa.id)
    serializer = VendaSerializer(vendas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(venda_list, 'view_venda')


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
confere_permissao(venda_create, 'add_venda')


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
confere_permissao(venda_detail, 'view_venda')
confere_permissao(venda_detail, 'change_venda')
confere_permissao(venda_detail, 'delete_venda')


# Views - VendaItem

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendaitem_list(request):
    """
    Lista os itens de uma venda.
    """
    vendaitens = VendaItem.objects.filter(empresa=request.user.funcionario.empresa.id)
    serializer = VendaItemSerializer(vendaitens, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
confere_permissao(vendaitem_list, 'view_vendaitem')


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
confere_permissao(vendaitem_create, 'add_vendaitem')


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
confere_permissao(vendaitem_detail, 'view_vendaitem')
confere_permissao(vendaitem_detail, 'change_vendaitem')
confere_permissao(vendaitem_detail, 'delete_vendaitem')

