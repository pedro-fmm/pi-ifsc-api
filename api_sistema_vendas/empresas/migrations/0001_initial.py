# Generated by Django 4.1 on 2022-08-25 14:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('razao_social', models.CharField(max_length=256)),
                ('nome_fantasia', models.CharField(max_length=256)),
                ('cnpj', models.CharField(max_length=14)),
                ('icone', models.FileField(blank=True, upload_to='media/icones-empresa/')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
                'ordering': ['nome_fantasia'],
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
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresas_fornecedor', to='empresas.empresa')),
            ],
            options={
                'verbose_name': 'fornecedores',
                'verbose_name_plural': 'fornecedor',
                'ordering': ['nome_fantasia'],
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
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas_cliente', to='empresas.empresa')),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=256)),
                ('is_admin', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_produtos', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_clientes', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_fornecedores', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_product', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_cargos', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('manage_funcionarios', models.BooleanField(choices=[('Pode', True), ('Não pode', False)], default=False)),
                ('empresa', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='empresas_cargo', to='empresas.empresa')),
            ],
            options={
                'verbose_name': 'cargo',
                'verbose_name_plural': 'cargos',
                'ordering': ['nome'],
            },
        ),
    ]
