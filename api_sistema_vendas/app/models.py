from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from uuid import uuid4
from django.contrib.auth.models import Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    """
    Gerenciador de usuários personalizados que cria e salva usuários e super usuários.
    """
    def create_user(self, email, username, primeiro_nome, ultimo_nome, password=None):
        """
        Cria e salva um usuário com o email, nome de usuário, primeiro nome e ultimo nome fornecidos.
        """
        if not email:
            raise ValueError('Usuários devem ter um email')
        if not username:
            raise ValueError('Usuários devem ter um nome de usuário')
        if not primeiro_nome:
            raise ValueError('Usuários devem ter um primeiro nome')
        if not ultimo_nome:
            raise ValueError('Usuários devem ter um último nome')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, username, primeiro_nome, ultimo_nome, password=None):
        """
        Cria e salva um super usuário com email, nome de usuário, primeiro nome e último nome fornecidos.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuario(PermissionsMixin, AbstractBaseUser):
    """
    Modelo de usuário personalizado com seus devidos campos
    """
    username                = models.CharField('usuario', max_length=15, unique=True)
    primeiro_nome           = models.CharField('primeiro nome', max_length=30)
    ultimo_nome             = models.CharField('ultimo nome', max_length=30)
    email                   = models.EmailField('endereco e-mail', max_length=255, unique=True)
    is_admin                = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_superuser            = models.BooleanField(default=False)
    date_joined             = models.DateTimeField('data de entrada', default=timezone.now, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'primeiro_nome', 'ultimo_nome']
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def get_full_name(self):
        nome_completo = f'{self.primeiro_nome} {self.ultimo_nome}'
        return nome_completo
    
    def get_short_name(self):
        return self.primeiro_nome

    def has_perm(self, perm, obj=None):
        try:
            if perm in self.funcionario.cargo.grupos:
                return True        
            return False
        except: return True

    def has_module_perms(self, app_label):
        return True


class Empresa(models.Model):
    """
    Modelo das empresas com seus respectivos campos.
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    administrador           = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='empresa')
    razao_social            = models.CharField(max_length=256) 
    nome_fantasia           = models.CharField(max_length=256)
    cnpj                    = models.CharField(max_length=14)
    icone                   = models.FileField(upload_to='media/icones-empresa/', blank=True)

    class Meta:
        ordering            = ["nome_fantasia"]
        verbose_name        = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.nome_fantasia


class Cargo(models.Model):
    """
    Modelo dos cargos
    """
    
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa')
    permissoes              = models.ManyToManyField(Permission)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "cargo"
        verbose_name_plural = "cargos"

    def __str__(self):
        return self.nome


class Funcionario(models.Model):
    usuario                 = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='funcionario')
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empresa_funcionarios')
    cargo                   = models.ForeignKey('Cargo', on_delete=models.CASCADE, related_name='funcionarios')
    comissao                = models.DecimalField(max_digits=2, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "funcionario"
        verbose_name_plural = "funcionarios"


class Fornecedor(models.Model):
    """
    Modelo dos fornecedores
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    razao_social            = models.CharField(max_length=256) 
    nome_fantasia           = models.CharField(max_length=256)
    cnpj                    = models.CharField(max_length=14)
    icone                   = models.FileField(upload_to='media/icones-empresa/', blank=True)
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas_fornecedor', null=True)

    class Meta:
        ordering            = ["nome_fantasia"]
        verbose_name        = "fornecedores"
        verbose_name_plural = "fornecedor"

    def __str__(self):
        return self.nome_fantasia


class Cliente(models.Model):
    """
    Modelo dos clientes
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    cpf                     = models.CharField(max_length=11)
    rg                      = models.CharField(max_length=7, blank=True)
    email                   = models.CharField(max_length=256)
    telefone                = models.CharField(max_length=11)
    endereco                = models.CharField(max_length=256)
    empresa                 = models.ForeignKey('Empresa', on_delete=models.CASCADE, related_name='empresas_cliente')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nome


class Plataforma(models.Model):
    """
    Modelo das plataformas com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='plataformas')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "plataformas"
        verbose_name_plural = "plataformas"

    def __str__(self):
        return self.nome

       
class FaixaEtaria(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    faixa                   = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='faixas')

    class Meta:
        ordering            = ["faixa"]
        verbose_name        = "faixa etária"
        verbose_name_plural = "faixas etárias"

    def __str__(self):
        return self.faixa


class Genero(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='generos')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "gênero"
        verbose_name_plural = "gêneros"

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.nome


class Preco(models.Model):
    """
    Modelo das faixas etárias com seus respectivos campos
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    produto                 = models.ForeignKey('Produto', on_delete=models.CASCADE, related_name='precos')
    data_alteracao          = models.DateTimeField(auto_now_add=True)
    preco_custo             = models.DecimalField(max_digits=8, decimal_places=2)
    preco_venda             = models.DecimalField(max_digits=8, decimal_places=2)
    descricao               = models.CharField(max_length=512)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='precos')

    class Meta:
        ordering            = ["data_alteracao"]
        verbose_name        = "preço"
        verbose_name_plural = "preços"

    def __str__(self):
        return str(self.preco_venda)


class Produto(models.Model):
    """
    Modelo dos produtos com seus respectivos campos.

    Tags tornam a pesquisa mais fácil.
    """
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome                    = models.CharField(max_length=256)
    descricao               = models.TextField()
    imagem                  = models.FileField(upload_to='media', blank=True)
    plataforma              = models.ForeignKey('Plataforma', on_delete=models.CASCADE, related_name='produtos')
    faixa_etaria            = models.ForeignKey('FaixaEtaria', on_delete=models.CASCADE, related_name='produtos')
    genero                  = models.ForeignKey('Genero', on_delete=models.CASCADE, related_name='produtos')
    categoria               = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='produtos')
    data_criacao            = models.DateField(auto_now_add=True)
    estoque                 = models.IntegerField(default=0)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='produtos')
    qtd_vendas              = models.IntegerField(default=0)

    class Meta:
        ordering            = ["nome"]
        verbose_name        = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.nome

    @property
    def is_disponivel(self):
        """
        Retorna a diponibilidade do produto.
        True    - estoque > 0
        False   - estoque <= 0 
        """
        if(self.estoque > 0):
            return True
        else:
            return False


def contador():
    numero = Venda.objects.count()
    if not numero:
        return 1
    else:
        return numero + 1


class Venda(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    cliente                 = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vendas')
    vendedor                = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='vendas')
    valor                   = models.DecimalField(max_digits=12, decimal_places=2)
    data                    = models.DateTimeField(auto_now_add=True)
    numero                  = models.IntegerField(default=contador, unique=True, editable=False)
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vendas')

    class Meta:
        ordering            = ["data"]
        verbose_name        = "venda"
        verbose_name_plural = "vendas"

    def __str__(self):
        return self.numero


class VendaItem(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    produto                 = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='vendaitens')
    venda                   = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='vendaitens')
    valor_produto           = models.ForeignKey(Preco, on_delete=models.DO_NOTHING, related_name="vendaitens")
