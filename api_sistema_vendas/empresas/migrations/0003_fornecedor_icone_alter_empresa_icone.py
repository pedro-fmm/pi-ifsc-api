# Generated by Django 4.1 on 2022-08-25 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0002_cargo_empresa_alter_fornecedor_empresa_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='fornecedor',
            name='icone',
            field=models.FileField(blank=True, upload_to='media/icones-empresa/'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='icone',
            field=models.FileField(blank=True, upload_to='media/icones-empresa/'),
        ),
    ]
