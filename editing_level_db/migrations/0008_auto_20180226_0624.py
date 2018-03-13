# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0007_auto_20180221_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='editing_site',
            name='ed',
            field=models.CharField(max_length=1, default='NA'),
        ),
        migrations.AddField(
            model_name='editing_site',
            name='edited_in_percent',
            field=models.DecimalField(null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='editing_site',
            name='mi_rna_gain',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_site',
            name='mi_rna_loss',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_site',
            name='ref',
            field=models.CharField(max_length=1, default='NA'),
        ),
    ]
