# Generated by Django 5.0.4 on 2024-04-16 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_remove_usuariol_oficinar_usuariol_area'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='rubro',
        ),
        migrations.AddField(
            model_name='registro',
            name='rubro',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='usuarios.rubro'),
        ),
    ]
