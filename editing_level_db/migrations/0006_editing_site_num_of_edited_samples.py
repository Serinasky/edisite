# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0005_auto_20180207_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='editing_site',
            name='num_of_edited_samples',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
