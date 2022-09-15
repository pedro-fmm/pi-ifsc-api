# Generated by Django 4.1 on 2022-09-15 14:50

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=15, unique=True, verbose_name='usuario')),
                ('primeiro_nome', models.CharField(max_length=30, verbose_name='primeiro nome')),
                ('ultimo_nome', models.CharField(max_length=30, verbose_name='ultimo nome')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='endereco e-mail')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, verbose_name='isAdmin')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='data de entrada')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('descricao', models.CharField(max_length=512)),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('cpf', models.CharField(max_length=11)),
                ('rg', models.CharField(blank=True, max_length=7)),
                ('email', models.CharField(max_length=256)),
                ('telefone', models.CharField(max_length=11)),
                ('endereco', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('razao_social', models.CharField(max_length=256)),
                ('nome_fantasia', models.CharField(max_length=256)),
                ('cnpj', models.CharField(max_length=14)),
                ('icone', models.FileField(blank=True, upload_to='media/icones-empresa/')),
                ('administrador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
                'ordering': ['nome_fantasia'],
            },
        ),
        migrations.CreateModel(
            name='FaixaEtaria',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('faixa', models.CharField(max_length=256)),
                ('descricao', models.CharField(max_length=512)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faixas', to='app.empresa')),
            ],
            options={
                'verbose_name': 'faixa etária',
                'verbose_name_plural': 'faixas etárias',
                'ordering': ['faixa'],
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa_funcionarios', to='app.empresa')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'funcionario',
                'verbose_name_plural': 'funcionarios',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('descricao', models.CharField(max_length=512)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generos', to='app.empresa')),
            ],
            options={
                'verbose_name': 'gênero',
                'verbose_name_plural': 'gêneros',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Plataforma',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('descricao', models.CharField(max_length=512)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plataformas', to='app.empresa')),
            ],
            options={
                'verbose_name': 'plataformas',
                'verbose_name_plural': 'plataformas',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('descricao', models.TextField()),
                ('imagem', models.FileField(blank=True, upload_to='media')),
                ('data_criacao', models.DateField(auto_now_add=True)),
                ('estoque', models.IntegerField(default=0)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='app.categoria')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='app.empresa')),
                ('faixa_etaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='app.faixaetaria')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='app.genero')),
                ('plataforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='app.plataforma')),
            ],
            options={
                'verbose_name': 'produto',
                'verbose_name_plural': 'produtos',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Venda',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=12)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('numero', models.IntegerField(default=app.models.contador, editable=False, unique=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='app.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='app.empresa')),
                ('vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendas', to='app.funcionario')),
            ],
            options={
                'verbose_name': 'venda',
                'verbose_name_plural': 'vendas',
                'ordering': ['data'],
            },
        ),
        migrations.CreateModel(
            name='VendaItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('valor_produto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendaitens', to='app.produto')),
                ('venda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendaitens', to='app.venda')),
            ],
        ),
        migrations.CreateModel(
            name='Preco',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('preco_custo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('preco_venda', models.DecimalField(decimal_places=2, max_digits=8)),
                ('descricao', models.CharField(max_length=512)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='precos', to='app.empresa')),
            ],
            options={
                'verbose_name': 'preço',
                'verbose_name_plural': 'preços',
                'ordering': ['data_alteracao'],
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('razao_social', models.CharField(max_length=256)),
                ('nome_fantasia', models.CharField(max_length=256)),
                ('cnpj', models.CharField(max_length=14)),
                ('icone', models.FileField(blank=True, upload_to='media/icones-empresa/')),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresas_fornecedor', to='app.empresa')),
            ],
            options={
                'verbose_name': 'fornecedores',
                'verbose_name_plural': 'fornecedor',
                'ordering': ['nome_fantasia'],
            },
        ),
        migrations.AddField(
            model_name='cliente',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas_cliente', to='app.empresa'),
        ),
        migrations.AddField(
            model_name='categoria',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='app.empresa'),
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresa', to='app.empresa')),
                ('permissoes', models.ManyToManyField(to='auth.permission')),
            ],
            options={
                'verbose_name': 'cargo',
                'verbose_name_plural': 'cargos',
                'ordering': ['nome'],
            },
        ),
        migrations.AddField(
            model_name='usuario',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuarios', to='app.cargo'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
