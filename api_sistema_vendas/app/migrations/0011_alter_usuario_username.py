# Generated by Django 4.1 on 2022-11-10 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_funcionario_comissao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=15, verbose_name='usuario'),
        ),
    ]
