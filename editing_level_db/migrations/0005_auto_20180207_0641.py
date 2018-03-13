# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editing_level_db', '0004_sample_tumor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editing_site',
            name='strand',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='cancer',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='name',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='tumor',
        ),
        migrations.AddField(
            model_name='editing_site',
            name='is_forward',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='sample',
            name='age_at_initial_pathologic_diagnosis',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='cancer_type',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='days_to_birth',
            field=models.IntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='days_to_death',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='days_to_last_followup',
            field=models.IntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='histological_type',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='history_of_neoadjuvant_treatment',
            field=models.CharField(max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='is_male',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sample',
            name='is_tumor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sample',
            name='number_of_times_in_patient',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='number_of_times_in_stage',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='other_dx',
            field=models.CharField(max_length=50, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='person_neoplasm_cancer_status',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='postoperative_rx_tx',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='radiation_therapy',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='sample_barcode',
            field=models.CharField(max_length=50, unique=True, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='stage_event_clinical_stage',
            field=models.PositiveIntegerField(default=0, choices=[(0, '--'), (1, 'Stage_I'), (2, 'Stage_II'), (3, 'Stage_III'), (4, 'Stage_IV')]),
        ),
        migrations.AddField(
            model_name='sample',
            name='stage_event_pathologic_stage',
            field=models.CharField(max_length=15, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='tissue_prospective_collection_indicator',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='tissue_retrospective_collection_indicator',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='tnm_categories_pathologic_M',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='tnm_categories_pathologic_N',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='tnm_categories_pathologic_T',
            field=models.CharField(max_length=10, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='tumor_tissue_site',
            field=models.CharField(max_length=100, default=''),
        ),
        migrations.AddField(
            model_name='sample',
            name='vital_status',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AddField(
            model_name='sample',
            name='year_of_initial_pathologic_diagnosis',
            field=models.PositiveIntegerField(null=True, default=None),
        ),
        migrations.AlterField(
            model_name='editing_level',
            name='level',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=9),
        ),
        migrations.AlterField(
            model_name='editing_site',
            name='conserve',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='editing_site',
            name='site',
            field=models.PositiveIntegerField(),
        ),
    ]
