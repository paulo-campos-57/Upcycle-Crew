# Generated by Django 5.1.3 on 2024-11-08 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upcycleproject', '0015_alter_unit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
