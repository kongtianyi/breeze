# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-18 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171023_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exts',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='Key')),
                ('value', models.CharField(max_length=200, verbose_name='Value')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'ext',
            },
        ),
    ]
