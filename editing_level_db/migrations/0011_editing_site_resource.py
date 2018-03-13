# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0010_auto_20180226_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='editing_site',
            name='resource',
            field=models.CharField(max_length=15, default='U', choices=[('RP', 'RediPortal'), ('HE', 'HyperEditing'), ('B', 'Both'), ('U', 'Unknown')]),
        ),
    ]
