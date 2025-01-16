# Generated by Django 5.1.4 on 2025-01-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_cooling_system_model_cooling_system_socket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case_model',
            name='case_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='cooling_system_model',
            name='cooling_system_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='cooling_system_model',
            name='cooling_system_socket',
            field=models.TextField(max_length=50),
        ),
        migrations.AlterField(
            model_name='cpu_model',
            name='cpu_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='gpu_model',
            name='gpu_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='motherboard_model',
            name='motherboard_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='power_supply_model',
            name='power_supply_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='ram_model',
            name='ram_description',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='storage_model',
            name='storage_description',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]