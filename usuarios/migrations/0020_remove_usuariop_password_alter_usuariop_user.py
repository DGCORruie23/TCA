# Generated by Django 4.2.6 on 2024-07-10 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuarios', '0019_rename_usuario_usuariop'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariop',
            name='password',
        ),
        migrations.AlterField(
            model_name='usuariop',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='usuarioP', to=settings.AUTH_USER_MODEL),
        ),
    ]
