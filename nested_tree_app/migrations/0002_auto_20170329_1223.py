# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-03-29 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nested_tree_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='content',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]