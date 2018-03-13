# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editing_site',
            name='editing_level',
            field=models.CharField(max_length=20),
        ),
    ]
