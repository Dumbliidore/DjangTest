# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-19 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20180418_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
    ]