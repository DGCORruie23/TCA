# Generated by Django 5.0.4 on 2024-06-28 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0013_remove_acciona2_area2_remove_acciona2_idaccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='claveAcuerdo',
            field=models.TextField(default='Clave de Acuerdo'),
        ),
    ]