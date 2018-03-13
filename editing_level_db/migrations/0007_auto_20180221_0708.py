# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0006_editing_site_num_of_edited_samples'),
    ]

    operations = [
        migrations.AddField(
            model_name='editing_level',
            name='hyper_A',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='hyper_C',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='hyper_G',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='hyper_T',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='normal_A',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='normal_C',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='normal_G',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='editing_level',
            name='normal_T',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='editing_level',
            name='level',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=19),
        ),
    ]
