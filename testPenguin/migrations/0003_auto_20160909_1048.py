# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-09 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testPenguin', '0002_auto_20160909_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='always_run',
            field=models.CharField(default='false', max_length=5),
        ),
    ]