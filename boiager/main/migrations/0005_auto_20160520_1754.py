# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160502154303 on 2016-05-20 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160519_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='boia',
            name='ip',
            field=models.CharField(blank=True, default='80.174.145.128:8080', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='registre_boia',
            name='humiext',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=6),
        ),
    ]