# Generated by Django 5.1.4 on 2025-04-13 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_case_model_case_featured_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case_model',
            name='case_featured',
        ),
        migrations.RemoveField(
            model_name='computer_build',
            name='build_featured',
        ),
        migrations.RemoveField(
            model_name='cooling_system_model',
            name='cooling_system_featured',
        ),
        migrations.RemoveField(
            model_name='cpu_model',
            name='cpu_featured',
        ),
        migrations.RemoveField(
            model_name='gpu_model',
            name='gpu_featured',
        ),
        migrations.RemoveField(
            model_name='motherboard_model',
            name='motherboard_featured',
        ),
        migrations.RemoveField(
            model_name='power_supply_model',
            name='power_supply_featured',
        ),
        migrations.RemoveField(
            model_name='ram_model',
            name='ram_featured',
        ),
        migrations.RemoveField(
            model_name='storage_model',
            name='storage_featured',
        ),
    ]
