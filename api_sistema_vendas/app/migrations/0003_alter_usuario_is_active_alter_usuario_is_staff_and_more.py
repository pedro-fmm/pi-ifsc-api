# Generated by Django 4.1 on 2022-09-22 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_usuario_is_staff_alter_usuario_is_superuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
