# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-18 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_exts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exts',
            name='value',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Value'),
        ),
    ]
