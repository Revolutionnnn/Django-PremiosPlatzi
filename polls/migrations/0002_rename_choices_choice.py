# Generated by Django 4.1.5 on 2023-01-17 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Choices',
            new_name='Choice',
        ),
    ]