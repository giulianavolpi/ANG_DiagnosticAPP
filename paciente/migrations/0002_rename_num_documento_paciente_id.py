# Generated by Django 3.2.6 on 2025-03-13 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paciente',
            old_name='num_documento',
            new_name='id',
        ),
    ]
