# Generated by Django 5.1.4 on 2025-01-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooling_system_model',
            name='cooling_system_socket',
            field=models.TextField(max_length=100),
        ),
    ]