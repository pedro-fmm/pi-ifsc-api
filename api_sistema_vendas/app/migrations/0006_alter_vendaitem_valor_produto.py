# Generated by Django 4.1 on 2022-10-06 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_funcionario_comissao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendaitem',
            name='valor_produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='vendaitens', to='app.preco'),
        ),
    ]
