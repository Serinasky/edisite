# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0008_auto_20180226_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='editing_site',
            name='is_snp',
            field=models.NullBooleanField(default=None),
        ),
    ]
