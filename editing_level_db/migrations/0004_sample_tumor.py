# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0003_auto_20180205_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='tumor',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
