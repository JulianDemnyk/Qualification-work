# Generated by Django 5.1.4 on 2025-04-19 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0013_remove_case_model_case_featured_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpu_model',
            name='cpu_power_consumption',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
