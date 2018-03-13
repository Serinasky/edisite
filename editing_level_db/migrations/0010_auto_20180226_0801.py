# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0009_editing_site_is_snp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editing_site',
            name='is_snp',
        ),
        migrations.AddField(
            model_name='editing_site',
            name='snp_id',
            field=models.CharField(max_length=20, default='NA'),
        ),
    ]
