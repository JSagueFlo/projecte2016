# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160502154303 on 2016-05-02 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centre',
            name='lat',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=9),
        ),
        migrations.AlterField(
            model_name='centre',
            name='lng',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=9),
        ),
    ]