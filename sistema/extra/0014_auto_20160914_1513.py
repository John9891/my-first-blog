# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 20:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0013_auto_20160914_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='despacho',
            name='NumeroBus',
        ),
        migrations.AlterField(
            model_name='tiempoasignacion',
            name='NumeroBus',
            field=models.ForeignKey(blank=True, default=800, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.BusAlimentador'),
        ),
    ]
