# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-14 18:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0009_auto_20160913_1825'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='busalimentador',
            options={'ordering': ['NumeroBus'], 'verbose_name_plural': 'BusAlimentador'},
        ),
        migrations.AddField(
            model_name='despacho',
            name='BusAlimentador',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='sistema.BusAlimentador'),
        ),
        migrations.AddField(
            model_name='tiempoasignacion',
            name='BusAlimentador',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='sistema.BusAlimentador'),
        ),
    ]