# Generated by Django 5.1.3 on 2024-11-07 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upcycleproject', '0004_remove_itemthrown_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemthrown',
            name='name',
        ),
    ]