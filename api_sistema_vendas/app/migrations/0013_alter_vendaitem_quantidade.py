# Generated by Django 4.1 on 2022-11-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_vendaitem_quantidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendaitem',
            name='quantidade',
            field=models.IntegerField(default=1),
        ),
    ]
