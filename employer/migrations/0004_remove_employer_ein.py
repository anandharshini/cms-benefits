# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-04 16:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_auto_20190801_0826'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer',
            name='ein',
        ),
    ]
