# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-09 10:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testPenguin', '0003_auto_20160909_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='step_type',
        ),
    ]
