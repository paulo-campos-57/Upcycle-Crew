# Generated by Django 5.1.3 on 2024-11-07 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upcycleproject', '0006_unit_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemthrown',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='upcycleproject.unit'),
        ),
    ]