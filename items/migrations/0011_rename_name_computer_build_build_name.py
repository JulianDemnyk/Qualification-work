# Generated by Django 5.1.4 on 2025-04-12 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0010_computer_build_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer_build',
            old_name='name',
            new_name='build_name',
        ),
    ]
