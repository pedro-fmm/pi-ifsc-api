# Generated by Django 4.1 on 2022-11-03 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_compraestoque'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='cargo',
        ),
        migrations.DeleteModel(
            name='Cargo',
        ),
    ]
