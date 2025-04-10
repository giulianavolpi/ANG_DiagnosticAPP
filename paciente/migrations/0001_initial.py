# Generated by Django 3.2.6 on 2025-03-13 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('infoAdmin', '0002_auto_20250313_0443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('num_documento', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('edad', models.IntegerField()),
                ('medicos', models.ManyToManyField(to='infoAdmin.Medico')),
            ],
        ),
    ]
