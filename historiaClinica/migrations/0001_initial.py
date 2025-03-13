# Generated by Django 3.2.6 on 2025-03-13 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaClinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paciente_id', models.CharField(max_length=100)),
                ('es_menor_edad', models.BooleanField(default=False)),
                ('existe', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
                ('genero', models.CharField(max_length=50)),
                ('medico', models.CharField(max_length=50)),
            ],
        ),
    ]
