from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from empresas.models import Empresa, Cargo

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
    is_staff                = models.BooleanField('isAdmin', default=False)
    is_active               = models.BooleanField('active', default=True)
    date_joined             = models.DateTimeField('data de entrada', default=timezone.now, editable=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'primeiro_nome', 'ultimo_nome']
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuario"

    def get_full_name(self):
        nome_completo = f'{self.primeiro_nome} {self.ultimo_nome}'
        return nome_completo
    
    def get_short_name(self):
        return self.primeiro_nome

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Administrador(models.Model):
    usuario                 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='administradores')


class Funcionario(models.Model):
    usuario                 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='funcionarios')
    empresa                 = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios')
    cargo                   = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='funcionarios')

