# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-01 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logger", "0026_auto_20160913_0239"),
    ]

    operations = [
        migrations.AlterField(
            model_name="widget",
            name="title",
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
