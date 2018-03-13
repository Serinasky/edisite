# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0002_auto_20180205_0452'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editing_level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('level', models.CharField(max_length=20)),
                ('sample', models.ForeignKey(to='editing_level_db.Sample')),
            ],
        ),
        migrations.RenameField(
            model_name='editing_site',
            old_name='attr2',
            new_name='gene',
        ),
        migrations.RenameField(
            model_name='editing_site',
            old_name='attr1',
            new_name='utr',
        ),
        migrations.RemoveField(
            model_name='editing_site',
            name='editing_level',
        ),
        migrations.RemoveField(
            model_name='editing_site',
            name='sample',
        ),
        migrations.AddField(
            model_name='editing_level',
            name='site',
            field=models.ForeignKey(to='editing_level_db.Editing_site'),
        ),
    ]
