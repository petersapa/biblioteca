# Generated by Django 5.2 on 2025-05-22 14:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('cognom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Alumne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idalu', models.CharField(max_length=20, unique=True)),
                ('curs', models.CharField(max_length=50)),
                ('usuari', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Llibre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titol', models.CharField(max_length=200)),
                ('descripcio', models.TextField(blank=True)),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('prestat', models.BooleanField(default=False)),
                ('autor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='biblioteca.autor')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='biblioteca.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Prestec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_prestec', models.DateField(auto_now_add=True)),
                ('data_devolucio', models.DateField(blank=True, null=True)),
                ('alumne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.alumne')),
                ('llibre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblioteca.llibre')),
            ],
        ),
    ]
