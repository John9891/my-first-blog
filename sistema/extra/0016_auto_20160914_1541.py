# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 20:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0015_remove_tiempoasignacion_numerobus'),
    ]

    operations = [
        migrations.AddField(
            model_name='despacho',
            name='NumeroBus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.BusAlimentador'),
        ),
        migrations.AddField(
            model_name='tiempoasignacion',
            name='NumeroBus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sistema.BusAlimentador'),
        ),
    ]