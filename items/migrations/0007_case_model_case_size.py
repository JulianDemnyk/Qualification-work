# Generated by Django 5.1.4 on 2025-01-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_gpu_model_gpu_bits_gpu_model_gpu_power_consumption'),
    ]

    operations = [
        migrations.AddField(
            model_name='case_model',
            name='case_size',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
