# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Editing_site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('chromosome', models.CharField(max_length=10)),
                ('site', models.CharField(max_length=10)),
                ('strand', models.CharField(max_length=1)),
                ('attr1', models.CharField(max_length=10)),
                ('attr2', models.CharField(max_length=50)),
                ('repetitive', models.CharField(max_length=30)),
                ('conserve', models.CharField(max_length=10)),
                ('editing_level', models.DecimalField(max_digits=20, decimal_places=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('cancer', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='editing_site',
            name='sample',
            field=models.ForeignKey(to='editing_level_db.Sample'),
        ),
    ]
