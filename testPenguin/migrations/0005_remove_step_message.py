# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-09 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testPenguin', '0004_remove_step_step_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='message',
        ),
    ]
