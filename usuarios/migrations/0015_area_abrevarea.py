# Generated by Django 5.0.4 on 2024-07-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_registro_claveacuerdo'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='abrevArea',
            field=models.CharField(default='abreviatura', max_length=15),
        ),
    ]
