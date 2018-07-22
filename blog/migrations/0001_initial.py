# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-23 23:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='文章标题')),
                ('category_id', models.IntegerField(verbose_name='分类id')),
                ('tags', models.TextField(verbose_name='标签')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('summery', models.TextField(null=True, verbose_name='文章简介')),
                ('pv', models.IntegerField(blank=True, default=0, null=True, verbose_name='Page View')),
                ('uv', models.IntegerField(blank=True, default=0, null=True, verbose_name='Unique View')),
                ('comment_count', models.IntegerField(blank=True, default=0, null=True, verbose_name='评论数')),
                ('url', models.CharField(max_length=200, verbose_name='时间索引url')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, verbose_name='分类名')),
                ('parent_id', models.IntegerField(verbose_name='父分类id')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'categorys',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('article_id', models.IntegerField(verbose_name='评论博文id')),
                ('comment_author', models.CharField(max_length=30, verbose_name='评论者昵称')),
                ('comment_author_email', models.CharField(max_length=100, verbose_name='评论者邮箱')),
                ('comment_author_url', models.CharField(max_length=200, verbose_name='评论者主页')),
                ('comment_author_ip', models.CharField(max_length=100, verbose_name='评论者ip')),
                ('comment_content', models.TextField(verbose_name='评论内容')),
                ('comment_approved', models.IntegerField(blank=True, default=0, null=True, verbose_name='评论是否通过审核')),
                ('comment_parent', models.IntegerField(verbose_name='父评论id 0-文章评论')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
